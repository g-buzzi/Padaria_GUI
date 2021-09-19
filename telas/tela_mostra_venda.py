from telas.tela_abstrata import Tela
from collections import defaultdict

class TelaMostraVenda(Tela):
    __instancia = None

    def __new__(cls):
        if TelaMostraVenda.__instancia is None:
            TelaMostraVenda.__instancia = object.__new__(cls)
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

        self.window = self.janela(layout)
        return self.read()

      

    def campos_para_mostrar(self, dados_venda = defaultdict(lambda: None), leitura = True, tipo='Encomenda'):

        lb_codigo = self.label("Código: ", tamanho=(17,1))
        in_codigo = self.entrada("codigo", dados_venda["codigo"], leitura= leitura, tamanho= (33, 1))

        lb_data_entrega = self.label("Data de entrega: ", tamanho=(17,1))
        in_data_entrega = self.entrada("data_entrega", dados_venda["data_entrega"], leitura= leitura, tamanho= (33, 1))

        lb_cliente = self.label("Cliente: ", tamanho=(17,1))
        in_cliente = self.entrada("cliente", dados_venda["cliente"], leitura= leitura, tamanho= (33, 1))

        lb_entregue = self.label("Entregue: ", tamanho=(17,1))
        in_entregue = self.entrada("entregue", dados_venda["entregue"], leitura= leitura, tamanho= (33, 1))

        lb_atendente = self.label("Atendente: ", tamanho=(17,1))
        in_atendente = self.entrada("atendente", dados_venda["atendente"], leitura = leitura, tamanho= (33, 1))

        lb_total = self.label("Total: ", tamanho=(17,1))
        in_total = self.entrada("total", dados_venda["total"], leitura = leitura, tamanho= (33, 1))

        lb_desconto = self.label("Desconto: ", tamanho=(17,1))
        in_desconto = self.entrada("desconto", dados_venda["desconto"], leitura = leitura, tamanho= (33, 1))

        campos = [
                    [lb_codigo, in_codigo, (lb_data_entrega, in_data_entrega) if tipo=='Encomenda' else None],
                    [lb_cliente, in_cliente, (lb_entregue, in_entregue) if tipo=='Encomenda' else None],
                    [lb_atendente, in_atendente],
                    [lb_total, in_total],
                    [lb_desconto, in_desconto]
                ]

        return campos

    def campos_para_cadastro(self, dados_venda = defaultdict(lambda: None), tipo=None, leitura = False):

        lb_codigo = self.label("Código: ", tamanho=(17,1))
        in_codigo = self.entrada("codigo", dados_venda["codigo"], leitura=leitura, tamanho= (33, 1))
        
        lb_data_entrega = self.label("Data de entrega: ", tamanho=(17,1))
        in_data_entrega = self.entrada("data_entrega", dados_venda["data_entrega"], leitura=leitura, tamanho= (33, 1))

        lb_cliente = self.label("Cliente: ", tamanho=(17,1))
        in_cliente = self.entrada("cliente", dados_venda["cliente"], leitura= leitura, tamanho= (33, 1))

        lb_atendente = self.label("Atendente: ", tamanho=(17,1))
        in_atendente = self.entrada("atendente", dados_venda["atendente"], leitura = leitura, tamanho= (33, 1))

        lb_desconto = self.label("Desconto: ", tamanho=(17,1))
        in_desconto = self.entrada("desconto", dados_venda["desconto"], leitura = leitura, tamanho= (33, 1))

        campos = [
                    [lb_codigo, in_codigo],
                    [lb_data_entrega, in_data_entrega] if tipo == 'tipo_encomenda' else [],
                    [lb_cliente, in_cliente],
                    [lb_atendente, in_atendente],
                    [lb_desconto, in_desconto]
                ]

        return campos

    
    def cadastrar(self, dados_venda = defaultdict(lambda: None), tipo=None):

            
        layout = [
                    [self.titulo("Cadastrar Venda" if tipo == 'tipo_venda' else "Cadastrar Encomenda")],
                    list(map(lambda campo : campo, self.campos_para_cadastro(dados_venda, tipo=tipo))),
                    [
                        self.botao("Cadastrar", "bt-cadastrar"), 
                        self.botao("Voltar", "bt-voltar")
                    ]
                ]

        self.window = self.janela(layout)
        return self.read()

    def mostrar(self, dados_venda = {}, tipo='Encomenda'):

        layout = [
                    [self.titulo('Venda ' + dados_venda["codigo"])],
                    list(map(lambda campo : campo, self.campos(dados_venda, leitura = True))),
                    [
                        self.botao("Entregar", "bt-entregar") if tipo == 'Encomenda' else None, 
                        self.botao("Cancelar", "bt-cancelar") if tipo == 'Encomenda' else None, 
                        self.botao("Voltar", "bt-voltar")
                    ]
                ]
       
        self.window = self.janela(layout)
        return self.read()