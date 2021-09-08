from telas.tela_abstrata import Tela
from collections import defaultdict

class TelaMostraIngrediente(Tela):
    
    __instancia = None

    def __new__(cls):
        if cls.__instancia is None:
            cls.__instancia = super().__new__(cls)
        return cls.__instancia

    def __init__(self):
        super().__init__()

    def campos(self, dados_ingrediente = defaultdict(lambda: None), leitura = False):

        lb_codigo = self.label("Código: ")
        in_codigo = self.entrada("codigo", dados_ingrediente["codigo"], leitura= leitura )

        lb_nome = self.label("Nome: ")
        in_nome = self.entrada("nome", dados_ingrediente["nome"], leitura= leitura)

        lb_unidade = self.label("Unidade de Medida: ")
        in_unidade = self.entrada("unidade_medida", dados_ingrediente["unidade_medida"], leitura= leitura)

        lb_preco = self.label("Preço Unitário: ")
        in_preco = self.entrada("preco_unitario", dados_ingrediente["preco_unitario"], leitura = leitura)

        campos = [[lb_codigo, in_codigo],
                  [lb_nome, in_nome],
                  [lb_unidade, in_unidade],
                  [lb_preco, in_preco]]
        return campos
        

    def mostra(self, dados_ingrediente = {}):
        titulo = self.titulo(dados_ingrediente["nome"])
        campos = self.campos(dados_ingrediente, True)
        alterar = self.botao("Alterar", "inicia_alteracao")
        remover = self.botao("Remover", "remove")
        voltar = self.botao("Voltar", "volta")
        layout = [[titulo]]
        for linha in campos:
            layout.append(linha)
        layout.append([alterar, remover, voltar])
        self.window = self.janela(layout)
        return self.read()

    def cadastra(self, dados_ingrediente = defaultdict(lambda: None)):
        titulo = self.titulo("Cadastra")
        campos = self.campos(dados_ingrediente)
        altera = self.botao("Cadastrar", "cadastra")
        voltar = self.botao("Voltar", "volta")
        layout = [[titulo]]
        for linha in campos:
            layout.append(linha)
        layout.append([altera, voltar])
        self.window = self.janela(layout)
        return self.read()

    def altera(self, dados_ingrediente = {}):
        titulo = self.titulo(dados_ingrediente["nome"])
        campos = self.campos(dados_ingrediente)
        altera = self.botao("Concluir", "conclui_alteracao")
        voltar = self.botao("Voltar", "volta")
        layout = [[titulo]]
        for linha in campos:
            layout.append(linha)
        layout.append([altera, voltar])
        self.window = self.janela(layout)
        return self.read()
