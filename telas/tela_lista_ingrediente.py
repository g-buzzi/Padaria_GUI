import PySimpleGUI as sg
from telas.tela_abstrata import Tela

class TelaListaIngrediente(Tela):
    instancia = None

    def __new__(cls):
        if TelaListaIngrediente.instancia is None:
            TelaListaIngrediente.instancia = super().__new__(cls)
        return TelaListaIngrediente.instancia
    
    def __init__(self):
        super().__init__()

    def lista_ingredientes(self, dados_ingredientes = [], pesquisa = False):
        if pesquisa is not False:
            titulo = self.titulo("Pesquisa '" + pesquisa + "'")
            selecionado = ""
        else:
            titulo = self.titulo("Ingredientes")
            selecionado = "listar"
        botoes = {"Listar": "listar", "Cadastrar": "cadastrar", "Pesquisar": "pesquisar", "Voltar": "voltar"}
        opcoes = self.opcoes(botoes, selecionado = selecionado)
        lista = self.lista(["Código", "Nome", "Unidade de Medida", "Preço unitário"], dados_ingredientes, chave= "lista")
        layout = [[titulo], opcoes, [lista]]
        self.window = self.janela(layout = layout, background = "#FC9326")
        self.configura_lista("lista")
        return self.read()

    def seleciona_ingrediente(self, dados_ingredientes: list):
        lista =  self.lista(["Código", "Nome", "Unidade de Medida", "Preço unitário"], dados_ingredientes, chave= "lista")
        janela = self.popup([[lista]], "Selecionar ingrediente", keyboard_events= False)
        self.configura_lista(janela= janela)
        botao, values = janela.read(close = True)
        if botao is None:
            return None
        else:
            try:
                return values["lista"][0]
            except IndexError:
                return None
            