from pessoa import Pessoa

class Cliente(Pessoa):

    def __init__(self, codigo: int, nome: str, cpf: str, telefone: int, email: str, endereco: str):
        super.__init__(nome, cpf, telefone, email)
        self.__codigo = codigo
        self.__endereco = endereco

    @property
    def codigo(self) -> int:
        return self.__codigo

    @codigo.setter
    def codigo(self, codigo):
        self.__codigo = codigo

    @property
    def endereco(self) -> str:
        return self.__endereco

    @endereco.setter
    def endereco(self, endereco):
        self.__endereco = endereco