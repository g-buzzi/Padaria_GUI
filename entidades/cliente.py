from entidades.pessoa import Pessoa

class Cliente(Pessoa):

    def __init__(self, nome: str, cpf: str, telefone: int, email: str, endereco: str):
        super().__init__(nome, cpf, telefone, email)
        self.__endereco = endereco

    @property
    def endereco(self) -> str:
        return self.__endereco

    @endereco.setter
    def endereco(self, endereco):
        self.__endereco = endereco