class Ingrediente:
    def __init__(self, nome: str, unidade_medida: str, preco_unitario: float):
        self.__nome = nome
        self.__unidade_medida = unidade_medida
        self.__preco_unitario = preco_unitario
        self.__quantidade_estoque = 0

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        self.__nome = nome

    @property
    def unidade_medida(self) -> str:
        return self.__unidade_medida

    @unidade_medida.setter
    def unidade_medida(self, unidade_medida: str):
        self.__unidade_medida = unidade_medida

    @property
    def preco_unitario(self) -> float:
        return self.__preco_unitario

    @preco_unitario.setter
    def preco_unitario(self, preco_unitario: float):
        self.__preco_unitario = preco_unitario

    @property
    def quantidade_estoque(self) -> int:
        return self.__quantidade_estoque

    @quantidade_estoque.setter
    def quantidade_estoque(self, quantidade_estoque: int):
        self.__quantidade_estoque = quantidade_estoque
