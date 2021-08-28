from controladores.controlador_abstrato import Controlador
from telas.tela_central import TelaCentral
from controladores.controlador_ingredientes import ControladorIngredientes
from controladores.controlador_receitas import ControladorReceitas
from controladores.controlador_produtos import ControladorProdutos
from controladores.controlador_estoque import ControladorEstoque
from controladores.controlador_funcionario import ControladorFuncionario
from controladores.controlador_cliente import ControladorCliente


class ControladorCentral(Controlador):

    def __init__(self):
        super().__init__(TelaCentral(self))
        self.__controlador_ingrediente = ControladorIngredientes(self)
        self.__controlador_receita = ControladorReceitas(self)
        self.__controlador_produto = ControladorProdutos(self)
        self.__controlador_estoque = ControladorEstoque(self)
        self.__controlador_funcionario = ControladorFuncionario(self)
        self.__controlador_cliente = ControladorCliente(self)
        
        self.__controladores = {
            0: False, 1: self.controlador_ingrediente, 
            2: self.controlador_receita, 
            3: self.controlador_produto, 
            4: self.controlador_estoque, 
            5: self.controlador_funcionario, 
            6: self.controlador_cliente
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
    def controlador_ingrediente(self):
        return self.__controlador_ingrediente
    
    @property
    def controlador_receita(self):
        return self.__controlador_receita

    @property
    def controlador_produto(self):
        return self.__controlador_produto

    @property
    def controlador_estoque(self):
        return self.__controlador_estoque
    
    @property
    def controlador_funcionario(self):
        return self.__controlador_funcionario
    
    @property
    def controlador_cliente(self):
        return self.__controlador_cliente


