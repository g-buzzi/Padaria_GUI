from datetime import datetime

class Movimentacao:
    def __init__(self, tipo: str, nome_produto: str, quantidade: int, valor_total: float):
        self.__data = datetime.now()
        self.__tipo = tipo
        self.__nome_produto = nome_produto
        self.__quantidade = quantidade
        self.__valor_total = valor_total

    @property
    def tipo(self):
        return self.__tipo

    @property
    def nome_produto(self):
        return self.__nome_produto

    @property
    def quantidade(self):
        return self.__quantidade

    @property
    def valor_total(self):
        return self.__valor_total

    @property
    def data(self):
        return self.__data