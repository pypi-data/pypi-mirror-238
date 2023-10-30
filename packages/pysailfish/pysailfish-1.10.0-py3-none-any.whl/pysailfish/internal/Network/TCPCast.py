from enum import Enum
from typing import Union, Set, List, Tuple, Dict, Any
import threading
import signal
import traceback
import socket
import select

class TCPStatus(Enum):
    SUCCESS = 1
    ERROR = 2
    READ = 3
    TIMEOUT = 4

class TCPCast(object):
    def __init__(self) -> None:
        self.__socket: socket = None
        self.__if_address: str = ""
        self.__if_port: int = 0
        self.__is_client: bool = False
        self.__num_clients: int = 0
        self.__buffer_size: int = 1024 * 1024 * 5 # 5 MB
        self.__client_mutex: threading.Lock = threading.Lock()
        self.__server_mutex: threading.Lock = threading.Lock()
        self.__timeout_in_seconds: float = 1
        self.__is_connected: bool = False

        signal.signal(signal.SIGINT, self.__stop)

    def InitComponent(self
                      , if_address: str
                      , if_port: int
                      , is_client: bool
                      , num_clients: int = 5
                      , timeout_in_seconds: float = 1) -> TCPStatus:
        self.__if_address = if_address
        self.__if_port = if_port
        self.__is_client = is_client
        self.__num_clients = num_clients
        self.__timeout_in_seconds = timeout_in_seconds

        if self.__is_client:
            self.__if_port = 0
            self.__num_clients = 0

        return self.__start(if_address=self.__if_address
                            , if_port=self.__if_port
                            , is_client=self.__is_client
                            , num_clients=self.__num_clients
                            , timeout_in_seconds=self.__timeout_in_seconds)

    # Client
    def Connect(self, to_address: str, to_port: int) -> TCPStatus:
        try:
            self.__socket.connect((to_address, to_port))
            with self.__client_mutex:
                self.__is_connected = True
        except Exception as e:
            with self.__client_mutex:
                self.__is_connected = False
            return TCPStatus.ERROR

        return TCPStatus.SUCCESS

    def ClientSend(self, send_msg: str) -> TCPStatus:
        with self.__client_mutex:
            try:
                self.__socket.send(send_msg.encode())
            except Exception as e:
                self.__is_connected = False
                return TCPStatus.ERROR

        return TCPStatus.SUCCESS

    def ClientRecv(self) -> Union[TCPStatus, str]:
        try:
            ready = select.select([self.__socket], [], [], self.__timeout_in_seconds)
            if ready[0]:
                msg = self.__socket.recv(self.__buffer_size)
                return (TCPStatus.SUCCESS, msg.decode())
            return (TCPStatus.TIMEOUT, None)
        except Exception as e:
            with self.__client_mutex:
                self.__is_connected = False
            return (TCPStatus.ERROR, None)

    def IsClientConnected(self) -> bool:
        with self.__client_mutex:
            return self.__is_connected

        return False

    # Server
    def Accept(self) -> Union[socket.socket, str]:
        try:
            client_socket, client_address = self.__socket.accept()
            return (client_socket, client_address)
        except Exception as e:
            return (None, None)

    def ServerSend(self, client_socket: socket.socket, send_msg: str) -> TCPStatus:
        try:
            with self.__server_mutex:
                client_socket.send(send_msg.encode())
            return TCPStatus.SUCCESS
        except Exception as e:
            return TCPStatus.ERROR

    def ServerRecv(self, client_socket: socket.socket) -> Union[TCPStatus, str]:
        try:
            ready = select.select([client_socket], [], [], self.__timeout_in_seconds)
            if ready[0]:
                msg = client_socket.recv(self.__buffer_size)
                return (TCPStatus.SUCCESS, msg.decode())
            return (TCPStatus.TIMEOUT, None)
        except Exception as e:
            return (TCPStatus.ERROR, None)

    def __start(self
                , if_address: str
                , if_port: int
                , is_client: bool
                , num_clients: int
                , timeout_in_seconds: float) -> TCPStatus:
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.__socket == None:
            return TCPStatus.ERROR

        if is_client == False:
            self.__socket.settimeout(timeout_in_seconds)
            self.__socket.bind((if_address, if_port))
            self.__socket.listen(num_clients)

        # self.__socket.setblocking(0)
        return TCPStatus.SUCCESS

    def __stop(self, signum, frame):
        if self.__socket is not None:
            self.__socket.shutdown(how=0)
