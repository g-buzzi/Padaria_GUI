from abc import ABC, abstractmethod


class Pessoa(ABC):

    @abstractmethod
    def __init__(self, nome: str, cpf: str, telefone: int, email: str):
        self.__nome = nome
        self.__cpf = cpf
        self.__telefone = telefone
        self.__email = email

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome):
        self.__nome = nome

    @property
    def cpf(self) -> str:
        return self.__cpf

    @cpf.setter
    def cpf(self, cpf):
        self.__cpf = cpf

    @property
    def telefone(self) -> int:
        return self.__telefone

    @telefone.setter
    def telefone(self, telefone):
        self.__telefone = telefone

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, email):
        self.__email = email
