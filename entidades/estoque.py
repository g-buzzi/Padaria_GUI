from entidades.ingrediente import Ingrediente
from entidades.produto import Produto
from entidades.movimentacao import Movimentacao

class Estoque:
    def __init__(self):
        self.__balanco = 0
        self.__movimentacoes = []

    @property
    def balanco(self):
        return self.__balanco

    @property
    def movimentacoes(self):
        return self.__movimentacoes

    def compra(self, ingrediente: Ingrediente, quantidade: int):
        valor_total = ingrediente.preco_unitario * quantidade
        self.__movimentacoes.append(Movimentacao("Compra", ingrediente, quantidade, valor_total))
        self.__balanco -= valor_total
        ingrediente.quantidade_estoque += quantidade

    def producao(self, produto: Produto, quantidade: int):
        self.__movimentacoes.append(Movimentacao("Produção", produto, quantidade * produto.receita.rendimento, 0))
        for ingrediente, quantidade_ingrediente in produto.receita.ingredientes_receita.items():
            ingrediente.quantidade_estoque -= (quantidade * quantidade_ingrediente)
        produto.quantidade_estoque += quantidade * produto.receita.rendimento 

    def venda(self, produto: Produto, quantidade: int):
        if quantidade > produto.quantidade_estoque:
            raise ValueError
        valor_total = produto.preco_venda * quantidade
        self.__movimentacoes.append(Movimentacao("Venda", produto, quantidade, valor_total))
        produto.quantidade_estoque -= quantidade
        self.__balanco += valor_total

    def baixa(self, estocado, quantidade: int):
        self.__movimentacoes.append(Movimentacao("Baixa", estocado, quantidade, 0))
        estocado.quantidade_estoque -= quantidade