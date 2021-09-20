from telas.tela_abstrata import Tela
from collections import defaultdict

class TelaMostraVenda(Tela):
    __instancia = None

    def __new__(cls):
        if TelaMostraVenda.__instancia is None:
            TelaMostraVenda.__instancia = super().__new__(cls)
        return TelaMostraVenda.__instancia

    def __init__(self):
        super().__init__()

    def opcoes_vendas(self):
        rd_tipo_venda = self.radio("tipo", "Venda", "venda", selecionado= True, tamanho= (11, 1))
        rd_tipo_encomenda = self.radio("tipo", "Encomenda", "encomenda", selecionado = False, tamanho= (11,1))

        layout = [
            [self.titulo('Tipo')],
            [rd_tipo_venda],
            [rd_tipo_encomenda],
            [self.botao("Ok", "bt-ok"), self.botao("Cancelar", "bt-cancelar")]
        ]

        janela = self.popup(layout)
        return janela.read(close = True)

      

    def campos_para_mostrar(self, dados_venda, leitura = True):


        lb_tipo = self.label("Encomenda: ", tamanho=(17,1))
        in_tipo = self.entrada("tipo", dados_venda["encomenda"], leitura= leitura, tamanho= (33, 1))

        lb_data_entrega = self.label("Data de entrega: ", tamanho=(17,1))
        in_data_entrega = self.entrada("data_entrega", dados_venda["data_entrega"], leitura= leitura, tamanho= (33, 1))

        lb_cliente = self.label("Cliente: ", tamanho=(17,1))
        in_cliente = self.entrada("cliente", dados_venda["cliente"], leitura= leitura, tamanho= (33, 1))

        lb_entregue = self.label("Entregue: ", tamanho=(17,1))
        in_entregue = self.entrada("entregue", dados_venda["entregue"], leitura= leitura, tamanho= (33, 1))

        lb_atendente = self.label("Atendente: ", tamanho=(17,1))
        in_atendente = self.entrada("atendente", dados_venda["atendente"], leitura = leitura, tamanho= (33, 1))

        lb_total = self.label("Total: ", tamanho=(17,1))
        in_total = self.entrada("total", dados_venda["preco_final"], leitura = leitura, tamanho= (33, 1))

        lb_desconto = self.label("Desconto: ", tamanho=(17,1))
        in_desconto = self.entrada("desconto", dados_venda["desconto"], leitura = leitura, tamanho= (33, 1))

        campos = [
                    [lb_tipo, in_tipo],
                    [lb_data_entrega, in_data_entrega] if dados_venda['encomenda'] == 'Sim' else [],
                    [lb_cliente, in_cliente],
                    [lb_entregue, in_entregue],
                    [lb_atendente, in_atendente],
                    [lb_desconto, in_desconto],
                    [lb_total, in_total]
                ]

        return campos

    def adiciona_item_venda(self, dados = defaultdict(lambda: None)):
        titulo = self.titulo("Adicionar Item")

        lb_codigo_produto = self.label("Código do produto:")
        in_codigo_produto = self.entrada("codigo_produto", dados["codigo_produto"],  tamanho= (33, 1))

        lb_quantidade = self.label("Quantidade:")
        in_quantidade = self.entrada("quantidade", dados["quantidade"], tamanho= (33, 1))

        bt_adicionar = self.botao("Adicionar", "adicionar", tamanho=(20, 1))
        bt_cancelar = self.botao("Cancelar", "cancelar", tamanho=(20, 1))

        layout = [
                    [titulo], 
                    [lb_codigo_produto, in_codigo_produto],
                    [lb_quantidade, in_quantidade], 
                    [bt_adicionar, bt_cancelar]
                ]

        popup = self.popup(layout, "Adicionar Item", keyboard_events= False)
        return popup.read(close= True)

    def campos_para_cadastro(self, dados_venda = defaultdict(lambda: None), tipo=None, leitura = False):


        lb_codigo = self.label("Código*: ", tamanho=(17,1))
        in_codigo = self.entrada("codigo", dados_venda["codigo"], leitura=leitura, tamanho= (33, 1))
        
        if tipo == 'tipo_encomenda':
            lb_data_entrega = self.label("Data de entrega*: ", tamanho=(17,1))
            in_data_entrega = self.entrada("data_entrega", dados_venda["data_entrega"], leitura=leitura, tamanho= (33, 1))

        lb_cliente = self.label("Cliente*: " if tipo == 'tipo_encomenda' else 'Cliente: ', tamanho=(17,1))
        in_cliente = self.entrada("cliente", dados_venda["cliente"], leitura= leitura, tamanho= (33, 1))

        lb_atendente = self.label("Atendente*: ", tamanho=(17,1))
        in_atendente = self.entrada("atendente", dados_venda["atendente"], leitura = leitura, tamanho= (33, 1))

        lb_desconto = self.label("Desconto: ", tamanho=(17,1))
        in_desconto = self.entrada("desconto", dados_venda["desconto"], leitura = leitura, tamanho= (33, 1))

        lb_itens = self.label("Itens*:", tamanho=(46,1))
        in_itens = self.lista(["Código", "Nome", "Quantidade", "Preço"], dados_venda["lista"], chave='itens', n_linhas= 5, padding=(1,1))

        bt_adicionar_item = self.botao("Adicionar", "bt_adicionar_item", padding=((1, 0), (1, 3)), expand_x= True)
        bt_remover_item = self.botao("Remover", "bt_remover_item", padding=((0, 1), (1, 3)), expand_x= True)

        campos = [
                    [lb_codigo, in_codigo],
                    [lb_data_entrega, in_data_entrega] if tipo == 'tipo_encomenda' else [],
                    [lb_cliente, in_cliente],
                    [lb_atendente, in_atendente],
                    [lb_desconto, in_desconto],
                    [lb_itens],
                    [in_itens],
                    [bt_adicionar_item, bt_remover_item]
                ]

        return campos

    
    def cadastrar(self, dados_venda = defaultdict(lambda: None), tipo=None):

        layout = [
                    [self.titulo("Cadastrar Venda" if tipo == 'tipo_venda' else "Cadastrar Encomenda")],
                    list(map(lambda campo : campo, self.campos_para_cadastro(dados_venda, tipo=tipo))),
                    [
                        self.botao("Cadastrar", "bt-cadastrar", tamanho=(20, 1)), 
                        self.botao("Voltar", "bt-voltar", tamanho=(20, 1))
                    ]
                ]

        self.window = self.janela(layout)
        return self.read()

    def mostrar(self, dados_venda = {}):

        print('lambda', list(map(lambda item: item.produto.nome, dados_venda['itens'])))

        layout = [
                    [self.titulo('Venda de Código: ' + str(dados_venda["codigo"]))],
                    list(map(lambda campo : campo, self.campos_para_mostrar(dados_venda, leitura = True))),
                    self.mostrar_itens(dados_venda),
                    [
                        self.botao("Entregar", "bt-entregar", tamanho=(12, 1)) if dados_venda['encomenda'] == 'Sim' and dados_venda['entregue'] == 'Não' else [], 
                        self.botao("Cancelar Encomenda", "bt-cancelar", tamanho=(12, 1)) if dados_venda['encomenda'] == 'Sim' and dados_venda['entregue'] == 'Não' else [], 
                        self.botao("Voltar", "bt-voltar", tamanho=(12, 1))
                    ]

                ]
       
        self.window = self.janela(layout)
        return self.read()

    def mostrar_itens(self, dados_venda):

        lb_itens = self.label('Itens: ')
        in_itens = self.lista(['Quantidade', 'Item', 'Preço'], list(map(lambda item: [item.quantidade, item.produto.nome, int(item.quantidade)*item.produto.preco_venda], dados_venda['itens'])), n_linhas=5)

        campos = [
            [lb_itens],
            [in_itens]
        ]

        return campos