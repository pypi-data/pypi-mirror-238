
# Imports
import argparse
import logging
import threading
import time


import pysailfish.internal.observability.log_helper as lh
from pysailfish.internal.Network.TCPCast import TCPCast, TCPStatus

# Variables
server_ip: str = "127.0.0.1" # "0.0.0.0" --- for linux and docker "127.0.0.1" --- for windows
server_port: int = 23456
tcp_client: TCPCast = TCPCast()

# Functions
def init_argparse(description: str = "") -> argparse.Namespace:
    """! initial argument parser

    @param description Argument parser description

    @return argument parser
    """
    parser = argparse.ArgumentParser(description=description)
    # parser.add_argument("-a", "--action", required=True)
    # parser.add_argument("-l", "--lang", required=True)
    # parser.add_argument("-pn", "--projectName", default="")
    return parser.parse_args()

def client_worker() -> int:
    logger = lh.init_logger(logger_name="sailfish_logger", is_json_output=False)
    if tcp_client.InitComponent(if_address=server_ip
                                , if_port=server_port
                                , is_client=True) == TCPStatus.ERROR:
        logger.error("Cannot create tcp client. Stop.")
        return -1

    if tcp_client.Connect(to_address=server_ip
                          , to_port=server_port) == TCPStatus.ERROR:
        logger.error("Cannot connect to tcp server. Stop.")
        return -1

    count = 0
    while count < 10000:
        count += 1
        recv_status, recv_msg = tcp_client.ClientRecv()
        if recv_status == TCPStatus.SUCCESS:
            if recv_msg != "":
                logger.info(f"Client received message: {recv_msg}")

    return 0

def main() -> None:
    """! sailfish main function

    @return None
    """
    logger = lh.init_logger(logger_name="sailfish_logger", is_json_output=False)
    args = init_argparse(description="sailfish Inputs")
    logger.info(f"We get args: {args}")

    # Here put your logic
    client_th: threading.Thread = threading.Thread(target=client_worker)
    client_th.start()

    time.sleep(5)

if __name__ == "__main__":
    main()
