from datetime import datetime

class Movimentacao:
    def __init__(self, tipo: str, movimentado, quantidade: int, valor_total: float):
        self.__data = datetime.now()
        self.__tipo = tipo
        self.__movimentado = movimentado
        self.__quantidade = quantidade
        self.__valor_total = valor_total

    @property
    def tipo(self):
        return self.__tipo

    @property
    def movimentado(self):
        return self.__movimentado

    @property
    def quantidade(self):
        return self.__quantidade

    @property
    def valor_total(self):
        return self.__valor_total

    @property
    def data(self):
        return self.__data