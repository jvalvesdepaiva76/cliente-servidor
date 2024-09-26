# File: server/server.py
import socket
from ds.avl_tree import AVLTree

class TaskServer:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.task_tree = AVLTree()  # AVL Tree para gerenciar tarefas
        self.next_id = 1  # Para gerar IDs únicos para as tarefas
    
    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            # Adiciona a opção para reutilizar a porta
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            server_socket.bind((self.host, self.port))
            server_socket.listen()
            print(f"Servidor iniciado em {self.host}:{self.port}")
            while True:
                conn, addr = server_socket.accept()
                with conn:
                    print(f"Conectado a {addr}")
                    self.handle_client(conn)
    
    def handle_client(self, conn):
        data = conn.recv(1024)
        if data:
            response = self.process_command(data.decode())
            conn.sendall(response.encode())
    
    def process_command(self, command: str) -> str:
        """
        Processa os comandos recebidos do cliente.
        Comandos disponíveis:
        - ADD <descrição>: Adiciona uma nova tarefa
        - LIST: Lista todas as tarefas
        - REMOVE <id>: Remove uma tarefa pelo ID
        - SEARCH <id>: Busca uma tarefa pelo ID
        """
        parts = command.split()

        if not parts:
            return "Comando inválido."

        action = parts[0].upper()

        if action == "ADD":
            if len(parts) < 2:
                return "Erro: descrição da tarefa não fornecida."
            description = ' '.join(parts[1:])
            return self.add_task(description)

        elif action == "LIST":
            return self.list_tasks()

        elif action == "REMOVE":
            if len(parts) != 2:
                return "Erro: ID da tarefa não fornecido."
            try:
                task_id = int(parts[1])
                return self.remove_task(task_id)
            except ValueError:
                return "Erro: ID da tarefa deve ser um número."

        elif action == "SEARCH":
            if len(parts) != 2:
                return "Erro: ID da tarefa não fornecido."
            try:
                task_id = int(parts[1])
                return self.search_task(task_id)
            except ValueError:
                return "Erro: ID da tarefa deve ser um número."

        return "Comando desconhecido."

    def add_task(self, description: str) -> str:
        """Adiciona uma nova tarefa na AVL Tree."""
        task = {
            'id': self.next_id,  # ID único
            'description': description,
            'completed': False  # Status da tarefa
        }
        self.task_tree.insert(task)  # Insere o dicionário da tarefa na AVL Tree
        self.next_id += 1
        return f"Tarefa adicionada com sucesso. ID: {task['id']}"

    def list_tasks(self) -> str:
        """Lista todas as tarefas armazenadas na AVL Tree."""
        tasks = []
        self.task_tree.inorder(lambda node: tasks.append(node.value))  # Faz o "inorder traversal" para obter todas as tarefas
        if not tasks:
            return "Nenhuma tarefa encontrada."
        task_list = "\n".join([f"ID: {task['id']}, Descrição: {task['description']}, Concluída: {task['completed']}" for task in tasks])
        return f"Tarefas:\n{task_list}"

    def remove_task(self, task_id: int) -> str:
        """Remove uma tarefa pelo ID."""
        task = self.task_tree.search(task_id)
        if task:
            self.task_tree.delete(task_id)
            return f"Tarefa {task_id} removida com sucesso."
        return f"Tarefa {task_id} não encontrada."

    def search_task(self, task_id: int) -> str:
        """Busca uma tarefa pelo ID."""
        task = self.task_tree.search(task_id)
        if task:
            return f"ID: {task['id']}, Descrição: {task['description']}, Concluída: {task['completed']}"
        return f"Tarefa {task_id} não encontrada."

if __name__ == '__main__':
    server = TaskServer()
    server.start()
