from DAOs.dao_abstrato import DAO
from entidades.movimentacao import Movimentacao
from excecoes.not_found_exception import NotFoundException

class MovimentacaoDAO(DAO):
    instancia = None

    def __new__(cls):
        if MovimentacaoDAO.instancia is None:
            MovimentacaoDAO.instancia = super().__new__(cls)
        return MovimentacaoDAO.instancia
    
    def __init__(self) -> None:
        super().__init__(datasource="movimentacoes.pkl")

    def add(self, movimentacao: Movimentacao):
        if (movimentacao is not None and isinstance(movimentacao, Movimentacao)):
            super().add(movimentacao.codigo, movimentacao)

    def remove(self, movimentacao: Movimentacao):
        if isinstance(movimentacao.codigo, int):
            try:
                super().remove(movimentacao.codigo)
            except KeyError:
                raise NotFoundException("Movimentação")

    def get(self, codigo: int):
        if isinstance(codigo, int):
            try:
                return super().get(codigo)
            except KeyError:
                raise NotFoundException("Movimentação")