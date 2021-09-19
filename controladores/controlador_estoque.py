from controladores.controlador_abstrato import Controlador
from entidades.movimentacao import Movimentacao
from entidades.venda import Venda
from telas.tela_menu_estoque import TelaMenuEstoque
from telas.tela_lista_estoque import TelaListaEstoque
from telas.tela_mostra_estoque import TelaMostraEstoque
from DAOs.dao_estoque import EstoqueDAO
from controladores.controlador_ingredientes import ControladorIngredientes
from controladores.controlador_produtos import ControladorProdutos
from excecoes.not_found_exception import NotFoundException
from excecoes.input_error import InputError
from collections import defaultdict

class ControladorEstoque(Controlador):
    __instancia = None

    def __new__(cls):
        if cls.__instancia is None:
            cls.__instancia = object.__new__(cls)
        return cls.__instancia

    def __init__(self):
        super().__init__(TelaMenuEstoque())
        self.__dao = EstoqueDAO()

#============================================ Shorthands =============================

    @property
    def estoque(self):
        return self.__dao.get()

    @property
    def produtos_estoque(self):
        return ControladorProdutos().produtos

    @property
    def ingredientes_estoque(self):
        return ControladorIngredientes().ingredientes

#============================================ Menu =============================

    def abre_tela_inicial(self):
        switcher = {"ingredientes": self.lista_estoque_ingredientes, "produtos": self.lista_estoque_produtos, "movimentacoes": self.lista_movimentacoes, "volta": False}
        while True:
            self.tela = TelaMenuEstoque()
            botao, values = self.tela.menu_estoque()
            funcao_escolhida = switcher[botao]
            self.tela.close()
            if funcao_escolhida is not False:
                funcao_escolhida()
            else:
                break

#============================================ Listar Estocados =============================

    def lista_estoque_ingredientes(self):
        self.tela = TelaListaEstoque()
        while True:
            estocados = self.dados_estocados(self.ingredientes_estoque, unidade_medida= True)
            botao, values = self.tela.lista_estocados(estocados, "Ingrediente")
            if botao == "volta":
                self.tela.close()
                break

    def lista_estoque_produtos(self):
        self.tela = TelaListaEstoque()
        while True:
            estocados = self.dados_estocados(self.produtos_estoque)
            botao, values = self.tela.lista_estocados(estocados, "Produto")
            if botao == "volta":
                self.tela.close()
                break
        

#============================================ Movimentações =============================

    def lista_movimentacoes(self):
        switcher = {"compra": self.realiza_compra, "producao": self.realiza_producao, "baixa": self.realiza_baixa, "volta": False}
        while True:
            self.tela = TelaListaEstoque()
            dados = self.dados_movimentacoes()
            botao, values = self.tela.lista_movimentacoes(dados, self.estoque.balanco)
            funcao = switcher[botao]
            self.tela.close()
            if funcao is False:
                break
            else:
                funcao()

    def realiza_compra(self):
        self.tela = TelaMostraEstoque()
        dados = defaultdict(lambda: None)
        while True:
            self.tela.close()
            botao, dados = self.tela.compra(dados)
            if botao == "seleciona":
                try:
                    dados["codigo"] = ControladorIngredientes().seleciona_ingrediente()["codigo"]
                except TypeError:
                    pass
                continue
            elif botao == "compra":
                try:
                    dados = self.trata_dados(dados)
                except InputError as e:
                    self.tela.mensagem_erro(e.mensagem)
                    continue
                try:
                    ingrediente = ControladorIngredientes().seleciona_ingrediente_por_codigo(dados["codigo"])
                except NotFoundException as e:
                    self.tela.mensagem_erro(str(e))
                    continue
                if dados["quantidade"] != 0:
                    estoque = self.estoque
                    estoque.compra(ingrediente, dados["quantidade"])
                    ControladorIngredientes().alteracao_estoque(ingrediente)
                    self.__dao.add(estoque)
                    self.tela.mensagem("Compra cadastrada com sucesso")
                    self.tela.close()
                    break
                else:
                    self.tela.mensagem_erro("Quantidade igual a 0, compra cancelada!")
            else:
                self.tela.close()
                break

    def realiza_producao(self):
        self.tela = TelaMostraEstoque()
        dados = defaultdict(lambda: None)
        while True:
            self.tela.close()
            botao, dados = self.tela.producao(dados)
            if botao == "seleciona":
                try:
                    dados["codigo"] = ControladorProdutos().seleciona_produto()["codigo"]
                except TypeError:
                    pass
                continue
            elif botao == "producao":
                try:
                    dados = self.trata_dados(dados)
                except InputError as e:
                    self.tela.mensagem_erro(e.mensagem)
                    continue
                try:
                    produto = ControladorProdutos().seleciona_produto_por_codigo(dados["codigo"])
                except NotFoundException as e:
                    self.tela.mensagem_erro(str(e))
                    continue
                if dados["quantidade"] != 0:
                    for ingrediente, quantidade_ingrediente in produto.receita.ingredientes_receita.items():
                            if ingrediente.quantidade_estoque < quantidade_ingrediente * dados["quantidade"]:
                                self.tela.mensagem_erro("Ingredientes insuficientes para a produção")
                                break 
                    else:
                        estoque = self.estoque
                        estoque.producao(produto, dados["quantidade"])
                        ControladorProdutos().producao(produto)
                        self.__dao.add(estoque)
                        self.tela.mensagem("Produção cadastrada com sucesso")
                        self.tela.close()
                        break
                else:
                    self.tela.mensagem_erro("Quantidade igual a 0, produção cancelada")
            else:
                self.tela.close()
                break

    def realiza_baixa(self):
        self.tela = TelaMostraEstoque()
        dados_baixa = defaultdict(lambda: None)
        dados_baixa["tipo_ingrediente"] = True
        dados_baixa["tipo_produto"] = False
        while True:
            self.tela.close()
            botao, dados_baixa = self.tela.baixa(dados_baixa)
            if botao == "cancela":
                self.tela.close()
                break
            if botao == "seleciona":
                try:
                    if dados_baixa["tipo_ingrediente"]:
                        dados_baixa["codigo"] = ControladorIngredientes().seleciona_ingrediente()["codigo"]
                    else:
                        dados_baixa["codigo"] = ControladorProdutos().seleciona_produto()["codigo"]
                except TypeError:
                    pass
                continue
            try:
                dados_baixa = self.trata_dados(dados_baixa)
            except InputError as e:
                self.tela.mensagem_erro(e.mensagem)
                continue
            if dados_baixa["tipo_ingrediente"]:
                resultado = self.realiza_baixa_ingrediente(dados_baixa)
            else:
                resultado = self.realiza_baixa_produto(dados_baixa)
            if resultado is True:
                self.tela.close()
                break
            

    def realiza_baixa_ingrediente(self, dados_baixa):
        try:
            ingrediente = ControladorIngredientes().seleciona_ingrediente_por_codigo(dados_baixa["codigo"])
        except NotFoundException as e:
            self.tela.mensagem_erro(str(e))
        else:
            if dados_baixa["quantidade"] == 0:
                self.tela.mensagem_erro("Quantidade igual a 0, baixa cancelada")
            elif dados_baixa["quantidade"] <= ingrediente.quantidade_estoque:
                estoque = self.estoque
                estoque.baixa(ingrediente, dados_baixa["quantidade"])
                self.__dao.add(estoque)
                ControladorIngredientes().alteracao_estoque(ingrediente)
                self.tela.mensagem("Baixa registrada com sucesso")
                return True
            else:
                self.tela.mensagem_erro("Baixa excede o número de ingredientes em estoque")
        return False

    def realiza_baixa_produto(self, dados_baixa):
        try:
            produto = ControladorProdutos().seleciona_produto_por_codigo(dados_baixa["codigo"])
        except NotFoundException as e:
            self.tela.mensagem_erro(str(e))
        else:
            if dados_baixa["quantidade"] == 0:
                self.tela.mensagem_erro("Quantidade igual a 0, baixa cancelada")
            elif dados_baixa["quantidade"] <= produto.quantidade_estoque:
                estoque = self.estoque
                estoque.baixa(produto, dados_baixa["quantidade"])
                self.__dao.add(estoque)
                ControladorProdutos().alteracao_estoque(produto)
                self.tela.mensagem("Baixa registrada com sucesso")
                return True
            else:
                self.tela.mensagem_erro("Baixa excede o número de produtos em estoque")
            return False

#============================================ Lidar com dados =============================


    def dados_estocados(self, estocados, unidade_medida = False):
        dados = []
        for estocado in estocados:
            dados_estocado = [estocado.codigo]
            dados_estocado.append(estocado.nome)
            if unidade_medida is True:
                dados_estocado.append("{}{}".format(estocado.quantidade_estoque, estocado.unidade_medida))
            else:
                dados_estocado.append(estocado.quantidade_estoque)
            dados.append(dados_estocado)
        return dados

    def dados_movimentacoes(self):
        dados = []
        for movimentacao in self.estoque.movimentacoes:
            dados_movimentacao = [movimentacao.data.strftime("%d/%m/%Y, %H:%M:%S")]
            dados_movimentacao.append(movimentacao.tipo)
            dados_movimentacao.append(movimentacao.movimentado.nome)
            dados_movimentacao.append(movimentacao.quantidade)
            dados_movimentacao.append("R$ {:.2f}".format(movimentacao.valor_total))
            dados.append(dados_movimentacao)
        return dados

    def trata_dados(self, dados):
        dados["codigo"] = self.formata_int(dados["codigo"], "Código")
        dados["quantidade"] = self.formata_int(dados["quantidade"], "Quantidade")
        return dados

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

#============================================ Contato Externo =============================

    def processa_venda(self, venda: Venda):
        venda_organizada = self.possibilidade_venda(venda)
        for produto, quantidade in venda_organizada.items():
            estoque = self.estoque
            estoque.venda(produto, quantidade)
            ControladorProdutos().alteracao_estoque(produto)
            self.__dao.add(estoque)

    def possibilidade_venda(self, venda: Venda):
        produtos = defaultdict(lambda: 0)
        for item in venda.itens:
            produtos[item.produto] += item.quantidade
        for produto, quantidade in produtos.items():
            if produto.quantidade_estoque < quantidade:
                self.tela.mensagem_erro("Quantidade insuficente de {} no estoque".format(produto.nome))
                raise ValueError
        return produtos


