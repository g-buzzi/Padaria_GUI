from abc import ABC, abstractmethod
from subprocess import check_call
from excecoes.EmptyField import EmptyFieldError
from excecoes.FloatError import FloatError
from excecoes.IntError import IntError
from telas.tela_abstrata import Tela


class Controlador(ABC):
    @abstractmethod
    def __init__(self, tela):
        self.__tela = tela

    @abstractmethod
    def abre_tela_inicial(self):
        pass

    def inicia(self):
        self.abre_tela_inicial()

    @property
    def tela(self):
        return self.__tela

    @tela.setter
    def tela(self, tela: Tela):
        self.__tela.close()
        self.__tela = tela

    def formata_int(self, valor: str, nome_campo: str) -> int:
        self.checar_vazio(valor)
        try:
            valor = int(valor)
            if valor < 0:
                raise ValueError()
            return valor
        except ValueError:
            raise IntError(nome_campo)

    def formata_float(self, valor: str, nome_campo: str, n_digitos = 2) -> float:
        self.checar_vazio(valor)
        try:
            valor = float(valor)
            valor = round(valor, n_digitos)
            if valor < 0:
                raise ValueError()
            return valor
        except ValueError:
            raise FloatError(nome_campo)

    def formata_string(self, valor: str) -> str:
        self.checar_vazio(valor)
        return valor.strip()

    def checar_vazio(self, valor: str):
        if valor is None or valor == "":
            raise EmptyFieldError()

