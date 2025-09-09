import socket
from src.core.types import SocketConection, Address
from src.common.connection_handler import ConnectionHandler

class Client:
    def __init__(
        self,
        conn: SocketConection,
        addr: Address
        ) -> None:
        self.conn = conn
        self.addr = addr
        self.handler = ConnectionHandler(self.conn, self.addr)
