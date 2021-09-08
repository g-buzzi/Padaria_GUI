from abc import ABC, abstractmethod
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

    

