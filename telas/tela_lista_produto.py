from telas.tela_abstrata import Tela

class TelaListaProduto(Tela):
    __instancia = None

    def __new__(cls):
        if cls.__instancia is None:
            cls.__instancia = object.__new__(cls)
        return cls.__instancia

    def __init__(self):
        super().__init__()

    def lista_produtos(self, dados_produtos: list, pesquisa = False):
        if pesquisa is False:
            titulo = self.titulo("Produtos")
            selecionado = "listar"
        else:
            titulo = self.titulo("Pesquisa '" + pesquisa + "'")
            selecionado = ""
        botoes = {"Listar": "listar", "Cadastrar": "cadastrar", "Pesquisar": "pesquisar", "Voltar": "voltar"}
        opcoes = self.opcoes(botoes, selecionado = selecionado)
        lista = self.lista(["Código", "Nome", "Descrição", "Custo de produção", "Preço de Venda"], dados_produtos)
        layout = [[titulo], opcoes, [lista]]
        self.window = self.janela(layout = layout, background = "#FC9326")
        self.configura_lista()
        return self.read()

    def seleciona_produto(self, dados_produtos: list):
        lista =  self.lista(["Código", "Nome", "Descrição", "Custo de produção", "Preço de Venda"], dados_produtos, chave= "lista")
        janela = self.popup([[lista]], "Selecionar Produto", keyboard_events= False)
        self.configura_lista(janela= janela)
        botao, values = janela.read(close = True)
        if botao is None:
            return None
        else:
            try:
                return values["lista"][0]
            except IndexError:
                return None
        