from controladores.controlador_abstrato import Controlador
from telas.tela_central import TelaCentral
from controladores.controlador_ingredientes import ControladorIngredientes
from controladores.controlador_receitas import ControladorReceitas
from controladores.controlador_produtos import ControladorProdutos
from controladores.controlador_estoque import ControladorEstoque
from controladores.controlador_funcionarios import ControladorFuncionarios
from controladores.controlador_clientes import ControladorClientes


class ControladorCentral(Controlador):

    def __init__(self):
        super().__init__(TelaCentral(self))
        self.__controlador_ingredientes = ControladorIngredientes(self)
        self.__controlador_receitas = ControladorReceitas(self)
        self.__controlador_produtos = ControladorProdutos(self)
        self.__controlador_estoque = ControladorEstoque(self)
        self.__controlador_funcionarios = ControladorFuncionarios(self)
        self.__controlador_clientes = ControladorClientes(self)
        
        self.__controladores = {
            0: False, 1: self.controlador_ingredientes, 
            2: self.controlador_receitas, 
            3: self.controlador_produtos, 
            4: self.controlador_estoque, 
            5: self.controlador_funcionarios, 
            6: self.controlador_clientes
        }

    def abre_tela_inicial(self):
        opcoes = {1: "Ingredientes", 2: "Receitas", 3: "Produtos", 4: "Estoque", 5: "Funcionários", 6: "Clientes", 0: "Sair"}
        while True:
            opcao = self.tela.mostra_opcoes(opcoes, "-------- Tela Inicial --------")
            controlador = self.__controladores[opcao]

            if controlador is False:
                break
            else:
                controlador.inicia()

    @property
    def controlador_ingredientes(self):
        return self.__controlador_ingredientes
    
    @property
    def controlador_receitas(self):
        return self.__controlador_receitas

    @property
    def controlador_produtos(self):
        return self.__controlador_produtos

    @property
    def controlador_estoque(self):
        return self.__controlador_estoque
    
    @property
    def controlador_funcionarios(self):
        return self.__controlador_funcionarios
    
    @property
    def controlador_clientes(self):
        return self.__controlador_clientes


