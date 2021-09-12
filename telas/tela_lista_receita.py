from PySimpleGUI.PySimpleGUI import popup_error
from telas.tela_abstrata import Tela

class TelaListaReceita(Tela):
    instancia = None

    def __new__(cls):
        if TelaListaReceita.instancia is None:
            TelaListaReceita.instancia = super().__new__(cls)
        return TelaListaReceita.instancia

    def __init__(self):
        super().__init__()

    def lista_receitas(self, dados: list, pesquisa = False):
        if pesquisa is not False:
            titulo = self.titulo("Pesquisa '" + pesquisa[1] + "'")
            selecionado = ""
        else:
            titulo = self.titulo("Receitas")
            selecionado = "listar"
        botoes = {"Listar": "listar", "Cadastrar": "cadastrar", "Pesquisar": "pesquisar", "Voltar": "voltar"}
        opcoes = self.opcoes(botoes, selecionado)
        lista = self.lista(["Código", "Produto", "Tempo de Preparo", "Rendimento"], dados)
        layout = [[titulo], opcoes, [lista]]
        self.window = self.janela(layout)
        self.configura_lista()
        return self.read()

    def seleciona_receita(self, dados:list):
        lista = self.lista(["Código", "Produto", "Tempo de Preparo", "Rendimento"], dados)
        janela = self.popup([[lista]], "Selecionar receita", keyboard_events= False)
        self.configura_lista(janela= janela)
        botao, values = janela.read(close = True)
        if botao is None:
            return None
        else:
            try:
                return values["lista"][0]
            except IndexError:
                return None


    def pesquisa_receita(self, codigo_ingrediente = ""):
        titulo = self.titulo("Pesquisa")
        lb_codigo_ingrediente = self.label("Código do ingrediente:")
        in_codigo_ingrediente = self.entrada("codigo_ingrediente", codigo_ingrediente,  tamanho=(20, 1), padding = ((1,0), 2))
        bt_codigo_ingrediente = self.botao("Selecionar", "seleciona_ingrediente", tamanho=(10,1), padding=((10,1), 2))
        bt_pesquisar = self.botao("Pesquisar", "pesquisar", tamanho=(20,1), padding=(2.5, 1))
        bt_voltar = self.botao("Voltar", "voltar", tamanho=(20,1), padding=(2.5, 1))
        layout = [[titulo], [lb_codigo_ingrediente], [in_codigo_ingrediente, bt_codigo_ingrediente], [bt_pesquisar, bt_voltar]]
        popup = self.popup(layout, "Pesquisar", keyboard_events= False)
        return popup.read(close= True)
