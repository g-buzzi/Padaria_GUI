from telas.tela_mostra_ingrediente import TelaMostraIngrediente
from telas.tela_abstrata import Tela
from collections import defaultdict

class TelaMostraReceita(Tela):
    __instancia = None

    def __new__(cls):
        if cls.__instancia is None:
            cls.__instancia = object.__new__(cls)
        return cls.__instancia

    def __init__(self):
        super().__init__()

    def mostra(self, dados):
        titulo = self.titulo("Receita")

        lb_codigo = self.label("Código:", tamanho= (17,1))
        in_codigo = self.entrada("codigo", dados["codigo"], True, tamanho=(33,1))

        lb_produto = self.label("Produto:", tamanho=(17,1))
        in_produto = self.entrada("produto", dados["produto_associado"], True, tamanho=(33,1))

        lb_tempo_preparo = self.label("Tempo de preparo:", tamanho=(17,1))
        in_tempo_preparo = self.entrada("tempo_preparo", dados["tempo_preparo"], True, tamanho=(33,1))

        lb_rendimento = self.label("Rendimento:", tamanho=(17,1))
        in_rendimento = self.entrada("rendimento", dados["rendimento"], True, tamanho=(33,1))

        lb_custo_preparo = self.label("Custo de preparo:", tamanho=(17,1))
        in_custo_preparo = self.entrada("custo_preparo", dados["custo_preparo"], True, tamanho=(33,1))

        lb_modo_preparo = self.label("Modo de preparo:", tamanho=(46,1))
        in_modo_preparo = self.textarea("modo_preparo", dados["modo_preparo"], True, tamanho=(46, 10))

        lb_ingredientes_receita = self.label("Ingredientes:", tamanho=(46,1))
        in_ingredientes_receita = self.lista(["Código", "Nome", "Quantidade", "Unidade de Medida"], dados["ingredientes_receita"], n_linhas= 5)

        bt_alterar = self.botao("Alterar", "alterar", tamanho=(13, 1))
        bt_remover = self.botao("Remover", "remover", tamanho=(13,1))
        bt_voltar = self.botao("Voltar", "voltar", tamanho=(13,1))

        layout = [[titulo],
                 [lb_codigo, in_codigo],
                 [lb_produto, in_produto],
                 [lb_tempo_preparo, in_tempo_preparo],
                 [lb_rendimento, in_rendimento],
                 [lb_custo_preparo, in_custo_preparo],
                 [lb_modo_preparo],
                 [in_modo_preparo],
                 [lb_ingredientes_receita],
                 [in_ingredientes_receita],
                 [bt_alterar, bt_remover, bt_voltar]]
        
        self.window = self.janela(layout)
        return self.read()
    
    def campos(self, dados):

        lb_codigo = self.label("Código:", tamanho=(17,1))
        in_codigo = self.entrada("codigo", dados["codigo"], tamanho=(33,1))

        lb_tempo_preparo = self.label("Tempo de Preparo:", tamanho=(17,1))
        in_tempo_preparo = self.entrada("tempo_preparo", dados["tempo_preparo"], tamanho=(33,1))

        lb_rendimento = self.label("Rendimento:", tamanho=(17,1))
        in_rendimento = self.entrada("rendimento", dados["rendimento"], tamanho=(33,1))

        lb_modo_preparo = self.label("Modo de preparo: ", tamanho=(46, 1))
        in_modo_preparo = self.textarea("modo_preparo", dados["modo_preparo"], tamanho=(46,10))

        lb_ingredientes_receita = self.label("Ingredientes:", tamanho=(46,1))
        in_ingredientes_receita = self.lista(["Código", "Nome", "Quantidade", "Unidade de Medida"], dados["ingredientes_receita"], n_linhas= 5, padding=(1,1))

        bt_adicionar_ingrediente = self.botao("Adicionar", "adicionar_ingrediente", padding=((1, 0), (1, 3)), expand_x= True)
        bt_remover_ingrediente = self.botao("Remover", "remover_ingrediente", padding=((0, 1), (1, 3)), expand_x= True)

        campos = [[lb_codigo, in_codigo],
                 [lb_tempo_preparo, in_tempo_preparo],
                 [lb_rendimento, in_rendimento],
                 [lb_modo_preparo],
                 [in_modo_preparo],
                 [lb_ingredientes_receita],
                 [in_ingredientes_receita],
                 [bt_adicionar_ingrediente, bt_remover_ingrediente]]
        return campos

    def cadastra(self, dados = defaultdict(lambda: None)):
        titulo = self.titulo("Cadastrar Receita")
        campos = self.campos(dados)
        bt_cadastrar = self.botao("Cadastrar", "cadastrar", tamanho=(23, 1), padding= (2.5, 2))
        bt_voltar = self.botao("Voltar", "voltar", tamanho=(23, 1), padding= (2.5, 2))

        layout = [[titulo], campos, [bt_cadastrar, bt_voltar]]
        self.window = self.janela(layout)
        return self.read()

    def altera(self, dados):
        titulo = self.titulo("Alterar Receita")
        campos = self.campos(dados)
        bt_alterar = self.botao("Alterar", "alterar", tamanho=(23, 1), padding= (2.5, 2))
        bt_cancelar = self.botao("Cancelar", "cancelar", tamanho=(23, 1), padding= (2.5, 2))

        layout = [[titulo], campos, [bt_alterar, bt_cancelar]]
        self.window = self.janela(layout)
        return self.read()

    def adiciona_ingrediente_receita(self, dados: dict):
        titulo = self.titulo("Adicionar Ingrediente")

        lb_codigo_ingrediente = self.label("Código do ingrediente:", tamanho=(30, 1))
        in_codigo_ingrediente = self.entrada("codigo_ingrediente", dados["codigo_ingrediente"],  tamanho=(20, 1), padding = ((1,0), 2))
        bt_codigo_ingrediente = self.botao("Selecionar", "seleciona_ingrediente", tamanho=(10,1), padding=((10,1), 2))

        lb_quantidade = self.label("Quantidade:", tamanho=(30, 1))
        in_quantidade = self.entrada("quantidade", dados["quantidade"], tamanho=(34,1))

        bt_adicionar = self.botao("Adicionar", "adicionar", tamanho=(12,1))
        bt_cancelar = self.botao("Cancelar", "cancelar", tamanho=(12, 1))

        layout = [[titulo], [lb_codigo_ingrediente], 
                  [in_codigo_ingrediente, bt_codigo_ingrediente],
                  [lb_quantidade], 
                  [in_quantidade],
                  [bt_adicionar, bt_cancelar]]

        popup = self.popup(layout, "Adicionar Ingrediente", keyboard_events= False)
        return popup.read(close= True)

