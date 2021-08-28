from typing import DefaultDict
from entidades.venda import Venda
from entidades.movimentacao import Movimentacao
from controladores.controlador_abstrato import Controlador
from telas.tela_estoque import TelaEstoque
from datetime import datetime
from entidades.estoque import Estoque
from collections import defaultdict

class ControladorEstoque(Controlador):
    def __init__(self, controlador_central):
        super().__init__(TelaEstoque(self))
        self.__estoque = Estoque()
        self.__controlador_central = controlador_central

    @property
    def estoque(self):
        return self.__estoque

    @property
    def produtos_estoque(self):
        return self.__controlador_central.controlador_produtos.produtos

    @property
    def ingredientes_estoque(self):
        return self.__controlador_central.controlador_ingredientes.ingredientes

    def abre_tela_inicial(self):
        opcoes = {1: "Compra", 2: "Produção", 3: "Baixa", 4: "Listar estoque", 5: "Movimentações", 0: "Voltar"}
        switcher = {1: self.realiza_compra, 2: self.realiza_producao, 3: self.realiza_baixa, 4: self.lista_estoque, 5: self.lista_movimentacoes, 0: False}
        while True:
            opcao = self.tela.mostra_opcoes(opcoes, "--------- Estoque ---------")
            funcao_escolhida = switcher[opcao]
            if funcao_escolhida:
                funcao_escolhida()
            else:
                break

    def processa_venda(self, venda: Venda):
        venda_organizada = self.possibilidade_venda(venda)
        for produto, quantidade in venda_organizada.items():
            self.__estoque.venda(produto, quantidade)
                

    def possibilidade_venda(self, venda: Venda):
        produtos = defaultdict(lambda: 0)
        for item in venda.itens:
            produtos[item.produto] += item.quantidade
        for produto, quantidade in produtos.items():
            if produto.quantidade_estoque < quantidade:
                self.tela.mensagem_erro("Quantidade insuficente de {} no estoque".format(produto.nome))
                raise ValueError
        return produtos
        
        


    def lista_estoque(self):
        self.tela.cabecalho("Lista do Estoque")
        self.lista_produtos()
        self.lista_ingredientes()
        self.tela.balanco(self.__estoque.balanco)

    def lista_ingredientes(self):
        self.tela.cabecalho("Ingredientes")
        self.tela.cabecalho_estoque("Ingrediente")
        for ingrediente in self.ingredientes_estoque.values():
            self.mostra_estoque(ingrediente)
        self.tela.quebra_linha()

    def lista_produtos(self):
        self.tela.cabecalho("Produtos")
        self.tela.cabecalho_estoque("Produto")
        for produto in self.produtos_estoque.values():
            self.mostra_estoque(produto)
        self.tela.quebra_linha()

    def lista_movimentacoes(self):
        self.tela.cabecalho("Movimentações")
        for movimentacao in self.__estoque.movimentacoes:
            dados = self.dados_movimentacao(movimentacao)
            self.tela.mostra_movimentacao(dados)

    def realiza_compra(self):
        opcoes = {1: "Continuar compras", 0: "Voltar"}
        while True:
            self.tela.cabecalho("Compra")
            codigo_ingrediente = self.tela.le_codigo("ingrediente")
            try:
                ingrediente = self.ingredientes_estoque[codigo_ingrediente]
            except KeyError:
                self.tela.mensagem_erro("Não existe ingrediente com este código")
            else:
                self.__controlador_central.controlador_ingredientes.mostra_ingrediente(ingrediente)
                quantidade = self.tela.le_quantidade()
                if quantidade != 0:
                    self.__estoque.compra(ingrediente, quantidade)
                    self.tela.mensagem("Compra registrada com sucesso")
                else:
                    self.tela.mensagem_erro("Quantidade igual a 0, compra cancelada")
            opcao = self.tela.mostra_opcoes(opcoes)
            if opcao == 0:
                break

    def realiza_producao(self):
        opcoes = {1: "Continuar produção", 0: "Voltar"}
        while True:
            self.tela.cabecalho("Produção")
            codigo_produto = self.tela.le_codigo("produto")
            try:
                produto = self.produtos_estoque[codigo_produto]
            except KeyError:
                self.tela.mensagem_erro("Não existe produto com este código")
            else:
                self.__controlador_central.controlador_produtos.mostra_produto(produto)
                if produto.receita is False:
                    self.tela.mensagem_erro("O produto não possui receita")
                    return
                else:
                    quantidade = self.tela.le_quantidade()
                    if quantidade == 0:
                        self.tela.mensagem_erro("Quantidade igual a 0, produção cancelada")
                        return
                    else:
                        for ingrediente, quantidade_ingrediente in produto.receita.ingredientes_receita.items():
                            if ingrediente.quantidade_estoque < quantidade_ingrediente * quantidade:
                                self.tela.mensagem_erro("Ingredientes insuficientes para a produção")
                                break 
                        else:
                            self.__estoque.producao(produto, quantidade)
                            self.tela.mensagem("Produção registrada com sucesso")
            opcao = self.tela.mostra_opcoes(opcoes)
            if opcao == 0:
                break

    def realiza_baixa(self):
        self.tela.cabecalho("Baixa")
        opcoes = {1: "Baixa de produto", 2: "Baixa de ingrediente", 0: "Voltar"}
        switcher = {1: self.realiza_baixa_produto, 2: self.realiza_baixa_ingrediente, 0: False}
        while True:
            opcao = self.tela.mostra_opcoes(opcoes)
            if switcher[opcao] is False:
                break
            switcher[opcao]()
            
    def realiza_baixa_ingrediente(self):
        self.tela.cabecalho("Baixa de Ingrediente")
        codigo_ingrediente = self.tela.le_codigo("ingrediente")
        try:
            ingrediente = self.ingredientes_estoque[codigo_ingrediente]
        except KeyError:
            self.tela.mensagem_erro("Não existe ingrediente com este código")
        else:
            self.__controlador_central.controlador_ingredientes.mostra_ingrediente(ingrediente)
            quantidade = self.tela.le_quantidade()
            if quantidade == 0:
                self.tela.mensagem_erro("Quantidade igual a 0, baixa cancelada")
            elif quantidade <= ingrediente.quantidade_estoque:
                self.__estoque.baixa(ingrediente, quantidade)
                self.tela.mensagem("Baixa registrada com sucesso")
            else:
                self.tela.mensagem_erro("Baixa excede o número de ingredientes em estoque")

    def realiza_baixa_produto(self):
        self.tela.cabecalho("Baixa de Produto")
        codigo_produto = self.tela.le_codigo("produto")
        try:
            produto = self.produtos_estoque[codigo_produto]
        except KeyError:
            self.tela.mensagem_erro("Não existe produto com este código")
        else:
            self.__controlador_central.controlador_produtos.mostra_produto(produto)
            quantidade = self.tela.le_quantidade()
            if quantidade == 0:
                self.tela.mensagem_erro("Quantidade igual a 0, baixa cancelada")
            elif quantidade <= produto.quantidade_estoque:
                self.__estoque.baixa(produto, quantidade)
                self.tela.mensagem("Baixa registrada com sucesso")
            else:
                self.tela.mensagem_erro("Baixa excede o número de produtos em estoque")

    def dados_estoque(self, estocado):
        dados = {}
        dados["nome"] = estocado.nome
        dados["quantidade"] = estocado.quantidade_estoque
        return dados

    def mostra_estoque(self, estocado, tipo = "Produto"):
        dados = self.dados_estoque(estocado)
        self.tela.mostra_estoque(dados, tipo)

    def dados_movimentacao(self, movimentacao: Movimentacao):
        dados = {}
        dados["data"] = movimentacao.data.strftime("%d/%m/%Y, %H:%M:%S")
        dados["tipo"] = movimentacao.tipo
        dados["nome_produto"] = movimentacao.movimentado.nome
        dados["quantidade"] = movimentacao.quantidade
        dados["valor_total"] = movimentacao.valor_total
        return dados

    def mostra_movimentacao(self, movimentacao: Movimentacao):
        dados = self.dados_movimentacao(movimentacao)
        self.tela.mostra_movimentacao(dados)