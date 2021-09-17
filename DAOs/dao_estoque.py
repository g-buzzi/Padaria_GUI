from DAOs.dao_abstrato import DAO
from entidades.estoque import Estoque
from excecoes.not_found_exception import NotFoundException

class EstoqueDAO(DAO):
    instancia = None

    def __new__(cls):
        if EstoqueDAO.instancia is None:
            EstoqueDAO.instancia = super().__new__(cls)
        return EstoqueDAO.instancia
    
    def __init__(self) -> None:
        super().__init__(datasource="estoque.pkl")

    def add(self, estoque: Estoque):
        if (estoque is not None and isinstance(estoque, Estoque)):
            super().add("estoque", estoque)

    def remove(self):
        pass

    def get(self):
        try:
            return super().get("estoque")
        except KeyError:
            estoque = Estoque()
            super().add("estoque", estoque)
            return estoque