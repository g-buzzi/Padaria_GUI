from DAOs.dao_abstrato import DAO
from entidades.produto import Produto
from excecoes.not_found_exception import NotFoundException

class ProdutoDAO(DAO):
    instancia = None

    def __new__(cls):
        if ProdutoDAO.instancia is None:
            ProdutoDAO.instancia = super().__new__(cls)
        return ProdutoDAO.instancia
    
    def __init__(self) -> None:
        super().__init__(datasource="produtos.pkl")

    def add(self, produto: Produto):
        if (produto is not None and isinstance(produto, Produto)):
            super().add(produto.codigo, produto)

    def remove(self, produto: Produto):
        if isinstance(produto.codigo, int):
            try:
                super().remove(produto.codigo)
            except KeyError:
                raise NotFoundException("Produto")

    def get(self, codigo: int):
        if isinstance(codigo, int):
            try:
                produto = super().get(codigo)
                return produto
            except KeyError:
                raise NotFoundException("Produto")

    def alter(self, produto: Produto, codigo_antigo):
        if isinstance(produto, Produto) and isinstance(codigo_antigo, int):
            super().alter(codigo_antigo, produto.codigo, produto)

    def update_receita(self, produto: Produto, receita):
        produto = self._cache[produto.codigo]
        produto.receita = receita
        self.add(produto)