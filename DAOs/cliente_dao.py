from DAOs.dao_abstrato import DAO
from entidades.cliente import Cliente


class ClienteDao(DAO):

    def __init__(self):
        super().__init__('clientes.pkl')

    def add(self, cliente: Cliente):
        if isinstance(cliente.cpf, str) and cliente is not None and isinstance(cliente, Cliente):
            super().add(cliente.cpf, cliente)

    def get(self, key: str):
        if isinstance(key, str):
            return super().get(key)

    def remove(self, key: str):
        if isinstance(key, str):
            return super().remove(key)

    def update(self, cpf_antigo: str, dado_novo_cliente: Cliente):
        if isinstance(dado_novo_cliente, Cliente) and isinstance(cpf_antigo, str):
            super().alter(cpf_antigo, dado_novo_cliente.cpf, dado_novo_cliente)
