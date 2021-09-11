from entidades.estocado import Estocado


class Ingrediente(Estocado):
    def __init__(self, codigo: int, nome: str, unidade_medida: str, preco_unitario: float):
        super().__init__(codigo, nome)
        self.__unidade_medida = unidade_medida
        self.__preco_unitario = preco_unitario

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