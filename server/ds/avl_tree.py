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
    
    def __searchData(self, key:any, node:Node)->Node:
        '''
        Private method that performs a recursive search in AVL Tree to find the node 
        whose key is equal to "key" argument.
        
        Arguments
        ------------
        key (any): the key value to be searched in AVL Tree
        node (Node): the node to be used as reference to start the search 
        Returns
        ----------
        None if the key was not found or AVL Tree is empty. Otherwise, returns
        the object/value stored at the node corresponding the key.
        '''
        if ( key == node.value):
            return node
        elif ( key < node.value and node.left != None):
            return self.__searchData( key, node.left())
        elif ( key > node.value and node.right != None):
            return self.__searchData( key, node.right)
        else:
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
  
    def __insert(self, root:Node, key:any):
        # Step 1 - Performs a BST recursion to add the node
        if not root: 
            return Node(key) 
        elif key < root.value: 
            root.left = self.__insert(root.left, key) 
        else: 
            root.right = self.__insert(root.right, key) 
  
        # Step 2 
        # The current node must be one of the ancestors of the newly inserted node.
        # Update the height of ancestor node
        root.height = 1 + max(self.__getHeight(root.left), 
                              self.__getHeight(root.right)) 
  
        # Step 3 - Computes the balance factor 
        # (left subtree height – right subtree height) of the current node
        balance = self.__getBalance(root) 
  
        # Step 4 - Checks if the node is unbalanced
        # Then, one of the following actions will be performed:

        # CASE 1 - Right rotation
        if balance > 1 and key < root.left.value: 
            return self.__rightRotate(root) 
  
        # CASE 2 - Left rotation
        if balance < -1 and key > root.right.value: 
            return self.__leftRotate(root) 
  
        # CASE 3 - Double rotation: Left-> Right 
        if balance > 1 and key > root.left.value: 
            root.left = self.__leftRotate(root.left) 
            return self.__rightRotate(root) 
  
        # CASE 4 - Double rotation: Right-> Left 
        if balance < -1 and key < root.right.value: 
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

    def inorder(self):
        '''
        Perform a in-order traversal in AVL Tree
        '''
        self.__inorder(self.__root)

    def __inorder(self, root): 
        if not root: 
            return
  
        self.__inorder(root.left) 
        print("{0} ".format(root.value), end="") 
        self.__inorder(root.right) 

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
        

    def __delete(self, root:Node, key:object)->Node: 
        """
        Recursive function to delete a node with given key from subtree
        with given root.

        Retorno
        --------------
        It returns root of the modified subtree.
        """
        # Step 1 - Perform standard BST delete 
        if not root: 
            return root   
        elif key < root.value: 
            root.left = self.__delete(root.left, key)   
        elif key > root.value: 
            root.right = self.__delete(root.right, key)   
        else: 
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
            root.right = self.__delete(root.right, 
                                      temp.value) 
  
        # If the tree has only one node, 
        # simply return it 
        if root is None: 
            return root 
  
        # Step 2 - Update the height of the  
        # ancestor node 
        root.height = 1 + max(self.__getHeight(root.left), 
                            self.__getHeight(root.right)) 
  
        # Step 3 - Get the balance factor 
        balance = self.__getBalance(root) 
  
        # Step 4 - If the node is unbalanced,  
        # then try out the 4 cases 
        # Case 1 - Left Left 
        if balance > 1 and self.__getBalance(root.left) >= 0: 
            return self.__rightRotate(root) 
  
        # Case 2 - Right Right 
        if balance < -1 and self.__getBalance(root.right) <= 0: 
            return self.__leftRotate(root) 
  
        # Case 3 - Left Right 
        if balance > 1 and self.__getBalance(root.left) < 0: 
            root.left = self.__leftRotate(root.left) 
            return self.__rightRotate(root) 
  
        # Case 4 - Right Left 
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
