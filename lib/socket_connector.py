import socket

class SocketServer:

    def __init__(self, port: int, host_ip: str) -> None:
        self.port: int = port
        # self.host_name: str = socket.gethostname()
        # self.host_ip: str = socket.gethostbyname(self.host_name)
        self.host_ip: str = host_ip
        print('Host IP:', self.host_ip)
        self.socket = socket.socket()
        self.client_socket = None

    def listen(self):
        print('Open socket.')
        self.socket.bind((self.host_ip, self.port))
        self.socket.listen(600)
        print('Server listening on port', self.port)
        
    def accept(self):
        self.client_socket, address = self.socket.accept()
    
    def read(self, bytes: int) -> bytearray:
        return self.client_socket.recv(bytes)

    def send(self, data) -> int:
        return self.client_socket.send(data)

    def close(self) -> None:
        self.client_socket.close()
        self.socket.close()

    def is_connected(self) -> bool:
        return self.client_socket != None

class SocketClient:

    def __init__(self, port: int, host_ip: str) -> None:
        self.port: int = port
        # self.host_name: str = socket.gethostname()
        # self.host_ip: str = socket.gethostbyname(self.host_name)
        self.host_ip: str = host_ip
        print('Host IP:', self.host_ip)
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def connect(self):
        socket_address = (self.host_ip, self.port)
        self.socket.connect(socket_address)

    def read(self, bytes: int) -> bytearray:
        return self.socket.recv(bytes)

    def send(self, data: bytearray) -> int:
        return self.socket.send(data)

    def close(self) -> None:
        self.socket.close()

class SocketConnector:

    def __init__(self, port: int, host_ip: str) -> None:
        self.port: int = port
        self.host_ip: str = host_ip
        self.socket = None

    def open_socket(self, is_server: bool) -> None:
        if is_server:
            self.socket: SocketServer = SocketServer(self.port, self.host_ip)
            self.__open_socket_server()
        else:
            self.socket: SocketClient = SocketClient(self.port, self.host_ip)
            self.__open_socket_client()

    def __open_socket_server(self) -> None:
        self.socket.listen()
        self.socket.accept()

    def __open_socket_client(self) -> None:
        print('Open client socket.')
        self.socket.connect()

    def close(self) -> None:
        self.socket.close()
