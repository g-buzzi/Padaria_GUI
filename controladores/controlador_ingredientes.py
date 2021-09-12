from excecoes.not_found_exception import NotFoundException
from PySimpleGUI.PySimpleGUI import No
from excecoes.input_error import InputError
from telas.tela_mostra_ingrediente import TelaMostraIngrediente
from telas.tela_lista_ingrediente import TelaListaIngrediente
from controladores.controlador_abstrato import Controlador
from DAOs.dao_ingrediente import IngredienteDAO
from entidades.ingrediente import Ingrediente



class ControladorIngredientes(Controlador):
    def __init__(self, controlador_central):
        super().__init__(TelaListaIngrediente())
        self.__dao = IngredienteDAO()
        self.__controlador_central = controlador_central
        self.__lista = []
        self.__pesquisa = False

    def inicia(self):
        self.abre_tela_inicial()

#============================================ Listar Ingredientes =============================

    def abre_tela_inicial(self, dados = None):
        switcher = {"cadastrar": self.cadastrar, "pesquisar": self.pesquisar, "lista_clique_duplo": self.mostrar, "listar": self.listar}
        self.listar()
        while True:
            self.tela.close()
            self.tela = TelaListaIngrediente()
            if self.__pesquisa is not False:
                self.__lista = self.pesquisa_ingrediente_por_nome(self.__pesquisa)
            else:
                self.__lista = self.dados_ingredientes()
            botao, valores = self.tela.lista_ingredientes(self.__lista, self.__pesquisa)
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


#============================================ Ingredientes individuais =============================

    def cadastrar(self, valores = None):
        self.tela = TelaMostraIngrediente()
        switcher = {"volta": False, "cadastra": True}
        dados = None
        while True:
            if dados is None:
                botao, dados = self.tela.cadastra(unidades_medida= self.unidades_medida())
            else:
                botao, dados = self.tela.cadastra(dados, self.unidades_medida())
            if switcher[botao] is not False:
                try:
                    dados = self.tratar_dados(dados)
                except InputError:
                    self.tela.close()
                    continue
                if dados["codigo"] not in self.__dao.get_keys():
                    for ingrediente in self.__dao.get_objects():
                        if dados["nome"].lower() == ingrediente.nome.lower():
                            self.tela.mensagem_erro("Nome duplicado, tente outro nome")
                            self.tela.close()
                            break
                    else:
                        self.__dao.add(Ingrediente(dados["codigo"], dados["nome"], dados["unidade_medida"], dados["preco_unitario"]))
                        self.tela.mensagem("Ingrediente cadastrado com sucesso")
                        self.tela.close()
                        self.listar()
                        break
                    continue
                else:
                    self.tela.mensagem_erro("Código já em uso, tente outro código")
                    self.tela.close()
                    continue
            else:
                self.tela.close()
                break

    def mostrar(self, dados):
        try:
            selecionado = dados["lista"][0]
        except IndexError:
            return
        codigo_ingrediente = self.__lista[selecionado][0]
        ingrediente = self.__dao.get(codigo_ingrediente)
        switcher = {"inicia_alteracao": self.alteracao, "remove": self.remove, "volta": False}
        while True:
            self.tela = TelaMostraIngrediente()
            botao, dados = self.tela.mostra(self.dados_ingrediente(ingrediente))
            self.tela.close()
            if switcher[botao] is False:
                break
            else:
                switcher[botao](ingrediente)
                if botao == "remove":
                    break

    def remove(self, ingrediente: Ingrediente):
        self.__dao.remove(ingrediente)

    def alteracao(self, ingrediente: Ingrediente):
        self.tela = TelaMostraIngrediente()
        dados = self.dados_ingrediente(ingrediente)
        while True:
            botao, dados = self.tela.altera(dados, self.unidades_medida())
            if botao == "volta":
                self.tela.close()
                break
            else:
                if self.altera(ingrediente, dados):
                    self.tela.mensagem("Alterações realizadas com sucesso")
                    self.tela.close()
                    break
            self.tela.close()

    def altera(self, ingrediente: Ingrediente, dados):
        try:
            dados = self.tratar_dados(dados)
        except InputError:
            return False
        if ingrediente.codigo != dados["codigo"]:
            if dados["codigo"] in self.__dao.get_keys():
                self.tela.mensagem_erro("Código em uso, as alteraçoes não serão realizadas")
                return False
        if dados["nome"] != ingrediente.nome:
            for ing in self.__dao.get_objects():
                if dados["nome"].lower() == ing.nome.lower() and ing != ingrediente:
                    self.tela.mensagem_erro("Nome duplicado, alterações não serão realizadas")
                    return False
        codigo_antigo = ingrediente.codigo
        ingrediente.codigo = dados["codigo"]
        ingrediente.nome = dados["nome"]
        ingrediente.unidade_medida = dados["unidade_medida"]
        ingrediente.preco_unitario = dados["preco_unitario"] 
        self.__dao.alter(ingrediente, codigo_antigo)
        return True

#============================================ Lidar com os dados =============================

    def listar(self, valores = None):
        self.__pesquisa = False

    def dados_ingredientes(self):
        dados = []
        for ingrediente in self.__dao.get_objects():
            dados.append([ingrediente.codigo, ingrediente.nome, ingrediente.unidade_medida, "{:.2f}".format(ingrediente.preco_unitario)])
        return dados

    def dados_ingrediente(self, ingrediente: Ingrediente) -> dict:
        dados = {"codigo": ingrediente.codigo, "nome": ingrediente.nome, "unidade_medida": ingrediente.unidade_medida,"preco_unitario": "{:.2f}".format(ingrediente.preco_unitario), "quantidade_estoque": ingrediente.quantidade_estoque}
        return dados

    def pesquisa_ingrediente_por_nome(self, pesquisa: str):
        dados = []
        for ingrediente in self.__dao.get_objects():
            if pesquisa.lower() in ingrediente.nome.lower():
                dados.append([ingrediente.codigo, ingrediente.nome, ingrediente.unidade_medida, "{:.2f}".format(ingrediente.preco_unitario)])
        return dados

    def tratar_dados(self, dados: dict):
        try:
            dados["codigo"] = self.formata_int(dados["codigo"], "Código")
            dados["nome"] = self.formata_string(dados["nome"])
            dados["unidade_medida"] = self.formata_string(dados["unidade_medida"])
            dados["preco_unitario"] = self.formata_float(dados["preco_unitario"], "Preço Unitário")
            return dados
        except InputError as e:
            self.tela.mensagem_erro(e.mensagem)
            raise InputError()

    def unidades_medida(self):
        unidades = [ingrediente.unidade_medida for ingrediente in self.__dao.get_objects()]
        unidades = set(unidades)
        unidades = list(unidades)
        return unidades

#============================================ Contato externo =============================

    def seleciona_ingrediente(self) -> dict:
        self.tela = TelaListaIngrediente()
        lista = self.dados_ingredientes()
        posicao = self.tela.seleciona_ingrediente(lista)
        if posicao is None:
            return None
        try:
            ingrediente = self.__dao.get(lista[posicao][0])
            return self.dados_ingrediente(ingrediente)
        except NotFoundException:
            return None

    def seleciona_ingrediente_por_codigo(self, codigo: int):
        return self.__dao.get(codigo)

