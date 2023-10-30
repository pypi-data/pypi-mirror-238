from typing import Dict, List, Set, Tuple, Union, Any
from datetime import datetime
import logging
import time
import decimal

import pysailfish.internal.observability.log_helper as lh
from pysailfish.internal.DataCtrl.MT4DataCtrl.MT4DataCtrl_Server import MT4DataCtrl_Server
from pysailfish.internal.Network.TCPCast import TCPCast, TCPStatus

class MT4_EA_Server(object):
    def __init__(self):
        self.__data_ctrl_server: MT4DataCtrl_Server = None
        self.__logger: logging.Logger = None

    def InitComponent(self
                      , logger: logging.Logger
                      , data_ctrl_server: MT4DataCtrl_Server) -> None:
        self.__logger = logger
        self.__data_ctrl_server = data_ctrl_server

        return None

    def Start_EA(self) -> None:
        self.__data_ctrl_server.start_th()

        while True:
            time.sleep(1)

        return None

    def Process_MT4_Message(self, fun_name: str, parts: List[str]) -> None:
        self.__logger.info(parts)
        return None

    def Process_No_MT4_Message(self) -> None:
        time.sleep(0.01)

        return None


def main() -> None:
    ea_name: str = "MT4_Server_EA"
    logger = lh.init_logger(logger_name=f"{ea_name}_logger", is_json_output=False)

    ea = MT4_EA_Server()
    # initial tcp cast
    tcp_server: TCPCast = TCPCast()
    tcp_server.InitComponent(if_address="127.0.0.1"
                             , if_port=23456
                             , is_client=False
                             , num_clients=10
                             , timeout_in_seconds=0)
    # initial mt4 data control
    mt4_data_ctrl: MT4DataCtrl_Server = MT4DataCtrl_Server()
    mt4_data_ctrl.init_component(logger=logger
                                 , tcp_server=tcp_server
                                 , mt4_msg_callback=ea.Process_MT4_Message
                                 , mt4_no_msg_callback=ea.Process_No_MT4_Message)
    # initial EA as a server
    ea.InitComponent(logger=logger, data_ctrl_server=mt4_data_ctrl)
    ea.Start_EA()

if __name__ == "__main__":
    main()
