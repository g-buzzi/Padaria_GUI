from telas.tela_abstrata import Tela

class TelaListaEstoque(Tela):
    instancia = None

    def __new__(cls):
        if TelaListaEstoque.instancia is None:
            TelaListaEstoque.instancia = super().__new__(cls)
        return TelaListaEstoque.instancia

    def __init__(self):
        super().__init__()

    def lista_estocados(self, dados: list, tipo: str):
        titulo = self.titulo("Estoque de {}s".format(tipo))
        lista = self.lista(["Código", tipo, "Quantidade"], dados)
        bt_volta = self.botao("Voltar", "volta", expand_x= True, padding=(1,1))
        self.window = self.janela([[titulo], [lista], [bt_volta]])
        return self.read()


    def lista_movimentacoes(self, dados: list, balanco: float):
        titulo = self.titulo("Movimentações")
        botoes = {"Compra": "compra", "Produção": "producao", "Baixa": "baixa", "Voltar": "volta"}
        opcoes = self.opcoes(botoes)
        lista = self.lista(["Data", "Tipo", "Movimentado", "Quantidade", "Valor"], dados)
        lb_balanco = self.label("Balanço:  R$ {:.2f}".format(balanco), justification="right", tamanho=(55,1))
        layout = [[titulo], opcoes, [lista], [lb_balanco]]
        self.window = self.janela(layout)
        return self.read()