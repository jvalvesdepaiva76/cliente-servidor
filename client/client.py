# File: client/client.py
import socket
from server.ds.queue import Fila, FilaError

class TaskClient:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.message_queue = Fila()  # Fila encadeada para gerenciar mensagens enviadas e recebidas
    
    def connect(self):
        """Conecta-se ao servidor e interage com o servidor."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((self.host, self.port))
            print(f"Conectado ao servidor em {self.host}:{self.port}")
            self.interact(client_socket)
    
    def interact(self, client_socket):
        """Interage com o servidor, enviando comandos e recebendo respostas."""
        while True:
            command = input("Digite um comando para o servidor: ")

            if command.lower() == 'exit':
                print("Desconectando...")
                break

            # Coloca a mensagem na fila antes de enviar
            self.message_queue.enfileira(command)

            # Processa a mensagem da fila para envio
            self.send_message(client_socket)

            # Recebe a resposta do servidor
            response = client_socket.recv(1024).decode()

            # Armazena a resposta recebida na fila
            self.message_queue.enfileira(response)

            # Processa a resposta recebida
            self.process_response()

    def send_message(self, client_socket):
        """Envia a mensagem para o servidor a partir da fila."""
        try:
            message = self.message_queue.desenfileira()  # Retira a mensagem da fila
            client_socket.sendall(message.encode())  # Envia para o servidor
        except FilaError as fe:
            print(f"Erro ao enviar a mensagem: {str(fe)}")

    def process_response(self):
        """Processa a resposta recebida do servidor a partir da fila."""
        try:
            response = self.message_queue.desenfileira()  # Retira a resposta da fila
            print(f"Resposta do servidor: {response}")
        except FilaError as fe:
            print(f"Erro ao processar a resposta: {str(fe)}")

if __name__ == '__main__':
    client = TaskClient()
    client.connect()
