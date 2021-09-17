from abc import ABC, abstractmethod
import textwrap
from PySimpleGUI.PySimpleGUI import BUTTON_TYPE_READ_FORM, WIN_CLOSED
from excecoes.window_closed import WindowClosed
import PySimpleGUI as sg

sg.InputText()

class Tela(ABC):

    @abstractmethod
    def __init__(self):
        self.definir_tema()

    @property
    def controlador(self):
        return self.__controlador

    @property
    def window(self):
        return self.__window

    @window.setter
    def window(self, window):
        self.__window = window

    def read(self):
        event, values = self.__window.read()
        if event == sg.WIN_CLOSED:
            raise WindowClosed()
        return (event, values)

    def close(self):
        try:
            if self.__window is not None:
                self.__window.close()
                self.__window = None
        except AttributeError:
            self.__window = None


#======================================= Utilidades =============================================

    def definir_tema(self):
        tema =  {"BACKGROUND": "#FFEDB7", 
         "TEXT": "#2A211C",
         "INPUT": "#FCAA7D", 
         "TEXT_INPUT": "#3A312C", 
         "SCROLL": "#3A312C", 
         "BUTTON": ("#FC9326","#3A312C"), 
         "PROGRESS": ("#FC9326","#3A312C"),
         "BORDER": 1, 
         "SLIDER_DEPTH": 0, 
         "PROGRESS_DEPTH": 0}
        sg.theme_add_new("Padaria", tema)
        sg.theme("Padaria")

    def janela(self, layout, titulo = "Padaria Elsecall", background = None, justificacao = "center"):
        janela = sg.Window(titulo, layout= layout, margins=(0,0), resizable= True, finalize= True, element_justification = justificacao, background_color= background, use_custom_titlebar = True, titlebar_icon= "C:/Users/Gabriel/Documents/#Faculdade/#1 - Segundo Semestre/Desenvolvimento de Sistemas Orientados a Objetos I/Padaria GUI/telas/icon.png") 
        return janela

    def popup(self, layout, titulo="Mensagem", tamanho = (None, None), keyboard_events = True):
        popup = sg.Window(titulo, layout, margins=(0,0), size = tamanho, element_justification= 'center', modal = True, use_custom_titlebar= True, return_keyboard_events = keyboard_events, finalize = True)
        return popup

    def titulo(self, texto, font_size = 14):
        titulo = sg.Text(texto, background_color="#3A312C",
                        text_color="#FC9326", pad=(0,0), 
                        expand_x = True, justification="center", 
                        font="Arial {} bold".format(font_size), 
                        relief= sg.RELIEF_FLAT, border_width=10)
        return titulo

    def botao(self, texto, chave, desativado = False, expand_x = False, expand_y = False, tamanho = (None, None), padding = None):
        if tamanho != (None, None):
            auto_size = False
        else:
            auto_size = True
        if desativado:
            botao = sg.Button(button_text = texto, key = chave, 
                              disabled=True, button_color=("#3A312C", "#FC9326"), 
                              disabled_button_color= ("#3A312C", "#3A312C"),
                              expand_x= expand_x, expand_y= expand_y,
                              pad = padding, size= tamanho, auto_size_button= auto_size)
        else:
            botao = sg.Button(button_text = texto, key = chave,
                              expand_x= expand_x, expand_y= expand_y,
                              pad = padding, size= tamanho, auto_size_button= auto_size)
        return botao

    def label(self, texto = "", tamanho = (17, 1), justification = "left", padding = (1, 1)):
        label = sg.Text(texto, font="Arial 10 bold", size= tamanho, justification= justification, pad= padding)
        return label

    def entrada(self, chave, valor = "", leitura = False, tamanho = (33, 1), expand_x = False, padding = (1, 1)):
        if tamanho != (None, None):
            expand_x = False
        entrada = sg.InputText(default_text = valor, key= chave, size= tamanho, readonly = leitura, disabled_readonly_background_color= "#FFEDB7", disabled_readonly_text_color= "#3A312C", border_width=0, expand_x = expand_x, pad= padding)
        return entrada

    def textarea(self, chave, valor = "", leitura = False, tamanho = (46, 10)):
        if leitura:
            area = sg.Text(valor, size= tamanho, key= chave, border_width= 0.5, relief= sg.RELIEF_SOLID)
        else:
            area = sg.Multiline(key = chave, default_text = valor, size= tamanho)
        return area

    def seletor(self, chave, valores = [], valor_selecionado = None, tamanho = (None, None), leitura = False):
        if leitura:
            seletor = sg.Text(valor_selecionado, size= tamanho, key= chave, border_width= 0, pad=(1,1))
        else:
            seletor = sg.Combo(valores, valor_selecionado, key= chave, size = tamanho, disabled= leitura)
        return seletor

    def radio(self, id_grupo, texto, chave, selecionado = False, tamanho = (None, None), leitura = False):
        radio = sg.Radio(texto, id_grupo, key = id_grupo + "_" + chave, default = selecionado, size = tamanho, circle_color= "#FCAA7D", disabled= leitura) 
        return radio

#======================================= Bases pra tela =============================================

    def opcoes(self, botoes = {}, selecionado = ""):
        opcoes = []
        for nome, chave in botoes.items():
            if chave == selecionado:
                bt = self.botao(nome, chave= chave, expand_x=True,
                                padding=((0.5, 0.5), (0.5, 0.5)), 
                                desativado= True)
            else:
                bt = self.botao(nome, chave= chave, expand_x=True,
                                padding=((0.5, 0.5), (0.5, 0.5)))
            opcoes.append(bt)
        return opcoes

    def pesquisar(self, texto = "Pesquisa: "):
        label = self.label(texto, tamanho=(30,1))
        entrada = self.entrada("pesquisa", tamanho=(30,1))
        bt_volta = self.botao("Voltar", "voltar", tamanho=(10,1), padding=(2,5))
        bt_pesquisa = self.botao("Pesquisar", "pesquisar", tamanho=(10,1), padding=(2,5))
        layout = [[label], [entrada], [bt_pesquisa, bt_volta]]
        botao, pesquisa = self.popup(layout, "Pesquisa", tamanho= (250, 125), keyboard_events= False).read(close=True)
        if botao == "pesquisar":
            pesquisa = pesquisa["pesquisa"]
        else:
            pesquisa = None
        return pesquisa

    def lista(self, heading = [], valores = [], chave = "lista", auto_size = True, n_linhas = 10, padding = (0,0)):
        if len(valores) == 0:
            auto_size = False
        tabela = sg.Table(valores, heading, key= chave,
                          expand_x = True, expand_y= True,
                          header_text_color= "#FC9326",
                          header_background_color= "#3A312C",
                          pad= padding, justification= "center",
                          auto_size_columns= auto_size,
                          num_rows= n_linhas)
        return tabela

    def menu(self, botoes = dict, tamanho_botao = (40,2), padding_botao = (5, 2.5)):
        menu = []
        for nome, chave in botoes.items():
            bt = self.botao(nome, chave, tamanho= tamanho_botao, padding= padding_botao)
            menu.append([bt])
        return menu

#======================================= Funções Universais =============================================

    def configura_lista(self, chave_lista = "lista", janela = None):
        if janela is None:
            janela = self.__window
        janela[chave_lista].bind('<Double-1>', "_clique_duplo")

    def mensagem(self, mensagem: str):
        mensagem = textwrap.fill(mensagem, width = 50)
        texto = self.label(mensagem,  justification= "center", padding=(5,2), tamanho=(None, None))
        botao = self.botao("Ok", "ok",tamanho=(10,1), padding=(2,5))
        layout = [[texto], [botao]]
        self.popup(layout, "Mensagem").read(close=True)

    def mensagem_erro(self, mensagem: str):
        mensagem = textwrap.fill(mensagem, width = 50)
        texto = self.label(mensagem, justification="center", padding= (5, 2), tamanho=(None, None))
        botao = sg.Button(button_text = "Ok", key = "ok", 
                              button_color=("#3A312C", "#FC9326"), 
                              pad = (2,5), size= (10,1))
        layout = [[texto], [botao]]
        self.popup(layout, "Erro").read(close = True)