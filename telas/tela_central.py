from tkinter.constants import CENTER
from entidades import ingrediente
from telas.tela_abstrata import Tela


class TelaCentral(Tela):
    instancia = None

    def __new__(cls):
        if TelaCentral.instancia is None:
            TelaCentral.instancia = super().__new__(cls)
        return TelaCentral.instancia

    def __init__(self):
        super().__init__()

    def inicia(self):
        botoes = {"Vendas": "vendas","Ingredientes": "ingredientes", "Receitas": "receitas",
                  "Produtos": "produtos", "Estoque": "estoque", "Funcionário": "funcionarios",
                  "Clientes": 'clientes', "Sair": "sair"}
        titulo = self.titulo("Menu")
        menu = self.menu(botoes)
        layout = [[titulo],
                    menu]
        self.window = self.janela(layout, justificacao= CENTER)
        return self.read()

