from telas.tela_abstrata import Tela
from collections import defaultdict

class TelaMostraProduto(Tela):
    __instancia = None

    def __new__(cls):
        if cls.__instancia is None:
            cls.__instancia = object.__new__(cls)
        return cls.__instancia

    def __init__(self):
        super().__init__()

    def campos(self, dados_produto = defaultdict(lambda: None), leitura = False):
        lb_codigo = self.label("Código:", tamanho=(17, 1))
        in_codigo = self.entrada("codigo", dados_produto["codigo"], leitura = leitura, tamanho=(33,1))

        lb_nome = self.label("Nome:", tamanho=(17, 1))
        in_nome = self.entrada("nome", dados_produto["nome"], tamanho=(33,1), leitura = leitura)

        if leitura:
            lb_codigo_receita = self.label("Código da receita:", tamanho=(17, 1))
            in_codigo_receita = self.entrada("codigo_receita", dados_produto["codigo_receita"], leitura, tamanho=(33,1))

            lb_custo_unitario = self.label("Custo Unitário: ", tamanho=(17, 1))
            in_custo_unitario = self.entrada("custo_unitario", dados_produto["custo_unitario"], leitura, tamanho=(33,1))

            receita = [[lb_codigo_receita, in_codigo_receita], [lb_custo_unitario, in_custo_unitario]]
        else:
            lb_codigo_receita = self.label("Código da receita:", tamanho=(17, 1))
            in_codigo_receita = self.entrada("codigo_receita", dados_produto["codigo_receita"], leitura, tamanho=(19,1))
            bt_seleciona_receita = self.botao("Selecionar", "seleciona_receita", tamanho=(10,1), padding=((10,1), 2))

            receita = [lb_codigo_receita, in_codigo_receita, bt_seleciona_receita]

        lb_preco_venda = self.label("Preço de venda:", tamanho=(17, 1))
        in_preco_venda = self.entrada("preco_venda", dados_produto["preco_venda"], leitura, tamanho=(33,1))

        lb_descricao = self.label("Descrição:", tamanho=(46, 1), padding=(1, 1))
        in_descricao = self.textarea("descricao", dados_produto["descricao"], leitura, tamanho=(46, 10))

        campos = [[lb_codigo, in_codigo],
                   [lb_nome, in_nome],
                    receita,
                    [lb_preco_venda, in_preco_venda],
                    [lb_descricao],
                    [in_descricao]]
        return campos

    def cadastra(self, dados):
        titulo = self.titulo("Cadastrar Produto")
        
        campos = self.campos(dados)

        bt_cadastrar = self.botao("Cadastrar", "cadastra", tamanho=(20, 1))
        bt_voltar = self.botao("Voltar", "volta", tamanho=(20,1))

        layout = [[titulo],
                  campos,
                  [bt_cadastrar, bt_voltar]]
        self.window = self.janela(layout)
        return self.read()

    def altera(self, dados):
        titulo = self.titulo("Alterar Produto")
        
        campos = self.campos(dados)

        bt_alterar = self.botao("Alterar", "altera", tamanho=(20,1))
        bt_cancelar = self.botao("Cancelar", "cancela", tamanho=(20,1))

        layout = [[titulo],
                  campos,
                  [bt_alterar, bt_cancelar]]
        self.window = self.janela(layout)
        return self.read()

    def mostra(self, dados):
        titulo = self.titulo(dados["nome"])

        campos = self.campos(dados, True)

        bt_alterar = self.botao("Alterar", "altera", tamanho=(12,1))
        bt_remover = self.botao("Remover", "remove", tamanho=(12,1))
        bt_voltar = self.botao("Voltar", "volta", tamanho=(12,1))

        layout = [[titulo],
                  campos,
                  [bt_alterar, bt_remover, bt_voltar]]

        self.window = self.janela(layout)
        return self.read()
