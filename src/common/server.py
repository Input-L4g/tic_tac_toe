import socket
from threading import Thread

# Recebe a ação.
# Valida.
# Atualiza o estado.
# Envia a resposta para todos os clientes (broadcast).

class Server:
    def __init__(self, host="0.0.0.0", port=5000) -> None:
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()

    def start_server(self) -> None:
        print(f"O servidor está ligado em: {self.host}:{self.port}")
        while True:
            client_socket, addr = self.server_socket.accept()
            
