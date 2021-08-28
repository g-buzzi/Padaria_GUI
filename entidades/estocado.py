from abc import ABC, abstractmethod

class Estocado(ABC):
    @abstractmethod
    def __init__(self, nome: str) -> None:
        super().__init__()
        self.__nome = nome
        self.__quantidade_estoque = 0

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        self.__nome = nome

    @property
    def quantidade_estoque(self) -> int:
        return self.__quantidade_estoque

    @quantidade_estoque.setter
    def quantidade_estoque(self, quantidade_estoque: int):
        self.__quantidade_estoque = quantidade_estoque
    
