import socket
import threading
from src.core.types import ConectionPort, IpAddress, ResponseMessage
from src.common.connection_handler import ConnectionHandler
from src.protocols.message_protocol import create_error_message
from src.core.config import RESPONSE_CODES
from src.utils.validation_utils import was_successful

class Client:
    def __init__(
        self,
        host: IpAddress,
        port: ConectionPort
        ) -> None:
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()

    def listen(self) -> None:


    def connect(self) -> ResponseMessage:
        result = self._try_connection()
        if not was_successful(result['code']):
            return result

        socket_thread = threading.Thread(target=self.listen)

        print(f"Conectado em {self.host}:{self.port}")

    def _try_connection(self) -> ResponseMessage:
        """
        Tenta se conectar a um servidor.

        Returns:
            ResponseMessage: Mensagem de resposta da operação.
        """
        try:
            self.sock.connect((self.host, self.port))
            result = create_error_message(0)
        except socket.gaierror:
            result = create_error_message(1001)
        except ConnectionRefusedError:
            result = create_error_message(1002)
        except socket.timeout:
            result = create_error_message(1003)
        except OSError as e:
            result = create_error_message(1004, e)
        except Exception as e: # pylint: disable=broad-exception-caught
            result = create_error_message(1000, e)
        return result
