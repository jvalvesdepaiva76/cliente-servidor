# File: server/server.py
import socket
import threading
from ds.avl_tree import AVLTree
from datetime import datetime

class TaskServer:
    """
    Classe responsável por gerenciar a comunicação com os clientes e o armazenamento das tarefas
    em uma árvore AVL (balanceada) para garantir eficiência nas operações.
    """
    
    def __init__(self, host: str = 'localhost', port: int = 12345) -> None:
        """
        Inicializa o servidor com o endereço e a porta especificados, além de configurar a árvore AVL 
        e um mecanismo de lock para threads.

        Args:
        host (str): Endereço do servidor. Padrão é 'localhost'.
        port (int): Porta para comunicação. Padrão é 12345.
        """
        self.host = host
        self.port = port
        self.task_tree = AVLTree()  # AVL Tree para gerenciar tarefas
        self.next_id = 1  # Para gerar IDs únicos para as tarefas
        self.lock = threading.Lock()  # Lock para proteger o acesso a dados compartilhados
    
    def start(self) -> None:
        """
        Inicia o servidor socket, aceita conexões de clientes e cria uma nova thread para cada cliente.
        O servidor escuta na porta especificada e trata múltiplos clientes simultaneamente.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.host, self.port))
            server_socket.listen()
            print(f"Servidor iniciado em {self.host}:{self.port}")

            while True:
                conn, addr = server_socket.accept()
                print(f"Conectado a {addr}")
                client_thread = threading.Thread(target=self.handle_client, args=(conn,))
                client_thread.start()
    
    def handle_client(self, conn: socket.socket) -> None:
        """
        Lida com a comunicação com o cliente, recebendo comandos, processando-os e enviando respostas.

        Args:
        conn (socket.socket): O socket de conexão com o cliente.
        """
        with conn:
            while True:
                try:
                    data = conn.recv(1024)
                    if not data:
                        break
                    response = self.process_command(data.decode())
                    conn.sendall(response.encode())
                except Exception as e:
                    conn.sendall(f"Erro no servidor: {str(e)}".encode())
                    break

    def process_command(self, command: str) -> str:
        """
        Processa os comandos recebidos do cliente.
        Comandos disponíveis:
        - ADD <descrição> [data de vencimento (opcional)] [prioridade (opcional)]: Adiciona uma nova tarefa com uma data e/ou prioridade.
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
            
            description = ' '.join(parts[1:])  # Assume inicialmente que tudo é descrição
            due_date = None
            priority = None

            # Verifica se o último item é prioridade
            if parts[-1].upper() in ["ALTA", "MEDIA", "BAIXA"]:
                priority = parts[-1].upper()
                description = ' '.join(parts[1:-1])  # Remove a prioridade da descrição

            # Verifica se o penúltimo item é uma data válida, considerando também a presença de prioridade
            if len(parts) > 2 and self.is_valid_date(parts[-2]):
                due_date = parts[-2]
                if priority:
                    description = ' '.join(parts[1:-2])  # Remove data e prioridade da descrição
                else:
                    description = ' '.join(parts[1:-1])  # Remove apenas a data

            # Verifica se há apenas uma data (e não prioridade)
            elif self.is_valid_date(parts[-1]):
                due_date = parts[-1]
                description = ' '.join(parts[1:-1])  # Remove a data da descrição

            return self.add_task(description, due_date, priority)

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
        """
        Verifica se uma string está no formato de data YYYY-MM-DD.

        Args:
        date_str (str): A string que representa a data.

        Returns:
        bool: True se a data for válida, False caso contrário.
        """
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def add_task(self, description: str, due_date: str = None, priority: str = None) -> str:
        """
        Adiciona uma nova tarefa na árvore AVL com data de vencimento e prioridade opcionais.

        Args:
        description (str): A descrição da tarefa.
        due_date (str, optional): A data de vencimento da tarefa.
        priority (str, optional): A prioridade da tarefa ('ALTA', 'MEDIA', 'BAIXA').

        Returns:
        str: Confirmação da adição da tarefa.
        """
        with self.lock:
            task = {
                'id': self.next_id,
                'description': description,
                'completed': False,
                'due_date': due_date,
                'priority': priority or 'BAIXA',
                'subtasks': []
            }
            self.task_tree.insert(task)
            self.next_id += 1
            return f"Tarefa adicionada com sucesso. ID: {task['id']}, Prioridade: {task['priority']}"
    
    def add_subtask(self, task_id: int, description: str) -> str:
        """
        Adiciona uma subtarefa a uma tarefa existente.

        Args:
        task_id (int): O ID da tarefa à qual a subtarefa será adicionada.
        description (str): A descrição da subtarefa.

        Returns:
        str: Confirmação da adição da subtarefa ou erro se a tarefa não for encontrada.
        """
        with self.lock:
            task = self.task_tree.search(task_id)
            if task:
                subtask = {
                    'description': description,
                    'completed': False
                }
                task['subtasks'].append(subtask)
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
        """
        Busca uma tarefa pelo ID e exibe suas subtarefas (se houver).

        Args:
        task_id (int): O ID da tarefa a ser buscada.

        Returns:
        str: Detalhes da tarefa e suas subtarefas, ou uma mensagem de erro se a tarefa não for encontrada.
        """
        task = self.task_tree.search(task_id)
        if task:
            result = f"ID: {task['id']}, Descrição: {task['description']}, Concluída: {task['completed']}, Vencimento: {task['due_date'] or 'Sem vencimento'}, Prioridade: {task['priority']}\n"
            
            # Verifica se a tarefa possui subtarefas
            if task['subtasks']:
                result += "Subtarefas:\n"
                for subtask in task['subtasks']:
                    result += f"  - Descrição: {subtask['description']}, Concluída: {subtask['completed']}\n"
            else:
                result += "Nenhuma subtarefa encontrada.\n"
            
            return result
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
        """Lista apenas as tarefas que ainda não foram concluídas, incluindo a data de vencimento e a prioridade."""
        tasks = []
        self.task_tree.inorder(lambda node: tasks.append(node.value) if not node.value['completed'] else None)
        
        if not tasks:
            return "Nenhuma tarefa não concluída encontrada."
        
        task_list = "\n".join([f"ID: {task['id']}, Descrição: {task['description']}, Vencimento: {task['due_date'] or 'Sem vencimento'}, Prioridade: {task['priority']}, Concluída: {task['completed']}" for task in tasks])
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
