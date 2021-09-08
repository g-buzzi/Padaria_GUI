from abc import ABC, abstractmethod
from tkinter.constants import CENTER, LEFT
import PySimpleGUI as sg


class Tela(ABC):
    @abstractmethod
    def __init__(self):
        self.__window = None
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

    def close(self):
        if self.__window is not None:
            self.__window.close()

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

    def janela(self, layout, titulo = "Padaria Elsecall", background = None):
        janela = sg.Window(titulo, layout= layout, margins=(0,0), finalize= True, element_justification = LEFT, use_custom_titlebar= True, background_color= background)
        return janela

    def titulo(self, texto, font_size = 14):
        titulo = sg.Text(texto, background_color="#3A312C",
                        text_color="#FC9326", pad=(0,0), 
                        expand_x = True, justification="center", 
                        font="Arial {} bold".format(font_size), 
                        relief= sg.RELIEF_FLAT, border_width=10)
        return titulo

    def botao(self, texto, chave, desativado = False, expand_x = False, expand_y = False, padding = None):
        if desativado:
            botao = sg.Button(button_text = texto, key = chave, 
                              disabled=True, button_color=("#3A312C", "#FC9326"), 
                              disabled_button_color= ("#3A312C", "#3A312C"),
                              expand_x= expand_x, expand_y= expand_y,
                              pad = padding)
        else:
            botao = sg.Button(button_text = texto, key = chave,
                              expand_x= expand_x, expand_y= expand_y,
                              pad = padding)
        return botao

    def label(self, texto = "", tamanho = (None, None)):
        label = sg.Text(texto, font="Arial 10 bold", size= tamanho, justification= LEFT)
        return label

    def entrada(self, chave, valor = "", leitura = False, tamanho = (50, 1)):
        entrada = sg.InputText(default_text = valor, key= chave, size= tamanho,  readonly = leitura, disabled_readonly_background_color= "#FFEDB7", disabled_readonly_text_color= "#3A312C", border_width=0)
        return entrada

    def textarea(self, chave, valor = "", leitura = False, tamanho = (55, 10)):
        if leitura:
            area = sg.Text(valor, size= tamanho, key= chave, border_width= 0.5, relief= sg.RELIEF_SOLID)
        else:
            area = sg.Multiline(key = chave, default_text = valor, size= tamanho)
        return area

    def seletor(self, chave, valores = [], valor_selecionado = None, tamanho = (None, None), leitura = False):
        if leitura:
            seletor = sg.Text(valor_selecionado, size= tamanho, key= chave, border_width= 0)
        else:
            seletor = sg.Combo(valores, valor_selecionado, key= chave, size = tamanho, disabled= leitura)
        return seletor

    def radio(id_grupo, texto, chave, selecionado = False, tamanho = (None, None), leitura = False):
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
        pesquisa = sg.popup_get_text(texto, title = "Pesquisa")
        return pesquisa

    def lista(self, heading = [], valores = [], chave = "lista", auto_size = True):
        if len(valores) == 0:
            auto_size = False
        tabela = sg.Table(valores, heading, key= chave,
                          expand_x = True, expand_y= True,
                          header_text_color= "#FC9326",
                          header_background_color= "#3A312C",
                          pad=(0,0), justification= CENTER,
                          auto_size_columns= auto_size)
        return tabela

    def configura_lista(self, chave_lista = "lista"):
        self.__window[chave_lista].bind('<Double-1>', "_clique_duplo")

    def mensagem(self, mensagem: str):
        sg.popup(mensagem, title = "Mensagem")

    def mensagem_erro(self, mensagem: str):
        sg.popup_error(mensagem, title = "Error")

""" Fazer novas checagens

    def le_num_inteiro(self, mensagem: str = "Escolha uma opção: ", valores_validos: list = None) -> int:
        while True:
            try:
                inteiro = input(mensagem)
                inteiro = int(inteiro) 
                if valores_validos and inteiro not in valores_validos:
                    raise ValueError
                if inteiro < 0:
                    self.mensagem_erro("Valor incorreto. Digite um valor maior que 0")
                else:
                    return inteiro
            except ValueError:
                self.mensagem_erro("Valor incorreto. Digite um número inteiro válido")

    def le_num_fracionario(self, mensagem: str = "Digite um valor", digitos: int = 2):
        while True:
            try:
                fracionario = round(float(input(mensagem)), digitos)
                if fracionario >= 0:
                    return fracionario
                self.mensagem_erro("Valor incorreto. Digite um número maior que 0.")
            except ValueError:
                self.mensagem_erro("Valor incorreto. Digite um número fracionário válido.")
    
    def le_string(self, mensagem: str = "Digite algo"):
        string = input(mensagem)
        return string.strip()

"""