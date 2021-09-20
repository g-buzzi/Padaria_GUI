from DAOs.dao_abstrato import DAO
from entidades.receita import Receita
from DAOs.dao_produto import ProdutoDAO
from excecoes.not_found_exception import NotFoundException

class ReceitaDAO(DAO):
    __instancia = None

    def __new__(cls):
        if cls.__instancia is None:
            cls.__instancia = object.__new__(cls)
        return cls.__instancia

    def __init__(self):
        super().__init__("receitas.pkl")

    def add(self, receita: Receita):
        if (receita is not None and isinstance(receita, Receita)):
            super().add(receita.codigo, receita)

    def remove(self, receita: Receita):
        if isinstance(receita.codigo, int):
            super().remove(receita.codigo, "Receita")

    def get(self, codigo: int) -> Receita:
        if isinstance(codigo, int):
            return super().get(codigo, "Receita")


    def alter(self, receita: Receita, codigo_antigo: int):
        if isinstance(receita, Receita) and isinstance(codigo_antigo, int):
            super().alter(codigo_antigo, receita.codigo, receita)
            if receita.produto_associado is not False:
                ProdutoDAO().update_receita(receita.produto_associado, receita)

    def update_ingredientes(self, ingrediente, codigo_antigo: int):
        for receita in self._cache.values():
            for ingrediente_receita, quantidade in receita.ingredientes_receita.items():
                if ingrediente_receita.codigo == codigo_antigo:
                    receita.ingredientes_receita.pop(ingrediente_receita)
                    receita.ingredientes_receita[ingrediente] = quantidade
                    self._cache[receita.codigo] = receita
                    if receita.produto_associado is not False:
                        ProdutoDAO().update_receita(receita.produto_associado, receita)
                    break
        self._dump()

    def remove_ingrediente(self, codigo_ingrediente: int):
        for receita in self._cache.values():
            for ingrediente_receita in receita.ingredientes_receita.keys():
                if ingrediente_receita.codigo == codigo_ingrediente:
                    receita.ingredientes_receita.pop(ingrediente_receita)
                    if receita.produto_associado is not False:
                        ProdutoDAO().update_receita(receita.produto_associado, receita)
                    break
        self._dump()