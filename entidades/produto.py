from entidades.estocado import Estocado
from entidades.receita import Receita

class Produto(Estocado):
    def __init__(self, codigo: int, nome: str, preco_venda: float, descricao: str, receita: Receita):
        super().__init__(nome)
        self.__codigo = codigo
        self.__preco_venda = preco_venda
        self.__descricao = descricao
        self.__receita = receita

    @property
    def codigo(self) -> int:
        return self.__codigo
    
    @codigo.setter
    def codigo(self, codigo: int):
        self.__codigo = codigo

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
        if self.__receita is not False:
            self.__receita.remove_produto_associado()
        self.__receita = receita
        self.__receita.produto_associado = self

    @property
    def custo_unitario(self) -> float:
        return self.__receita.custo_preparo/self.__receita.rendimento

    def remove_receita(self):
        self.__receita = False