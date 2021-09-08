from controladores.controlador_abstrato import Controlador
from telas.tela_central import TelaCentral
from controladores.controlador_ingredientes import ControladorIngredientes
from controladores.controlador_receitas import ControladorReceitas
from controladores.controlador_produtos import ControladorProdutos
from controladores.controlador_estoque import ControladorEstoque
from controladores.controlador_funcionarios import ControladorFuncionarios
from controladores.controlador_clientes import ControladorClientes
from controladores.controlador_vendas import ControladorVendas


class ControladorCentral(Controlador):

    def __init__(self):
        super().__init__(TelaCentral())
        self.__controlador_ingredientes = ControladorIngredientes(self)
        self.__controlador_receitas = ControladorReceitas(self)
        self.__controlador_produtos = ControladorProdutos(self)
        self.__controlador_estoque = ControladorEstoque(self)
        self.__controlador_funcionarios = ControladorFuncionarios(self)
        self.__controlador_clientes = ControladorClientes(self)
        self.__controlador_vendas = ControladorVendas(self)


    def abre_tela_inicial(self):
        switcher = {
            "sair": quit, "ingredientes": self.controlador_ingredientes.inicia, 
            "receitas": self.controlador_receitas.inicia, 
            "produtos": self.controlador_produtos.inicia, 
            "estoque": self.controlador_estoque.inicia, 
            "funcionarios": self.controlador_funcionarios.inicia, 
            "clientes": self.controlador_clientes.inicia,
            "vendas": self.controlador_vendas.inicia
        }
        while True:
            botao, dados = self.tela.inicia()
            switcher[botao]()

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
      
    @property
    def controlador_vendas(self):
        return self.__controlador_vendas


