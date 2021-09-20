from DAOs.dao_abstrato import DAO
from entidades.produto import Produto
import DAOs.dao_ingrediente
from excecoes.not_found_exception import NotFoundException

class ProdutoDAO(DAO):
    __instancia = None

    def __new__(cls):
        if cls.__instancia is None:
            cls.__instancia = object.__new__(cls)
        return cls.__instancia
    
    def __init__(self) -> None:
        super().__init__(datasource="produtos.pkl")

    def add(self, produto: Produto):
        if (produto is not None and isinstance(produto, Produto)):
            super().add(produto.codigo, produto)

    def remove(self, produto: Produto):
        if isinstance(produto.codigo, int):
            super().remove(produto.codigo, "Produto")

    def get(self, codigo: int):
        if isinstance(codigo, int):
            return super().get(codigo, "Produto")

    def alter(self, produto: Produto, codigo_antigo):
        if isinstance(produto, Produto) and isinstance(codigo_antigo, int):
            super().alter(codigo_antigo, produto.codigo, produto)

    def update_receita(self, produto: Produto, receita):
        produto = self._cache[produto.codigo]
        produto.receita = receita
        self.add(produto)

    def producao(self, produto: Produto):
        self.add(produto)
        for ingrediente in produto.receita.ingredientes_receita.keys():
            DAOs.dao_ingrediente.IngredienteDAO().alter(ingrediente, ingrediente.codigo)