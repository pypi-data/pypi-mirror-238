import logging
import time
import traceback
from typing import List, Dict, Tuple, Union, Set, Any
from datetime import datetime

import pysailfish.internal.observability.log_helper as lh
from pysailfish.internal.Network.TCPCast import TCPCast, TCPStatus
from pysailfish.internal.devTools.ThreadClass import ThreadClass

class MT4DataCtrl(ThreadClass):
    def __init__(self):
        self.__logger: logging.Logger = None
        self.__tcp_client: TCPCast = None
        self.__mt4_msg_callback: Any = None
        self.__data_pool: str = ""
        self.__cmd_start: str = "cmd_start"
        self.__cmd_end: str = "cmd_end"
        self.__cmd_end_len: int = len(self.__cmd_end)
        self.__proxy_msg: List[str] = list()

    # override
    def init_component(self
                       , logger: logging.Logger
                       , tcp_client: TCPCast
                       , mt4_msg_callback: Any):
        self.__logger = logger
        self.__tcp_client = tcp_client
        self.__mt4_msg_callback = mt4_msg_callback

        super().init_component(logger=logger)

    def is_connection_okay(self) -> bool:
        return self.__tcp_client.IsClientConnected()

    def send_message(self) -> None:
        # message start
        send_msg: str = self.__cmd_start + ","
        # message count
        send_msg += str(len(self.__proxy_msg)) + ","
        # message content
        send_msg += ",".join(self.__proxy_msg) + ","
        # message end
        send_msg += self.__cmd_end

        # send to mt4
        self.__tcp_client.ClientSend(send_msg=send_msg)

        self.__proxy_msg = list()

    def add_data_to_msg(self, data: str) -> None:
        self.__proxy_msg.append(data)

    def receive_string_from_mt4(self) -> str:
        fun_name, parts = self.receive_data_from_mt4()
        if fun_name is None:
            return ""
        else:
            return parts[0]

    def receive_bool_from_mt4(self) -> bool:
        fun_name, parts = self.receive_data_from_mt4()
        if fun_name is None or parts[0] == "":
            return False
        else:
            if parts[0] == "0":
                return False
            else:
                return True

    def receive_int_from_mt4(self) -> int:
        fun_name, parts = self.receive_data_from_mt4()
        if fun_name is None or parts[0] == "":
            return 0
        else:
            return int(parts[0])

    def receive_datetime_from_mt4(self) -> datetime:
        fun_name, parts = self.receive_data_from_mt4()
        if fun_name is None or parts[0] == "":
            return datetime(1970, 1, 1, 0, 0, 0)
        else:
            return datetime.strptime(parts[0], "%Y.%m.%d %H:%M:%S")

    def receive_float_from_mt4(self) -> float:
        fun_name, parts = self.receive_data_from_mt4()
        if fun_name is None or parts[0] == "":
            return 0
        else:
            return float(parts[0])

    def receive_data_from_mt4(self) -> Union[str, List[str]]:
        local_data_pool: str = ""
        while True:
            recv_status, recv_msg = self.__tcp_client.ClientRecv()
            if recv_status == TCPStatus.SUCCESS:
                local_data_pool += recv_msg
                if not local_data_pool.find(self.__cmd_end):
                    # command not ended then retry
                    continue

                parts: List[str] = local_data_pool.split(",")
                if len(parts) < 3:
                    self.__logger.error(f"message is not completed: {local_data_pool}")
                    return (None, None)

                cmd_count: int = int(parts[1])
                if cmd_count + 3 != len(parts):
                    # skip this command due to checksum is wrong
                    self.__logger.error(f"message checksum is wrong: {len(parts)}, expected: {cmd_count + 3}")
                    return (None, None)

                fun_name: str = parts[2]
                return (fun_name, parts[3:-1])

    # override
    def _user_main(self) -> None:
        recv_status, recv_msg = self.__tcp_client.ClientRecv()
        if recv_status == TCPStatus.SUCCESS:
            self.__data_pool += recv_msg
            if not self.__data_pool.find(self.__cmd_end):
                # command not ended
                return None

            while True:
                start_pos = -1
                end_pos = -1

                # find next start position
                start_pos = self.__data_pool.find(self.__cmd_start, start_pos + 1)
                # find next end position
                end_pos = self.__data_pool.find(self.__cmd_end, end_pos + 1)
                if start_pos == -1 or end_pos == -1:
                    # no more complete commands found
                    break
                if start_pos > end_pos:
                    # should not go to this case
                    break

                # extract one command from data pool
                # cmd: cmd_start,cmd_count,cmd_content,cmd_end
                cmd = self.__data_pool[start_pos:end_pos+self.__cmd_end_len]
                # remove old data from pool
                self.__data_pool = self.__data_pool[end_pos+self.__cmd_end_len:]

                parts: List[str] = cmd.split(",")
                if len(parts) < 3:
                    self.__logger.error(f"message is not completed: {cmd}")
                    continue

                cmd_count: int = int(parts[1])
                if cmd_count + 3 != len(parts):
                    # skip this command due to checksum is wrong
                    continue

                fun_name: str = parts[2]
                try:
                    self.__mt4_msg_callback(fun_name=fun_name, parts=parts[3:-1])
                except Exception as e:
                    self.__logger.error(e)
                    traceback.print_exc()
