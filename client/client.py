# File: client/client.py
import socket

class TaskClient:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
    
    def connect(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((self.host, self.port))
            self.interact(client_socket)
    
    def interact(self, client_socket):
        while True:
            command = input("Digite um comando para o servidor: ")
            if command.lower() == 'exit':
                break
            client_socket.sendall(command.encode())
            response = client_socket.recv(1024)
            print("Resposta do servidor:", response.decode())

if __name__ == '__main__':
    client = TaskClient()
    client.connect()
