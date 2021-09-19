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
    __instancia = None

    def __new__(cls):
        if cls.__instancia is None:
            cls.__instancia = object.__new__(cls)
        return cls.__instancia

    def __init__(self):
        super().__init__(TelaCentral())

    def abre_tela_inicial(self):
        switcher = {
            "sair": quit, "ingredientes": ControladorIngredientes, 
            "receitas": ControladorReceitas, 
            "produtos": ControladorProdutos, 
            "estoque": ControladorEstoque, 
            "funcionarios": ControladorFuncionarios, 
            "clientes": ControladorClientes,
            "vendas": ControladorVendas
        }
        while True:
            botao, dados = self.tela.inicia()
            self.tela.close()
            if botao == "sair":
                quit()
            else:
                switcher[botao]().inicia()
