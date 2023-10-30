
# Imports
import argparse
import logging
import threading
import time

import pysailfish.internal.observability.log_helper as lh
from pysailfish.internal.Network.TCPCast import TCPCast, TCPStatus

# Variables
server_ip: str = "192.168.1.104" # "0.0.0.0"
server_port: int = 7788
tcp_server: TCPCast = TCPCast()
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

def server_worker() -> int:
    logger = lh.init_logger(logger_name="sailfish_logger", is_json_output=False)
    if tcp_server.InitComponent(if_address=server_ip
                                , if_port=server_port
                                , is_client=False) == TCPStatus.ERROR:
        logger.error("Cannot create tcp server. Stop.")
        return -1

    client_socket, client_address = tcp_server.Accept()
    count: int = 1
    while True:
        send_status: TCPStatus = tcp_server.ServerSend(client_socket=client_socket, send_msg="Hello from server")
        if send_status == TCPStatus.SUCCESS:
            logger.info(f"Server send success: {count}")
        else:
            logger.error(f"Server send failed: {count}")
        count += 1

        recv_status, recv_msg = tcp_server.ServerRecv(client_socket=client_socket)
        if recv_status == TCPStatus.SUCCESS:
            logger.info(f"Received message: {recv_msg}")

        time.sleep(1)

    return 0

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

    count: int = 2000
    while True:
        recv_status, recv_msg = tcp_client.ClientRecv()
        if recv_status == TCPStatus.SUCCESS:
            logger.info(f"Client received message: {recv_msg}")

        if tcp_client.ClientSend(send_msg="Hello from client") == TCPStatus.SUCCESS:
            logger.info(f"Client send success: {count}")
        else:
            logger.error(f"Client send failed: {count}")

        count += 1
        time.sleep(1)

    return 0

def main() -> None:
    """! sailfish main function

    @return None
    """
    logger = lh.init_logger(logger_name="sailfish_logger", is_json_output=False)
    args = init_argparse(description="sailfish Inputs")
    logger.info(f"We get args: {args}")

    # Here put your logic
    server_th: threading.Thread = threading.Thread(target=server_worker)
    server_th.start()
    time.sleep(1)

    client_th: threading.Thread = threading.Thread(target=client_worker)
    client_th.start()

    time.sleep(5)

if __name__ == "__main__":
    main()
