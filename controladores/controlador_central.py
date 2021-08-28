from controladores.controlador_abstrato import Controlador
from telas.tela_central import TelaCentral
from controladores.controlador_ingredientes import ControladorIngredientes


class ControladorCentral(Controlador):

    def __init__(self):
        super().__init__(TelaCentral(self))

    def abre_tela_inicial(self):
        switcher = {0: False, 1: ControladorIngredientes().inicia}
        while True:
            opcao = self.tela.mostra_opcoes()
            funcao_escolhida = switcher[opcao]

            if funcao_escolhida is False:
                break
            else:
                funcao_escolhida()


