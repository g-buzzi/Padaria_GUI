from telas.tela_abstrata import Tela

class TelaMostraEstoque(Tela):
    __instancia = None

    def __new__(cls):
        if cls.__instancia is None:
            cls.__instancia = object.__new__(cls)
        return cls.__instancia

    def __init__(self):
        super().__init__()

    def campos(self, dados, tipo = "ingrediente"):
        if tipo == None:
            lb_codigo = self.label("Código: ", tamanho= (30,1))
        else:
            lb_codigo = self.label("Código do {}:".format(tipo), tamanho= (30,1))
        in_codigo = self.entrada("codigo", dados["codigo"],  tamanho=(20, 1), padding = ((1,0), 2))
        bt_codigo = self.botao("Selecionar", "seleciona", tamanho=(10,1), padding=((10,1), 2))

        lb_quantidade = self.label("Quantidade:", tamanho= (30,1))
        in_quantidade = self.entrada("quantidade", dados["quantidade"])

        campos = [[lb_codigo], [in_codigo, bt_codigo], [lb_quantidade], [in_quantidade]]

        return campos

    def baixa(self, dados):
        titulo = self.titulo("Baixa do Estoque")
        lb_tipo = self.label("Tipo", tamanho= (30,1))
        rd_ing = self.radio("tipo", "Ingrediente", "ingrediente", selecionado= dados["tipo_ingrediente"], tamanho= (11, 1))
        rd_prod = self.radio("tipo", "Produto", "produto", selecionado = dados["tipo_produto"], tamanho= (11,1))
        campos = self.campos(dados, None)

        bt_baixa = self.botao("Baixa", "baixa", tamanho=(13, 1))
        bt_cancela = self.botao("Cancelar", "cancela", tamanho=(13, 1))

        layout = [[titulo], [lb_tipo], [rd_ing, rd_prod], campos, [bt_baixa, bt_cancela]]
        self.window = self.janela(layout)
        return self.read()


    def compra(self, dados):
        titulo = self.titulo("Compra")
        campos = self.campos(dados, tipo= "ingrediente")
        bt_compra = self.botao("Comprar", "compra", tamanho= (13, 1))
        bt_cancela = self.botao("Cancelar", "cancela", tamanho=(13,1))
        layout = [[titulo], campos, [bt_compra, bt_cancela]]
        self.window = self.janela(layout)
        return self.read()

    def producao(self, dados):
        titulo = self.titulo("Produção")
        campos = self.campos(dados, tipo= "produto")
        bt_produzir = self.botao("Produzir", "producao", tamanho=(13,1))
        bt_cancela = self.botao("Cancelar", "cancela", tamanho=(13,1))
        layout = [[titulo], campos, [bt_produzir, bt_cancela]]
        self.window = self.janela(layout)
        return self.read()
