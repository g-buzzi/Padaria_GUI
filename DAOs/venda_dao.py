from DAOs.dao_abstrato import DAO
from entidades.venda import Venda


class VendaDao(DAO):

    def __init__(self):
        super().__init__('vendas.pkl')

    def add(self, venda: Venda):
        if isinstance(venda.codigo, int) and venda is not None and isinstance(venda, Venda):
            super().add(venda.codigo, venda)

    def get(self, key: int):
        if isinstance(key, int):
            return super().get(key)

    def remove(self, key: int):
        if isinstance(key, int):
            return super().remove(key)
