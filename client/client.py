import socket
from ds.queue import Fila, FilaError

class TaskClient:
    """
    Classe que representa o cliente responsável por enviar comandos e receber respostas do servidor.

    Atributos:
    host (str): Endereço do servidor.
    port (int): Porta de comunicação com o servidor.
    message_queue (Fila): Fila encadeada para gerenciar mensagens enviadas e recebidas.
    """
    
    def __init__(self, host: str = 'localhost', port: int = 12345) -> None:
        """
        Inicializa o cliente com o endereço e porta do servidor.

        Args:
        host (str): Endereço do servidor. Padrão é 'localhost'.
        port (int): Porta de comunicação com o servidor. Padrão é 12345.
        """
        self.host = host
        self.port = port
        self.message_queue = Fila()

    def connect(self) -> None:
        """
        Conecta ao servidor e inicia a interação.

        Se a conexão falhar, exibe uma mensagem de erro para o usuário.
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((self.host, self.port))
                print(f"Conectado ao servidor em {self.host}:{self.port}")
                self.interact(client_socket)
        except ConnectionRefusedError:
            print(f"Erro: Não foi possível conectar ao servidor {self.host}:{self.port}. Verifique se o servidor está ativo.")
        except socket.gaierror:
            print(f"Erro: Nome ou endereço do host inválido ({self.host}).")
        except Exception as e:
            print(f"Erro inesperado ao tentar conectar: {str(e)}")

    def interact(self, client_socket: socket.socket) -> None:
        """
        Interage com o servidor enviando comandos e recebendo respostas.

        Args:
        client_socket (socket.socket): O socket usado para a comunicação com o servidor.
        """
        while True:
            command = input("Digite um comando para o servidor: ")

            if command.lower() == 'exit':
                print("Desconectando...")
                break

            try:
                self.message_queue.enfileira(command)
                self.send_message(client_socket)
                response = client_socket.recv(1024).decode()
                self.message_queue.enfileira(response)
                self.process_response()
            except socket.error:
                print("Erro: Falha na comunicação com o servidor. Verifique sua conexão.")
                break
            except FilaError as fe:
                print(f"Erro na manipulação da fila: {str(fe)}")
            except Exception as e:
                print(f"Erro inesperado: {str(e)}")

    def send_message(self, client_socket: socket.socket) -> None:
        """
        Envia a mensagem atual ao servidor usando a fila de mensagens.

        Args:
        client_socket (socket.socket): O socket usado para a comunicação com o servidor.
        """
        try:
            message = self.message_queue.desenfileira()
            client_socket.sendall(message.encode())
        except FilaError as fe:
            print(f"Erro ao enviar a mensagem: {str(fe)}")
        except socket.error:
            print("Erro: Falha ao enviar dados ao servidor.")
        except Exception as e:
            print(f"Erro inesperado ao enviar a mensagem: {str(e)}")

    def process_response(self) -> None:
        """
        Processa a resposta recebida do servidor a partir da fila de mensagens.
        """
        try:
            response = self.message_queue.desenfileira()
            print(f"Resposta do servidor: {response}")
        except FilaError as fe:
            print(f"Erro ao processar a resposta: {str(fe)}")
        except Exception as e:
            print(f"Erro inesperado ao processar a resposta: {str(e)}")


if __name__ == '__main__':
    client = TaskClient()
    client.connect()
