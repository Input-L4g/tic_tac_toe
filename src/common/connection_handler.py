import socket
from src.core.types import SocketConection, Address
from src.managers.game_manager import GameManager
from src.protocols.serialize import serialize, deserialize

class ConnectionHandler:
    def __init__(
        self,
        conn: SocketConection,
        addr: Address
        ) -> None:
        self.client_socket = conn
        self.addr = addr
        self.game_manager = GameManager()

    def run(self) -> None:
        print(f"Cliente conectado: {self.addr}")
        try:
            while True:
                client_data = deserialize(self.client_socket.recv(1024))
                if not client_data:
                    break

                self.game_manager.apply_action(client_data)
        except Exception as e: # pylint: disable=<broad-exception-caught>
            print(f"Erro com o cliente {self.addr}: {e}")
        finally:
            try:
                self.client_socket.shutdown(socket.SHUT_RDWR)
                self.client_socket.close()
            except:
                pass
            print(f'Cliente {self.addr} foi desconectado com sucesso.')
