# Sistema de Gerenciamento de Tarefas

## Autores:
- João Victor Alves de Paiva - paiva.joao@academico.ifpb.edu.br

## Disciplinas Envolvidas:
- Estrutura de Dados - Prof. Alex Sandro da Cunha Rêgo
- Protocolos de Interconexão de Redes - Prof. Leonidas Francisco de Lima Júnior

## Descrição do Problema:
Este projeto consiste no desenvolvimento de um sistema distribuído de gerenciamento de tarefas, utilizando uma arquitetura cliente-servidor com comunicação via **Sockets TCP**. O cliente pode adicionar, listar, pesquisar, remover e marcar tarefas como concluídas, além de gerenciar subtarefas. O servidor utiliza uma **árvore AVL** para organizar as tarefas, garantindo eficiência em operações como busca e inserção.

O sistema é capaz de atender múltiplos clientes simultaneamente, evitando condições de corrida através de **locks** de threads no servidor.

## Arquivos do Projeto:

| Arquivo                    | Descrição |
| --------------------------- | --------- |
| `client/client.py`           | Implementação do cliente que envia comandos ao servidor. Utiliza uma fila encadeada para gerenciar as mensagens. |
| `server/server.py`           | Implementação do servidor que processa os comandos dos clientes. Gerencia as tarefas utilizando uma árvore AVL. |
| `ds/queue.py`                | Implementação da estrutura de dados **Fila Encadeada** utilizada pelo cliente para gerenciar as mensagens. |
| `ds/avl_tree.py`             | Implementação da **Árvore AVL** utilizada pelo servidor para gerenciar as tarefas de forma balanceada. |
| `README.md`                  | Este arquivo de descrição do projeto. |

## Pré-requisitos para Execução:

Antes de executar o sistema, instale os seguintes pacotes/bibliotecas:

1. **Python 3.x** - A linguagem usada para implementar o sistema.
2. **Biblioteca `socket`** (interna no Python) - Para comunicação via Sockets.
3. **Biblioteca `threading`** (interna no Python) - Para manipulação de threads no servidor.
   
Não é necessário instalar pacotes externos adicionais, apenas certifique-se de que o Python 3.x esteja instalado no sistema.

## Protocolo da Aplicação:

A comunicação entre cliente e servidor é feita através de comandos de texto simples enviados via **Sockets TCP**. Cada comando pode ter parâmetros opcionais, dependendo da funcionalidade.

### Comandos Disponíveis:

- **ADD <descrição> [data de vencimento] [prioridade]**:
    - Adiciona uma nova tarefa. A prioridade pode ser `ALTA`, `MEDIA` ou `BAIXA` (padrão). A data deve ser no formato `YYYY-MM-DD`.
    - **Exemplo**: `ADD Estudar para a prova 2024-10-10 ALTA`
    - **Resposta**: `Tarefa adicionada com sucesso. ID: 1, Prioridade: ALTA`
    
- **ADD_SUBTASK <id> <descrição>**:
    - Adiciona uma subtarefa a uma tarefa existente.
    - **Exemplo**: `ADD_SUBTASK 1 Revisar notas`
    - **Resposta**: `Subtarefa adicionada com sucesso à tarefa 1.`
    
- **LIST**:
    - Lista todas as tarefas não concluídas, incluindo suas datas de vencimento e prioridades.
    - **Exemplo**: `LIST`
    - **Resposta**: `Tarefas não concluídas: ID: 1, Descrição: Estudar para a prova, Vencimento: 2024-10-10, Prioridade: ALTA, Concluída: False`.
    
- **LIST_DETAILED**:
    - Lista todas as tarefas não concluídas com suas subtarefas.
    - **Exemplo**: `LIST_DETAILED`
    - **Resposta**: `Tarefas não concluídas (com subtarefas):`
        `ID: 1, Descrição: Estudar para a prova, Vencimento: 2024-10-10, Concluída: False`
            `Subtarefas:`
                `- Descrição: Revisar notas, Concluída: False.`
    
- **TASK_HISTORY**:
    - Lista todas as tarefas, concluídas e não concluídas.
    - **Exemplo**: `TASK_HISTORY`
    - **Resposta**: `Histórico de Tarefas:`
        `ID: 1, Descrição: Estudar para a prova, Concluída: False`
        `ID: 2, Descrição: Ir para academia, Concluída: True.`
    
- **REMOVE <id>**:
    - Remove uma tarefa pelo ID.
    - **Exemplo**: `REMOVE 1`
    - **Resposta**: `Tarefa 1 removida com sucesso.`
    
- **SEARCH <id>**:
    - Busca uma tarefa pelo ID.
    - **Exemplo**: `SEARCH 1`
    - **Resposta**: `ID: 1, Descrição: Estudar para a prova, Vencimento: 2024-10-10, Concluída: False`
                        `Subtarefas:`
                            `- Descrição: Revisar notas, Concluída: False.`.
    
- **COMPLETE <id>**:
    - Marca uma tarefa como concluída.
    - **Exemplo**: `COMPLETE 1`
    - **Resposta**: `Tarefa 1 marcada como concluída.`

## Instruções para Execução:

### Executando o Servidor:
1. Navegue até a pasta `server`:
    ```bash
    cd server
    ```
2. Execute o servidor:
    ```bash
    python3 server.py
    ```

O servidor será iniciado e ficará aguardando conexões de clientes.

### Executando o Cliente:
1. Em uma nova janela de terminal, navegue até a pasta `client`:
    ```bash
    cd client
    ```
2. Execute o cliente:
    ```bash
    python3 client.py
    ```

O cliente se conectará ao servidor e solicitará comandos ao usuário. Basta digitar os comandos desejados conforme a seção de **Protocolo da Aplicação**.

### Exemplo de Fluxo de Execução:

1. O servidor é iniciado e aguarda conexões.
2. O cliente se conecta ao servidor e adiciona uma nova tarefa:
   - Comando: `ADD "Fazer compras" 2024-10-15 ALTA`
   - Resposta do servidor: `Tarefa adicionada com sucesso. ID: 1, Prioridade: ALTA`
3. O cliente lista as tarefas não concluídas:
   - Comando: `LIST`
   - Resposta do servidor: `ID: 1, Descrição: Fazer compras, Vencimento: 2024-10-15, Prioridade: ALTA, Concluída: False`

O servidor pode continuar respondendo a vários clientes simultaneamente, processando comandos de maneira eficiente graças ao uso de threads.