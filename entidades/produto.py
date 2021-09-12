from entidades.estocado import Estocado
from entidades.receita import Receita

class Produto(Estocado):
    def __init__(self, codigo: int, nome: str, preco_venda: float, descricao: str, receita: Receita = False):
        super().__init__(codigo, nome)
        self.__preco_venda = preco_venda
        self.__descricao = descricao
        self.__receita = receita

    @property
    def preco_venda(self) -> float:
        return self.__preco_venda

    @preco_venda.setter
    def preco_venda(self, preco_venda: float):
        self.__preco_venda = preco_venda

    @property
    def descricao(self) -> str:
        return self.__descricao

    @descricao.setter
    def descricao(self, descricao: str):
        self.__descricao = descricao

    @property
    def receita(self) -> Receita:
        return self.__receita

    @receita.setter
    def receita(self, receita: Receita):
        self.__receita = receita

    @property
    def custo_unitario(self) -> float:
        return self.__receita.custo_preparo/self.__receita.rendimento

    def remove_receita(self):
        self.__receita = False
