from telas.tela_abstrata import Tela

class TelaListaProduto(Tela):
    instancia = None

    def __new__(cls):
        if TelaListaProduto.instancia is None:
            TelaListaProduto.instancia = super().__new__(cls)
        return TelaListaProduto.instancia

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
        lista = self.lista(["Código", "Nome", "Custo de produção", "Preço de Venda"], dados_produtos)
        layout = [[titulo], opcoes, [lista]]
        self.window = self.janela(layout = layout, background = "#FC9326")
        self.configura_lista()
        return self.read()
        