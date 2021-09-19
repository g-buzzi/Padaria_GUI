from controladores.controlador_abstrato import Controlador
from entidades.produto import Produto
from telas.tela_lista_produto import TelaListaProduto
from telas.tela_mostra_produto import TelaMostraProduto
from DAOs.dao_produto import ProdutoDAO
import controladores.controlador_receitas
from excecoes.duplicated_exception import DuplicatedException
from excecoes.not_found_exception import NotFoundException
from excecoes.input_error import InputError
from collections import defaultdict
import textwrap

class ControladorProdutos(Controlador):
    instancia = None

    def __new__(cls):
        if cls.instancia is None:
            cls.instancia = super().__new__(cls)
        return cls.instancia

    def __init__(self):
        super().__init__(TelaListaProduto())
        self.__dao = ProdutoDAO()
        self.__pesquisa = False

#============================================ Listar Produtos =============================

    def abre_tela_inicial(self):
        switcher = {"cadastrar": self.cadastrar, "pesquisar": self.pesquisar, "lista_clique_duplo": self.mostrar, "listar": self.listar}
        self.listar()
        while True:
            self.tela.close()
            self.tela = TelaListaProduto()
            if self.__pesquisa is not False:
                self.__lista = self.pesquisa_produto_por_nome(self.__pesquisa)
            else:
                self.__lista = self.dados_produtos()
            botao, valores = self.tela.lista_produtos(self.__lista, self.__pesquisa)
            if botao == "voltar":
                self.tela.close()
                break
            switcher[botao](valores)
            self.tela.close()

    def pesquisar(self, valores = None):
        pesquisa = self.tela.pesquisar("Nome: ")
        try:
            if pesquisa is not None:
                pesquisa = self.formata_string(pesquisa)
                self.__pesquisa = pesquisa
        except InputError as e:
            self.tela.mensagem_erro(e.mensagem)

#============================================ Produtos individuais =============================

    def cadastrar(self, dados = None):
        dados_produto = defaultdict(lambda: None)
        self.tela = TelaMostraProduto()
        while True:
            self.tela.close()
            botao, dados_produto = self.tela.cadastra(dados_produto)
            if botao == "volta":
                break
            elif botao == "seleciona_receita":
                dados_receita = controladores.controlador_receitas.ControladorReceitas().seleciona_receita()
                if dados_receita is not None:
                    dados_produto["codigo_receita"] = dados_receita["codigo"]
            else:
                try:
                    dados_produto = self.tratar_dados(dados_produto)
                except InputError as e:
                    self.tela.mensagem_erro(e.mensagem)
                    continue
                try:
                    self.__dao.get(dados_produto["codigo"])
                except (NotFoundException, KeyError):
                    pass
                else:
                    self.tela.mensagem_erro("O código já está em uso!")
                    continue
                if dados_produto["codigo_receita"] is not False:
                    try:
                        receita = controladores.controlador_receitas.ControladorReceitas().seleciona_receita_por_codigo(dados_produto["codigo_receita"])
                    except NotFoundException as e:
                        self.tela.mensagem_erro(str(e))
                else:
                    receita = False
                for produto in self.__dao.get_objects():
                    if dados_produto["nome"].lower() == produto.nome.lower():
                        self.tela.mensagem_erro("Nome duplicado")
                        break
                else:
                    produto = Produto(dados_produto["codigo"], dados_produto["nome"], dados_produto["preco_venda"], dados_produto["descricao"], receita)
                    if receita is not False:
                        try:
                            controladores.controlador_receitas.ControladorReceitas().associar_produto_receita(receita, produto)
                        except DuplicatedException as e:
                            self.tela.mensagem_erro(str(e))
                            continue
                    self.__dao.add(produto)
                    self.tela.mensagem("Produto cadastrado com sucesso")
                    self.tela.close()
                    break

    def mostrar(self, dados):
        try:
            selecionado = dados["lista"][0]
        except IndexError:
            return
        selecionado = self.__lista[selecionado][0]
        produto = self.__dao.get(selecionado)
        switcher = {"volta": False, "altera": self.alteracao, "remove": self.remove}
        while True:
            self.tela = TelaMostraProduto()
            botao, dados = self.tela.mostra(self.dados_produto(produto))
            self.tela.close()
            if switcher[botao] is False:
                break
            else:
                switcher[botao](produto)
                if botao == "remove":
                    break


    def alteracao(self, produto: Produto):
        self.tela = TelaMostraProduto()
        dados = self.dados_produto(produto)
        while True:
            botao, dados = self.tela.altera(dados)
            if botao == "cancela":
                self.tela.close()
                break
            elif botao == "seleciona_receita":
                dados_receita = controladores.controlador_receitas.ControladorReceitas().seleciona_receita()
                if dados_receita is not None:
                    dados["codigo_receita"] = dados_receita["codigo"]
            else:
                if self.altera(produto, dados):
                    self.tela.mensagem("Alterações realizadas com sucesso")
                    self.tela.close()
                    break
            self.tela.close()

    def altera(self, produto: Produto, dados):
        try:
            dados = self.tratar_dados(dados)
        except InputError as e:
            self.tela.mensagem_erro(e.mensagem)
            return False
        if dados["codigo"] != produto.codigo:
            if dados["codigo"] in self.__dao.get_keys():
                self.tela.mensagem_erro("Código já em utilização")
                return
        if dados["nome"].lower() != produto.nome.lower():
            for prod in self.__dao.get_objects():
                if dados["nome"].lower() == prod.nome.lower() and produto.codigo != prod.codigo:
                    self.tela.mensagem_erro("Nome já em utilização")
                    return
        if dados["codigo_receita"] is False:
            receita = False
        else:
            try:
                receita = controladores.controlador_receitas.ControladorReceitas().seleciona_receita_por_codigo(dados["codigo_receita"])
            except NotFoundException as e:
                self.tela.mensagem_erro(str(e))
                return False
        if receita is not False and receita.produto_associado is not False and (produto.receita is False or receita.codigo != produto.receita.codigo):
            self.tela.mensagem_erro("Receita já associada a um produto")
            return False
        codigo_antigo = produto.codigo
        produto.codigo = dados["codigo"]
        produto.nome = dados["nome"]
        produto.preco_venda = dados["preco_venda"]
        produto.descricao = dados["descricao"]
        if produto.receita is not False:
            controladores.controlador_receitas.ControladorReceitas().remover_produto_associado(produto.receita)
        produto.receita = receita
        if receita is not False:
            controladores.controlador_receitas.ControladorReceitas().associar_produto_receita(receita, produto)
        self.__dao.alter(produto, codigo_antigo)
        return True


    def remove(self, produto: Produto):
        self.__dao.remove(produto)
        if produto.receita is not False:
            controladores.controlador_receitas.ControladorReceitas().remover_produto_associado(produto.receita)


 #============================================ Lidar com os dados =============================

 
    def listar(self, dados = None):
        self.__pesquisa = False

    def dados_produto(self, produto: Produto):
        dados = {}
        dados["codigo"] = produto.codigo
        dados["nome"] = produto.nome
        dados["preco_venda"] = produto.preco_venda
        dados["descricao"] = produto.descricao
        if produto.receita:
            dados["codigo_receita"] = produto.receita.codigo
            dados["custo_unitario"] = produto.custo_unitario
        else:
            dados["codigo_receita"] = "--"
            dados["custo_unitario"] = "--"
        return dados

    def dados_produtos(self):
        dados = []
        for produto in self.__dao.get_objects():
            dados_produto = []
            dados_produto.append(produto.codigo)
            dados_produto.append(produto.nome)
            dados_produto.append(textwrap.shorten(produto.descricao, 20, placeholder=" ..."))
            if produto.receita:
                dados_produto.append("R$ {:.2f}".format(produto.custo_unitario))
            else:
                dados_produto.append("----")
            dados_produto.append("R$ {:.2f}".format(produto.preco_venda))
            dados.append(dados_produto)
        return dados

    def tratar_dados(self, dados: dict):
        dados["codigo"] = self.formata_int(dados["codigo"], "Código do produto")
        dados["nome"] = self.formata_string(dados["nome"])
        dados["preco_venda"] = self.formata_float(dados["preco_venda"], "Preço de Venda")
        dados["descricao"] = self.formata_string(dados["descricao"])
        if dados["codigo_receita"] == "":
            dados["codigo_receita"] = False
        else:
            dados["codigo_receita"] = self.formata_int(dados["codigo_receita"], "Código da receita")
        return dados

    def pesquisa_produto_por_nome(self, pesquisa: str):
        dados = []
        for produto in self.__dao.get_objects():
            if pesquisa in produto.nome.lower():
                dados_produto = []
                dados_produto.append(produto.codigo)
                dados_produto.append(produto.nome)
                dados_produto.append(textwrap.shorten(produto.descricao, 20, placeholder=" ..."))
                if produto.receita:
                    dados_produto.append("R$ {:.2f}".format(produto.custo_unitario))
                else:
                    dados_produto.append("----")
                dados_produto.append("R$ {:.2f}".format(produto.preco_venda))
                dados.append(dados_produto)
        return dados

#============================================ Contato externo =============================

    @property
    def produtos(self):
        return self.__dao.get_objects()

    def producao(self, produto: Produto):
        self.__dao.producao(produto)

    def alteracao_estoque(self, produto: Produto):
        self.__dao.add(produto)

    def seleciona_produto(self) -> dict:
        self.tela = TelaListaProduto()
        lista = self.dados_produtos()
        posicao = self.tela.seleciona_produto(lista)
        if posicao is None:
            return None
        try:
            produto = self.__dao.get(lista[posicao][0])
            return self.dados_produto(produto)
        except NotFoundException:
            return None
            
    def seleciona_produto_por_codigo(self, codigo: int):
        return self.__dao.get(codigo)

    def remover_receita_associada(self, produto: Produto):
        produto.remove_receita()
        self.__dao.add(produto)