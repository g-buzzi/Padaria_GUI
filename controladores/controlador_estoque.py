from entidades.produto import Produto
from entidades.movimentacao import Movimentacao
from controladores.controlador_abstrato import Controlador
from entidades.ingrediente import Ingrediente
from entidades.produto import Produto
from telas.tela_estoque import TelaEstoque
from datetime import datetime

class ControladorEstoque(Controlador):
    def __init__(self, controlador_central):
        super().__init__(TelaEstoque(self))
        self.__balanco = 0
        self.__movimentacoes = []
        self.__controlador_central = controlador_central

    @property
    def movimentacoes(self):
        return self.__movimentacoes

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

    def venda(self, produto: Produto, quantidade: int):
        try:
            if quantidade > produto.quantidade_estoque:
                raise ValueError
            valor_total = produto.preco_venda * quantidade
            self.__movimentacoes.append(Movimentacao("Venda", produto.nome, quantidade, valor_total))
            produto.quantidade_estoque -= quantidade
            self.__balanco += valor_total
        except ValueError:
            self.tela.mensagem_erro("Produto com estoque insuficiente")

    def compra(self, ingrediente: Ingrediente, quantidade: int):
        valor_total = ingrediente.preco_unitario * quantidade
        self.__movimentacoes.append(Movimentacao("Compra", ingrediente.nome, quantidade, valor_total))
        self.__balanco -= valor_total
        ingrediente.quantidade_estoque += quantidade

    def producao(self, produto: Produto, quantidade: int):
        self.__movimentacoes.append(Movimentacao("Produção", produto.nome, quantidade * produto.receita.rendimento, 0))
        for ingrediente, quantidade_ingrediente in produto.receita.ingredientes_receita.items(): #Não diminiu
            ingrediente.quantidade_estoque -= (quantidade * quantidade_ingrediente)
        produto.quantidade_estoque += quantidade * produto.receita.rendimento 

    def baixa(self, estoque, quantidade: int):
        self.__movimentacoes.append(Movimentacao("Baixa", estoque.nome, quantidade, 0))
        estoque.quantidade_estoque -= quantidade


    def processa_venda(self, venda):
        pass

    def lista_estoque(self):
        self.tela.cabecalho("Lista do Estoque")
        self.lista_produtos()
        self.lista_ingredientes()
        self.tela.balanco(self.__balanco)

    def lista_ingredientes(self):
        self.tela.cabecalho("Ingredientes")
        self.tela.cabecalho_estoque("Ingrediente")
        for ingrediente in self.ingredientes_estoque.values():
            self.mostra_estoque(ingrediente)

    def lista_produtos(self):
        self.tela.cabecalho("Produtos")
        self.tela.cabecalho_estoque("Produto")
        for produto in self.produtos_estoque.values():
            self.mostra_estoque(produto)

    def lista_movimentacoes(self):
        self.tela.cabecalho("Movimentações")
        for movimentacao in self.__movimentacoes:
            dados = self.dados_movimentacao(movimentacao)
            self.tela.mostra_movimentacao(dados)

    def realiza_compra(self):
        opcoes = {1: "Continuar compras", 0: "Voltar"}
        while True:
            self.tela.cabecalho("Compra")
            codigo_ingrediente = self.tela.le_codigo_ingrediente()
            try:
                ingrediente = self.ingredientes_estoque[codigo_ingrediente]
            except KeyError:
                self.tela.mensagem_erro("Não existe ingrediente com este código")
            else:
                self.__controlador_central.controlador_ingredientes.mostra_ingrediente(ingrediente)
                quantidade = self.tela.le_quantidade()
                self.compra(ingrediente, quantidade)
                self.tela.mensagem("Compra registrada com sucesso")
            opcao = self.tela.mostra_opcoes(opcoes)
            if opcao == 0:
                break

    def realiza_producao(self):
        opcoes = {1: "Continuar produção", 0: "Voltar"}
        while True:
            self.tela.cabecalho("Produção")
            codigo_produto = self.tela.le_codigo_produto()
            try:
                produto = self.produtos_estoque[codigo_produto]
            except KeyError:
                self.tela.mensagem_erro("Não existe produto com este código")
            else:
                self.__controlador_central.controlador_produtos.mostra_produto(produto)
                if produto.receita is False:
                    self.tela.mensagem_erro("O produto não possui receita")
                    return
                quantidade = self.tela.le_quantidade()
                for ingrediente, quantidade_ingrediente in produto.receita.ingredientes_receita.items():
                    if ingrediente.quantidade_estoque <= quantidade_ingrediente * quantidade:
                        self.tela.mensagem_erro("Ingredientes insuficientes para a produção")
                        break 
                else:
                    self.producao(produto, quantidade)
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
        codigo_ingrediente = self.tela.le_codigo_ingrediente()
        try:
            ingrediente = self.ingredientes_estoque[codigo_ingrediente]
        except KeyError:
            self.tela.mensagem_erro("Não existe ingrediente com este código")
        else:
            self.__controlador_central.controlador_ingredientes.mostra_ingrediente(ingrediente)
            quantidade = self.tela.le_quantidade()
            self.baixa(ingrediente, quantidade)
            self.tela.mensagem("Baixa registrada com sucesso")

    def realiza_baixa_produto(self):
        self.tela.cabecalho("Baixa de Produto")
        codigo_produto = self.tela.le_codigo_produto()
        try:
            produto = self.produtos_estoque[codigo_produto]
        except KeyError:
            self.tela.mensagem_erro("Não existe produto com este código")
        else:
            self.__controlador_central.controlador_produtos.mostra_produto(produto)
            quantidade = self.tela.le_quantidade()
            self.baixa(produto, quantidade)
            self.tela.mensagem("Baixa registrada com sucesso")

    def dados_estoque(self, estoque):
        dados = {}
        dados["nome"] = estoque.nome
        dados["quantidade"] = estoque.quantidade_estoque
        return dados

    def mostra_estoque(self, estoque, tipo = "Produto"):
        dados = self.dados_estoque(estoque)
        self.tela.mostra_estoque(dados, tipo)

    def dados_movimentacao(self, movimentacao: Movimentacao):
        dados = {}
        dados["data"] = movimentacao.data.strftime("%d/%m/%Y, %H:%M:%S")
        dados["tipo"] = movimentacao.tipo
        dados["nome_produto"] = movimentacao.nome_produto
        dados["quantidade"] = movimentacao.quantidade
        dados["valor_total"] = movimentacao.valor_total
        return dados

    def mostra_movimentacao(self, movimentacao: Movimentacao):
        dados = self.dados_movimentacao(movimentacao)
        self.tela.mostra_movimentacao(dados)