class Node:
    '''
    Class that models a dinamic node of a binary tree.
    '''
    def __init__(self,value:object):
        '''
        Constructor that initializes a node with a data and
        without children.'''
        self.__value = value
        self.__left = None
        self.__right = None
        # attribute that specifies the height (balance factor of the node)
        self.__height = 1

    @property
    def value(self)->object:
        return self.__value

    @value.setter
    def value(self, newValue:object):
        self.__value = newValue

    @property
    def left(self)->'Node':
        return self.__left

    @left.setter
    def left(self, newLeftChild:object):
        self.__left = newLeftChild

    @property
    def right(self)->'Node':
        return self.__right

    @right.setter
    def right(self, newRightChild:'Node'):
        self.__right = newRightChild

    @property
    def height(self)->int:
        return self.__height

    @height.setter
    def height(self, newHeight:int):
        self.__height = newHeight

    def insertLeft(self, data:object):
        if self.__left == None:
            self.__left = Node(data)	

    def hasLeftChild(self)->bool:
        return self.__left != None

    def hasRightChild(self)->bool:
        return self.__right != None

    def insertRight(self,data:object):
        if self.__right == None:
            self.__right = Node(data)

    def __str__(self):
        #return f'{self.__data}'
        return f'|{self.__value}:h={self.__height}|'
    

  
# Classe AVL tree 
class AVLTree(object): 
    def __init__(self, value:object = None):
        """ 
        Constructor of the AVL tree object
        Arguments
        ----------------
        value (object): data to be added to AVL tree. If a value
                        is not provided, the tree initializes "empty".
                        Otherwise, a node with "value" is created as root.
        """
        self.__root = None if value is None else self.insert(value)


    def getRoot(self)->any:
        '''
        Method that returns the object/value stored on root node.
        Returns
        ------------
        None if there is no root node, otherwise, returns the object/value stored
        on root node
        '''
        return None if self.__root is None else self.__root.value

    def isEmpty(self)->bool:
        '''
        Method that verifies AVL Tree is empty or not.
        Returns
        ---------
        True: AVL Tree is empty
        False: AVL Tree is not empty, i.e., there is at least a root node.
        '''
        return self.__root == None

    def search(self, key:any )->any:
        '''
        Perform a search in AVL Tree to find the node whose key is equal to "key" argument.
        Returns
        ----------
        None if the key was not found or AVL Tree is empty. Otherwise, returns
        the object/value stored at the corresponding key node.
        '''
        if( self.__root != None ):
           node = self.__searchData(key, self.__root)
           return node.value if node is not None else None
        else:
            return None

    def __searchData(self, key: any, node: Node) -> Node:
        """
        Método privado que realiza a busca recursiva na AVL Tree para encontrar o nó
        cujo valor seja igual à chave (key).
        """
        if node is None:
            return None
        
        # Comparação usando o 'id' do valor do nó
        if key == node.value['id']:
            return node
        elif key < node.value['id'] and node.left is not None:
            return self.__searchData(key, node.left)
        elif key > node.value['id'] and node.right is not None:
            return self.__searchData(key, node.right)
        
        return None

    def __len__(self)->int:
        '''Method that returns the number of nodes of this AVL tree
        Returns
        -------------
        int: the number of nodes of the tree.
        '''
        return self.__count(self.__root)

    def __count(self, node:Node)->int:
        if ( node == None):
            return 0
        else:
            return 1 + self.__count(node.left) + self.__count(node.right)


    def insert(self, key:object):
        '''
        Insert a new node in AVL Tree recursively from root.
        AVL tree is a self-balancing Binary Search Tree (BST) where the 
        difference between heights of left and right subtrees cannot be 
        more than one for all nodes.
        The given tree remains AVL after every insertion after re-balancing.

        Parameters
        ----------
        data (any): the data to be stored in the new node.
        '''
        if(self.__root == None):
            self.__root = Node(key)
        else:
            self.__root = self.__insert(self.__root, key)
  
    def __insert(self, root: Node, task: dict):
        """
        Método interno de inserção que compara os ids das tarefas.
        """
        key = task['id']  # Comparar usando o ID da tarefa
        
        if not root:
            return Node(task)  # Insere a tarefa como um nó da AVL
        
        # Comparação usando o 'id' da tarefa
        if key < root.value['id']:  # Usamos o ID da tarefa para comparação
            root.left = self.__insert(root.left, task)
        else:
            root.right = self.__insert(root.right, task)
        
        # Atualiza a altura e balanceia a árvore como antes
        root.height = 1 + max(self.__getHeight(root.left), self.__getHeight(root.right))
        balance = self.__getBalance(root)
        
        # Realiza rotações, se necessário
        if balance > 1 and key < root.left.value['id']:
            return self.__rightRotate(root)
        
        if balance < -1 and key > root.right.value['id']:
            return self.__leftRotate(root)
        
        if balance > 1 and key > root.left.value['id']:
            root.left = self.__leftRotate(root.left)
            return self.__rightRotate(root)
        
        if balance < -1 and key < root.right.value['id']:
            root.right = self.__rightRotate(root.right)
            return self.__leftRotate(root)
        
        return root
  
    def __leftRotate(self, p:Node)->Node: 
        """
        Realiza a rotação 'à esquerda' tomando o no 'p' como base
        para tornar 'u' como nova raiz        
        """
 
        u = p.right 
        T2 = u.left 
  
        # Perform rotation 
        u.left = p 
        p.right = T2 
  
        # Update heights 
        p.height = 1 + max(self.__getHeight(p.left), 
                         self.__getHeight(p.right)) 
        u.height = 1 + max(self.__getHeight(u.left), 
                         self.__getHeight(u.right)) 
  
        # Return the new root "u" node 
        return u 
  
    def __rightRotate(self, p:Node)->Node: 
        """ Realiza a rotação à direita tomando o no "p" como base
            para tornar "u" como nova raiz
        """
  
        u = p.left 
        T2 = u.right 
  
        # Perform rotation 
        u.right = p 
        p.left = T2 
  
        # Update heights 
        p.height = 1 + max(self.__getHeight(p.left), 
                        self.__getHeight(p.right)) 
        u.height = 1 + max(self.__getHeight(u.left), 
                        self.__getHeight(u.right)) 
  
        # Return the new root ("u" node)
        return u 
  
    def __getHeight(self, node:Node)->int: 
        """ Obtém a altura relativa ao nó passado como argumento
            Argumentos:
            -----------
            node (Node): o nó da árvore no qual se deseja consultar a altura
            
            Retorno
            -----------
            Retorna um número inteiro representando a altura da árvore
            representada pelo nó "node". O valor 0 significa que o "node"
            não é um objeto em memória
        """
        if node is None: 
            return 0
  
        return node.height 
  
    def __getBalance(self, node:Node)->int: 
        """
        Calcula o valor de balanceamento do nó passado como argumento.

        Argumentos:
        -----------
        node (object): o nó da árvore no qual se deseja determinar o 
                       balanceamento
            
        Retorno
        -----------
        Retorna o fator de balanceamento do nó em questão.
        Um valor 0, +1 ou -1 indica que o nó está balanceado
        """
        if not node: 
            return 0
  
        return self.__getHeight(node.left) - self.__getHeight(node.right) 

    def __getMinValueNode(self, root:Node)->Node:
        """
        Método que obtem o nó de menor valor a partir do 'root'
        passado como argumento (nó mais à esquerda)
        """
        if root is None or root.left is None:
            return root
 
        return self.__getMinValueNode(root.left)
    
    def __getMaxValueNode(self, root:Node)->Node:
        """
        Método que obtem o nó de maior valor a partir do 'root'
        passado como argumento (nó mais à direita)
        """
        if root is None or root.right is None:
            return root
 
        return self.__getMaxValueNode(root.right)  
    
    def preorder(self):
        '''
        Perform a pre-order traversal in AVL Tree
        '''
        self.__preorder(self.__root)

    def __preorder(self, root): 
        if not root: 
            return
  
        print("{0} ".format(root.value), end="") 
        self.__preorder(root.left) 
        self.__preorder(root.right) 

    def inorder(self, visit_callback):
        """ Faz a travessia in-order da árvore e executa o callback para cada nó visitado. """
        self.__inorder(self.__root, visit_callback)

    def __inorder(self, root, visit_callback):
        if not root:
            return
        self.__inorder(root.left, visit_callback)
        visit_callback(root)  # Executa o callback passando o nó atual
        self.__inorder(root.right, visit_callback)

    def posorder(self):
        '''
        Perform a pos-order traversal in AVL Tree
        '''
        self.__posorder(self.__root)

    def __posorder(self, root): 
        if not root: 
            return
  
        self.__posorder(root.left) 
        self.__posorder(root.right) 
        print("{0} ".format(root.value), end="") 


    def delete(self, key:object):
        '''
        Perform a delete operation of the specified key in AVL Tree
        Arguments  
        ------------
        key (object): the key value to be deleted from AVL Tree
        '''
        if(self.__root is not None):
            self.__root = self.__delete(self.__root, key)
        
    def __delete(self, root: Node, key: any) -> Node:
        """
        Função recursiva para deletar um nó com a chave fornecida (ID da tarefa) da subárvore
        com a raiz fornecida.
        """
        if not root:
            return root
        
        # Comparação usando o 'id' do valor do nó
        if key < root.value['id']:
            root.left = self.__delete(root.left, key)
        elif key > root.value['id']:
            root.right = self.__delete(root.right, key)
        else:
            # Nó encontrado. Proceder com a remoção.
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp
            
            temp = self.__getMinValueNode(root.right)
            root.value = temp.value
            root.right = self.__delete(root.right, temp.value['id'])
        
        if root is None:
            return root
        
        # Atualiza a altura do nó atual
        root.height = 1 + max(self.__getHeight(root.left), self.__getHeight(root.right))
        
        # Obtém o fator de balanceamento e realiza rotações, se necessário
        balance = self.__getBalance(root)
        
        if balance > 1 and self.__getBalance(root.left) >= 0:
            return self.__rightRotate(root)
        
        if balance < -1 and self.__getBalance(root.right) <= 0:
            return self.__leftRotate(root)
        
        if balance > 1 and self.__getBalance(root.left) < 0:
            root.left = self.__leftRotate(root.left)
            return self.__rightRotate(root)
        
        if balance < -1 and self.__getBalance(root.right) > 0:
            root.right = self.__rightRotate(root.right)
            return self.__leftRotate(root)
        
        return root
    
    def __str__(self):
        '''
        Returns a string representation of the AVL Tree
        '''
        return self.__strPreOrder(self.__root)
    
    def __strPreOrder(self, root:Node)->str:
        if root is None:
            return ''
        else:
            return f'{root} {self.__strPreOrder(root.left)} {self.__strPreOrder(root.right)}'
