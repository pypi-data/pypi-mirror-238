import logging
import time
import traceback
import socket
from typing import List, Dict, Tuple, Union, Set, Any
from datetime import datetime

import pysailfish.internal.observability.log_helper as lh
from pysailfish.internal.Network.TCPCast import TCPCast, TCPStatus
from pysailfish.internal.devTools.ThreadClass import ThreadClass
from pysailfish.internal.MT_EA.mt4_fun_num_map import mt4_fun_num_map

class MT4_TCP_Client(object):
    def __init__(self):
        self.soc: socket = None
        self.address: str = ""
        self.data_pool: str = ""

class MT4DataCtrl_Server(ThreadClass):
    def __init__(self):
        self.__logger: logging.Logger = None
        self.__tcp_server: TCPCast = None
        self.__tcp_clients: Dict[str, MT4_TCP_Client] = dict()
        self.__mt4_msg_callback: Any = None
        self.__mt4_no_msg_callback: Any = None
        self.__data_pool: str = ""
        self.__cmd_start: str = "cmd_start"
        self.__cmd_end: str = "cmd_end"
        self.__cmd_end_len: int = len(self.__cmd_end)
        self.__hb_interval_sec: int = 5
        self.__last_hb_time: datetime = None
        self.__fun_num_map: Dict[str, int] = mt4_fun_num_map

    # override
    def init_component(self
                       , logger: logging.Logger
                       , tcp_server: TCPCast
                       , mt4_msg_callback: Any
                       , mt4_no_msg_callback: Any):
        self.__logger = logger
        self.__tcp_server = tcp_server
        self.__mt4_msg_callback = mt4_msg_callback
        self.__mt4_no_msg_callback = mt4_no_msg_callback

        super().init_component(logger=logger)

    def send_heartbeat(self) -> None:
        # check if time to send out heartbeat
        if self.__last_hb_time is None:
            # update hb send time
            self.__last_hb_time = datetime.now()
        else:
            cur_time = datetime.now()
            if (cur_time - self.__last_hb_time).total_seconds() > self.__hb_interval_sec:
                # update hb send time
                self.__last_hb_time = cur_time
            else:
                # too early to send out heartbeat
                return None

        hb_data = list()
        hb_data.append(str(self.__fun_num_map["Heartbeat"]))

        failed_client_names: List[str] = list()
        for client_name, client_ele in self.__tcp_clients.items():
            try:
                self.send_message_to_one(client_ele=client_ele
                                         , data=hb_data)
            except Exception as e:
                # assumpt connection issue when exception catached
                # remove connection and wait for next client
                client_ele.soc.close()
                failed_client_names.append(client_name)

        for failed_client_name in failed_client_names:
            # remove connection and wait for next client
            del self.__tcp_clients[failed_client_name]
            self.__logger.error(f"Remove client: {failed_client_name} due to heartbeat failed")

        return None

    def send_message_to_one(self, client_ele: MT4_TCP_Client, data: List[str]) -> None:
        send_msg: str = self.__get_send_msg(data=data)
        self.__tcp_server.ServerSend(client_socket=client_ele.soc
                                     , send_msg=send_msg)

        return None

    def send_message_to_all(self, data: List[str]) -> None:
        send_msg: str = self.__get_send_msg(data=data)

        # send to mt4
        for client in self.__tcp_clients.values():
            self.__tcp_server.ServerSend(client_socket=client.soc
                                         , send_msg=send_msg)

        return None

    def receive_data_from_client(self
                                 , tcp_server: TCPCast
                                 , client_ele: MT4_TCP_Client) -> bool:
        recv_status, recv_msg = tcp_server.ServerRecv(client_socket=client_ele.soc)

        if recv_status == TCPStatus.SUCCESS:
            client_ele.data_pool += recv_msg
            return True
        elif recv_status == TCPStatus.ERROR:
            client_ele.data_pool = ""
            return False
        else:
            return True

        return True

    def get_message_from_client(self
                                , cmd_end: str
                                , client_ele: MT4_TCP_Client) -> Union[str, List[str]]:
        if not client_ele.data_pool.find(cmd_end):
            # command not finished, process next client
            return (None, None)

        start_pos = -1
        end_pos = -1

        # find next start position
        start_pos = client_ele.data_pool.find(self.__cmd_start, start_pos + 1)
        # find next end position
        end_pos = client_ele.data_pool.find(self.__cmd_end, end_pos + 1)
        if start_pos == -1 or end_pos == -1:
            # no more complete commands found
            return (None, None)
        if start_pos > end_pos:
            # should not go to this case
            return (None, None)

        # extract one command from data pool
        # cmd: cmd_start,cmd_count,cmd_content,cmd_end
        cmd = client_ele.data_pool[start_pos:end_pos+self.__cmd_end_len]
        # remove old data from pool
        client_ele.data_pool = client_ele.data_pool[end_pos+self.__cmd_end_len:]

        parts: List[str] = cmd.split(",")
        if len(parts) < 3:
            self.__logger.error(f"message is not completed: {cmd}")
            return (None, None)

        cmd_count: int = int(parts[1])
        if cmd_count + 3 != len(parts):
            # skip this command due to checksum is wrong
            return (None, None)

        fun_name: str = parts[2]
        return (fun_name, parts[3:-1])

    # override
    def _user_main(self) -> None:
        self.__accept_clients()
        if len(self.__tcp_clients) == 0:
            time.sleep(0.01)
            return None

        self.send_heartbeat()

        failed_client_names: List[str] = list()
        for client_name, client_ele in self.__tcp_clients.items():
            if self.receive_data_from_client(tcp_server=self.__tcp_server
                                             , client_ele=client_ele):
                fun_name, parts = self.get_message_from_client(cmd_end=self.__cmd_end, client_ele=client_ele)
                if fun_name is None:
                    continue

                try:
                    self.__mt4_msg_callback(fun_name=fun_name, parts=parts)
                except Exception as e:
                    self.__logger.error(e)
                    traceback.print_exc()
            else:
                client_ele.soc.close()
                failed_client_names.append(client_name)

        # remove failed clients
        for failed_client_name in failed_client_names:
            del self.__tcp_clients[failed_client_name]
            self.__logger.error(f"Remove client: {failed_client_name} due to receive failed")

        self.__mt4_no_msg_callback()

    def __get_send_msg(self, data: List[str]) -> str:
        # message start
        send_msg: str = self.__cmd_start + ","
        # message count
        send_msg += str(len(data)) + ","
        # message content
        send_msg += ",".join(data) + ","
        # message end
        send_msg += self.__cmd_end

        return send_msg

    def __accept_clients(self) -> bool:
        client_socket, client_address = self.__tcp_server.Accept()
        if client_socket is None:
            return False

        client_ele = MT4_TCP_Client()
        client_ele.soc = client_socket
        client_ele.address = client_address

        while self.receive_data_from_client(tcp_server=self.__tcp_server
                                            , client_ele=client_ele):
            fun_name, parts = self.get_message_from_client(cmd_end=self.__cmd_end, client_ele=client_ele)

            if fun_name is None:
                continue

            if fun_name != "Client_Registration":
                self.__logger.error(f"Get client with address: {client_address} in a wrong registration formality. Close it now.")
                client_socket.close()
                return False

            # process registration for new client
            client_name: str = f"{parts[0]}.{parts[1]}" # broker_name.account_name
            # insert to the map
            self.__logger.info(f"Add client with name: {client_name}, address: {client_address}")
            self.__tcp_clients.update({client_name: client_ele})

            return True

        return False
