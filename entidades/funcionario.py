from pessoa import Pessoa

class Funcionario(Pessoa):

    def __init__(self, matrícula: int, nome: str, cpf: str, telefone: int, email: str, salario: float):
        super.__init__(nome, cpf, telefone, email)
        self.__matricula = matrícula
        self.__salario = salario

    @property
    def matricula(self) -> int:
        return self.__matricula

    @matricula.setter
    def matricula(self, matricula):
        self.__matricula = matricula

    @property
    def salario(self) -> float:
        return self.__salario

    @salario.setter
    def salario(self, salario):
        self.__salario = salario