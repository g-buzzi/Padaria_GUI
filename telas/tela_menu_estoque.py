from telas.tela_abstrata import Tela

class TelaMenuEstoque(Tela):
    __instancia = None

    def __new__(cls):
        if cls.__instancia is None:
            cls.__instancia = object.__new__(cls)
        return cls.__instancia

    def __init__(self):
        super().__init__()

    def menu_estoque(self):
        titulo = self.titulo("Estoque")
        botoes = {"Ingredientes" :"ingredientes", "Produtos": "produtos", "Movimentações": "movimentacoes", "Voltar": "volta"}
        menu = self.menu(botoes)
        self.window = self.janela([[titulo], menu])
        return self.read()