from entidades.produto import Produto

class Item():
    
    def __init__(self, produto: Produto, quantidade: int):
        self.__produto = produto
        self.__quantidade = quantidade
        
    @property
    def produto(self) -> Produto:
        return self.__produto
    
    @produto.setter
    def produto(self, produto):
        self.__produto = produto
    
    @property
    def quantidade(self) -> int:
        return self.__quantidade
    
    @quantidade.setter
    def quantidade(self, quantidade):
        self.__quantidade = quantidade

    
        