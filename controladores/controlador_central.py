from controladores.controlador_abstrato import Controlador
from telas.tela_central import TelaCentral
from controladores.controlador_ingredientes import ControladorIngredientes
from controladores.controlador_receitas import ControladorReceitas
from controladores.controlador_produtos import ControladorProdutos
from controladores.controlador_estoque import ControladorEstoque
from controladores.controlador_funcionario import ControladorFuncionario


class ControladorCentral(Controlador):

    def __init__(self):
        super().__init__(TelaCentral(self))
        self.__controladores = {0: False, 1: ControladorIngredientes(self), 2: ControladorReceitas(self), 3: ControladorProdutos(self), 4: ControladorEstoque(self), 5: ControladorFuncionario(self)}

    def abre_tela_inicial(self):
        opcoes = {1: "Ingredientes", 2: "Receitas", 3: "Produtos", 4: "Estoque", 5: "Funcionário", 0: "Sair"}
        while True:
            opcao = self.tela.mostra_opcoes(opcoes, "-------- Tela Inicial --------")
            controlador = self.__controladores[opcao]

            if controlador is False:
                break
            else:
                controlador.inicia()

    @property
    def controlador_ingredientes(self):
        return self.__controladores[1]
    
    @property
    def controlador_receitas(self):
        return self.__controladores[2]

    @property
    def controlador_produtos(self):
        return self.__controladores[3]

    @property
    def controlador_estoque(self):
        return self.__controladores[4]

