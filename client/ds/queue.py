class FilaError(Exception):
    def __init__(self, msg:str):
        super().__init__(msg)


class No:
    def __init__(self, carga:any):
        self.carga = carga
        self.proximo = None
    
    def __str__(self):
        return f'{self.carga}'


class Descritor:
    def __init__(self):
        self.inicio = self.final = None
        self.tamanho = 0


class Fila:
    '''
    Classe que implementa a estrutura de dados Pilha usando a 
    técnica sequencial
    '''
    def __init__(self):
        self.__head = Descritor()

    def __len__(self)->int:
        return self.__head.tamanho

    def esta_vazia(self):
        return self.__head.tamanho == 0

    def frente(self)->any:
        '''
        Método que retorna a carga armazenada na frente da fila
        '''
        if self.esta_vazia():
            raise FilaError('Fila está vazia')
        return self.__head.inicio.carga
    
    def elemento(self, posicao:int)->any:
        '''
        Método que recebe a posição de um elemento da pilha que deseja
        consultar. Retorna a carga armazenada na posição específica.
        A posicao retornada é em direição da base para o topo
        '''
        try:
            assert  0 < posicao <= len(self)
            cursor = self.__head.inicio
            for _ in range(len(self)-posicao):
                cursor = cursor.proximo
            return cursor.carga
        except AssertionError:
            raise FilaError(f'Posicao invalida. A fila no momento possui {len(self)} elementos.')

    def busca(self, chave:any)->int:
        '''
        Método que recebe uma chave de busca e retorna a posição em
        que a carga foi encontrada na pilha
        '''
        cursor = self.__head.inicio
        contador = 1
        while(cursor != None):
            if cursor.carga == chave:
                return contador
            cursor = cursor.proximo
            contador +=1
        raise FilaError(f"Chave {chave} não encontrada")

    def enfileira(self, carga:any):
        no = No(carga)
        if self.esta_vazia():
            self.__head.inicio = self.__head.final = no
        else: 
            self.__head.final.proximo = no
            self.__head.final= no
        self.__head.tamanho += 1
            
    def desenfileira(self)->any:
        if self.esta_vazia():
            raise FilaError('Fila está vazia')
        carga = self.__head.inicio.carga
        if len(self) == 1:
            self.__head.final = None
        else:
            self.__head.inicio =  self.__head.inicio.proximo
        self.__head.tamanho -= 1
        return carga
        
    def esvaziar(self):
        while not self.esta_vazia():
            self.desenfileira()

    def __str__(self)->str:
        s = 'inicio->[ '

        cursor = self.__head.inicio
        while( cursor != None):
            s += f'{cursor.carga}, '
            cursor = cursor.proximo

        s = s.strip(', ')
        s += ' ]<-fim'
        return s
    
     
    def combina(self, fila1:'Fila', fila2:'Fila' ):
        while( not fila1.esta_vazia() and not fila2.esta_vazia()):
            self.__enfileira(fila1.desenfileira())
            self.__enfileira(fila2.desenfileira())
        if (fila1.esta_vazia and not fila2.esta_vazia()):
            while( not fila2.esta_vazia()):
                self.__enfileira(fila2.desenfileira())
        if (not fila1.esta_vazia() and  fila2.esta_vazia()):
            while( not fila1.esta_vazia()):
                self.__enfileira(fila1.desenfileira())