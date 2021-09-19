from typing import List
from telas.tela_abstrata import Tela
from collections import defaultdict

class TelaMostraIngrediente(Tela):
    instancia = None

    def __new__(cls):
        if TelaMostraIngrediente.instancia is None:
            TelaMostraIngrediente.instancia = super().__new__(cls)
        return TelaMostraIngrediente.instancia

    def __init__(self):
        super().__init__()

    def campos(self, dados_ingrediente = defaultdict(lambda: None), unidades_medida = list(), leitura = False):

        lb_codigo = self.label("Código:", tamanho=(17,1))
        in_codigo = self.entrada("codigo", dados_ingrediente["codigo"], leitura= leitura, tamanho= (33, 1))

        lb_nome = self.label("Nome:", tamanho=(17,1))
        in_nome = self.entrada("nome", dados_ingrediente["nome"], leitura= leitura, tamanho= (33, 1))

        lb_unidade = self.label("Unidade de Medida:", tamanho=(17,1))
        in_unidade = self.seletor("unidade_medida", valores= unidades_medida, valor_selecionado= dados_ingrediente["unidade_medida"], leitura= leitura, tamanho= (30, 1))

        lb_preco = self.label("Preço Unitário:", tamanho=(17,1))
        in_preco = self.entrada("preco_unitario", dados_ingrediente["preco_unitario"], leitura = leitura, tamanho= (33, 1))

        campos = [[lb_codigo, in_codigo],
                  [lb_nome, in_nome],
                  [lb_unidade, in_unidade],
                  [lb_preco, in_preco]]
        return campos
        

    def mostra(self, dados_ingrediente = {}):
        titulo = self.titulo(dados_ingrediente["nome"])
        campos = self.campos(dados_ingrediente, leitura = True)
        alterar = self.botao("Alterar", "inicia_alteracao")
        remover = self.botao("Remover", "remove")
        voltar = self.botao("Voltar", "volta")
        layout = [[titulo]]
        for linha in campos:
            layout.append(linha)
        layout.append([alterar, remover, voltar])
        self.window = self.janela(layout)
        return self.read()

    def cadastra(self, dados_ingrediente = defaultdict(lambda: None), unidades_medida = list()):
        titulo = self.titulo("Cadastrar Ingrediente")
        campos = self.campos(dados_ingrediente, unidades_medida)
        altera = self.botao("Cadastrar", "cadastra")
        voltar = self.botao("Voltar", "volta")
        layout = [[titulo]]
        for linha in campos:
            layout.append(linha)
        layout.append([altera, voltar])
        self.window = self.janela(layout)
        return self.read()

    def altera(self, dados_ingrediente = {}, unidades_medida = list()):
        titulo = self.titulo(dados_ingrediente["nome"])
        campos = self.campos(dados_ingrediente, unidades_medida)
        altera = self.botao("Concluir", "conclui_alteracao")
        voltar = self.botao("Voltar", "volta")
        layout = [[titulo]]
        for linha in campos:
            layout.append(linha)
        layout.append([altera, voltar])
        self.window = self.janela(layout)
        return self.read()
