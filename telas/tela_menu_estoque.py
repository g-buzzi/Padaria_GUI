from telas.tela_abstrata import Tela

class TelaMenuEstoque(Tela):
    instancia = None

    def __new__(cls):
        if TelaMenuEstoque.instancia is None:
            TelaMenuEstoque.instancia = super().__new__(cls)
        return TelaMenuEstoque.instancia

    def __init__(self):
        super().__init__()

    def menu_estoque(self):
        titulo = self.titulo("Estoque")
        botoes = {"Ingredientes" :"ingredientes", "Produtos": "produtos", "Movimentações": "movimentacoes", "Voltar": "volta"}
        menu = self.menu(botoes)
        self.window = self.janela([[titulo], menu])
        return self.read()