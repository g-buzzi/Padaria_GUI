from abc import ABC, abstractmethod
from telas.tela_abstrata import Tela

class Controlador(ABC):
    @abstractmethod
    def __init__(self, tela: Tela):
        self.__tela = tela

    @abstractmethod
    def abre_tela_inicial(self, switcher: dict):
        while True:
            opcao = self.__tela.mostra_opcoes()
            funcao_escolhida = switcher[opcao]
            funcao_escolhida()

    def inicia(self):
        self.abre_tela_inicial()

    @property
    def tela(self):
        return self.__tela

    @tela.setter
    def tela(self, tela: Tela):
        self.__tela = Tela

    

