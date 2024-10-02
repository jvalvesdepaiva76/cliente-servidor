# File: server/server.py
import socket
import threading
from ds.avl_tree import AVLTree
from datetime import datetime

class TaskServer:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.task_tree = AVLTree()  # AVL Tree para gerenciar tarefas
        self.next_id = 1  # Para gerar IDs únicos para as tarefas
        self.lock = threading.Lock()  # Lock para proteger o acesso a dados compartilhados
    
    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            # Adiciona a opção para reutilizar a porta
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            server_socket.bind((self.host, self.port))
            server_socket.listen()
            print(f"Servidor iniciado em {self.host}:{self.port}")

            while True:
                conn, addr = server_socket.accept()
                print(f"Conectado a {addr}")
                # Cria uma nova thread para lidar com o cliente
                client_thread = threading.Thread(target=self.handle_client, args=(conn,))
                client_thread.start()  # Inicia a thread
    
    def handle_client(self, conn):
        with conn:
            while True:
                try:
                    data = conn.recv(1024)
                    if not data:
                        break  # Se não há dados, encerra a conexão
                    response = self.process_command(data.decode())
                    conn.sendall(response.encode())
                except Exception as e:
                    # Logar exceções no servidor e enviar resposta ao cliente
                    conn.sendall(f"Erro no servidor: {str(e)}".encode())
                    break  # Em caso de erro, fecha a conexão

    def process_command(self, command: str) -> str:
        """
        Processa os comandos recebidos do cliente.
        Comandos disponíveis:
        - ADD <descrição> [data de vencimento (opcional)]: Adiciona uma nova tarefa com uma data opcional.
        - LIST: Lista apenas as tarefas não concluídas, com data de vencimento (se houver).
        - LIST_DETAILED: Lista as tarefas não concluídas com suas subtarefas (se houver).
        - TASK_HISTORY: Lista todas as tarefas (concluídas e não concluídas)
        - REMOVE <id>: Remove uma tarefa pelo ID
        - SEARCH <id>: Busca uma tarefa pelo ID
        - COMPLETE <id>: Marca uma tarefa como concluída
        - ADD_SUBTASK <id> <descrição>: Adiciona uma subtarefa a uma tarefa existente
        - LIST_SUBTASKS <id>: Lista todas as subtarefas de uma tarefa
        """
        parts = command.split()

        if not parts:
            return "Comando inválido."

        action = parts[0].upper()

        if action == "ADD":
            if len(parts) < 2:
                return "Erro: descrição da tarefa não fornecida."
            description = ' '.join(parts[1:-1])
            due_date = parts[-1] if self.is_valid_date(parts[-1]) else None
            if due_date:
                description = ' '.join(parts[1:-1])  # Corrige a descrição sem a data
            else:
                description = ' '.join(parts[1:])  # Se não houver data
            return self.add_task(description, due_date)

        elif action == "ADD_SUBTASK":
            if len(parts) < 3:
                return "Erro: ID da tarefa ou descrição da subtarefa não fornecido."
            try:
                task_id = int(parts[1])
                subtask_description = ' '.join(parts[2:])
                return self.add_subtask(task_id, subtask_description)
            except ValueError:
                return "Erro: ID da tarefa deve ser um número."

        elif action == "LIST_SUBTASKS":
            if len(parts) != 2:
                return "Erro: ID da tarefa não fornecido."
            try:
                task_id = int(parts[1])
                return self.list_subtasks(task_id)
            except ValueError:
                return "Erro: ID da tarefa deve ser um número."

        elif action == "LIST":
            return self.list_uncompleted_tasks()

        elif action == "LIST_DETAILED":
            return self.list_detailed_uncompleted_tasks()

        elif action == "TASK_HISTORY":
            return self.task_history()

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

        elif action == "COMPLETE":
            if len(parts) != 2:
                return "Erro: ID da tarefa não fornecido."
            try:
                task_id = int(parts[1])
                return self.complete_task(task_id)
            except ValueError:
                return "Erro: ID da tarefa deve ser um número."

        return "Comando desconhecido."
    
    def is_valid_date(self, date_str: str) -> bool:
        """Valida se a string está no formato de data YYYY-MM-DD."""
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def add_task(self, description: str, due_date: str = None) -> str:
        """Adiciona uma nova tarefa na AVL Tree com uma data de vencimento opcional."""
        with self.lock:  # Protege o acesso aos dados compartilhados
            task = {
                'id': self.next_id,  # ID único
                'description': description,
                'completed': False,  # Status da tarefa
                'due_date': due_date,  # Data de vencimento opcional
                'subtasks': []  # Lista de subtarefas
            }
            self.task_tree.insert(task)  # Insere o dicionário da tarefa na AVL Tree
            self.next_id += 1
            return f"Tarefa adicionada com sucesso. ID: {task['id']}"
    
    def add_subtask(self, task_id: int, description: str) -> str:
        """Adiciona uma subtarefa a uma tarefa existente."""
        with self.lock:  # Protege o acesso aos dados compartilhados
            task = self.task_tree.search(task_id)
            if task:
                subtask = {
                    'description': description,
                    'completed': False
                }
                task['subtasks'].append(subtask)  # Adiciona a subtarefa na lista de subtarefas
                return f"Subtarefa adicionada com sucesso à tarefa {task_id}."
            return f"Tarefa {task_id} não encontrada."

    def remove_task(self, task_id: int) -> str:
        """Remove uma tarefa pelo ID."""
        with self.lock:  # Protege o acesso aos dados compartilhados
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
    
    def complete_task(self, task_id: int) -> str:
        """Marca uma tarefa como concluída."""
        with self.lock:  # Protege o acesso aos dados compartilhados
            task = self.task_tree.search(task_id)
            if task:
                task['completed'] = True  # Marca a tarefa como concluída
                return f"Tarefa {task_id} marcada como concluída."
            return f"Tarefa {task_id} não encontrada."
    
    def list_uncompleted_tasks(self) -> str:
        """Lista apenas as tarefas que ainda não foram concluídas, incluindo a data de vencimento."""
        tasks = []
        self.task_tree.inorder(lambda node: tasks.append(node.value) if not node.value['completed'] else None)
        
        if not tasks:
            return "Nenhuma tarefa não concluída encontrada."
        
        task_list = "\n".join([f"ID: {task['id']}, Descrição: {task['description']}, Vencimento: {task['due_date'] or 'Sem vencimento'}, Concluída: {task['completed']}" for task in tasks])
        return f"Tarefas não concluídas:\n{task_list}"
    
    def list_detailed_uncompleted_tasks(self) -> str:
        """Lista as tarefas não concluídas com suas subtarefas (se houver)."""
        tasks = []
        self.task_tree.inorder(lambda node: tasks.append(node.value) if not node.value['completed'] else None)
        
        if not tasks:
            return "Nenhuma tarefa não concluída encontrada."
        
        task_list = ""
        for task in tasks:
            task_list += f"ID: {task['id']}, Descrição: {task['description']}, Vencimento: {task['due_date'] or 'Sem vencimento'}, Concluída: {task['completed']}\n"
            if task['subtasks']:
                task_list += "  Subtarefas:\n"
                for subtask in task['subtasks']:
                    task_list += f"    - Descrição: {subtask['description']}, Concluída: {subtask['completed']}\n"
            task_list += "\n"
        
        return f"Tarefas não concluídas (com subtarefas):\n{task_list}"

    def list_subtasks(self, task_id: int) -> str:
        """Lista todas as subtarefas de uma tarefa."""
        task = self.task_tree.search(task_id)
        if task:
            subtasks = task['subtasks']
            if not subtasks:
                return f"Tarefa {task_id} não possui subtarefas."
            subtask_list = "\n".join([f"Descrição: {subtask['description']}, Concluída: {subtask['completed']}" for subtask in subtasks])
            return f"Subtarefas da Tarefa {task_id}:\n{subtask_list}"
        return f"Tarefa {task_id} não encontrada."
    
    def task_history(self) -> str:
        """Lista todas as tarefas (concluídas e não concluídas)."""
        tasks = []
        self.task_tree.inorder(lambda node: tasks.append(node.value))
        
        if not tasks:
            return "Nenhuma tarefa encontrada."
        
        task_list = "\n".join([f"ID: {task['id']}, Descrição: {task['description']}, Concluída: {task['completed']}" for task in tasks])
        return f"Histórico de Tarefas:\n{task_list}"

if __name__ == '__main__':
    server = TaskServer()
    server.start()
