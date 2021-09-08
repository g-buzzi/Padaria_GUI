from telas.tela_mostra_ingrediente import TelaMostraIngrediente
from telas.tela_lista_ingrediente import TelaListaIngrediente
from controladores.controlador_abstrato import Controlador
from entidades import ingrediente
from entidades.ingrediente import Ingrediente
from telas.tela_ingrediente import TelaIngrediente


class ControladorIngredientes(Controlador):
    def __init__(self, controlador_central):
        super().__init__(TelaListaIngrediente())
        self.__ingredientes = {}
        self.__controlador_central = controlador_central
        self.__lista = []
        self.__pesquisa = False

    @property
    def ingredientes(self):
        return self.__ingredientes

    def inicia(self):
        self.abre_tela_inicial()

    def abre_tela_inicial(self, dados = None):
        switcher = {"cadastrar": self.cadastrar, "pesquisar": self.pesquisar, "lista_clique_duplo": self.mostrar, "listar": self.listar}
        self.listar()
        while True:
            self.tela = TelaListaIngrediente()
            if self.__pesquisa is not False:
                self.__lista = self.pesquisa_ingrediente_por_nome(self.__pesquisa)
            else:
                self.__lista = self.dados_ingredientes()
            botao, valores = self.tela.lista_ingredientes(self.__lista, self.__pesquisa)
            if botao == "voltar":
                break
            switcher[botao](valores)

    def listar(self, valores = None):
        self.__pesquisa = False

    def dados_ingredientes(self):
        dados = []
        for ingrediente in self.__ingredientes.values():
            dados.append([ingrediente.codigo, ingrediente.nome, ingrediente.unidade_medida, ingrediente.preco_unitario])
        return dados

    def dados_ingrediente(self, ingrediente: Ingrediente) -> dict:
        dados = {"codigo": ingrediente.codigo, "nome": ingrediente.nome, "unidade_medida": ingrediente.unidade_medida, "preco_unitario": ingrediente.preco_unitario, "quantidade_estoque": ingrediente.quantidade_estoque}
        return dados

    def pesquisar(self, valores = None):
        pesquisa = self.tela.pesquisar("Nome: ")
        if pesquisa is not None:
            dados_pesquisa = self.pesquisa_ingrediente_por_nome(pesquisa)
            self.__pesquisa = pesquisa

    def pesquisa_ingrediente_por_nome(self, pesquisa: str):
        dados = []
        for ingrediente in self.__ingredientes.values():
            if pesquisa.lower() in ingrediente.nome.lower():
                dados.append([ingrediente.codigo, ingrediente.nome, ingrediente.unidade_medida, ingrediente.preco_unitario])
        return dados

    def mostrar(self, dados):
        try:
            selecionado = dados["lista"][0]
        except IndexError:
            return
        codigo_ingrediente = self.__lista[selecionado][0]
        ingrediente = self.__ingredientes[codigo_ingrediente]
        self.tela = TelaMostraIngrediente()
        switcher = {"inicia_alteracao": self.alteracao, "remove": self.remove, "volta": False}
        while True:
            botao, dados = self.tela.mostra(self.dados_ingrediente(ingrediente))
            if switcher[botao] is False:
                break
            else:
                switcher[botao](ingrediente)
                if botao == "remove":
                    break

    def remove(self, ingrediente: Ingrediente):
        self.__ingredientes.pop(ingrediente.codigo)


    def cadastrar(self, valores = None):
        self.tela = TelaMostraIngrediente()
        switcher = {"volta": False, "cadastra": True}
        botao, dados = self.tela.cadastra()
        if switcher[botao]:
            if dados["codigo"] not in self.__ingredientes.keys():
                for ingrediente in self.__ingredientes.values():
                    if dados["nome"].lower() == ingrediente.nome.lower():
                        self.tela.mensagem_erro("Nome duplicado, tente outro nome")
                        break
                else:
                    self.__ingredientes[dados["codigo"]] = Ingrediente(dados["codigo"], dados["nome"], dados["unidade_medida"], dados["preco_unitario"])
                    self.tela.mensagem("Ingrediente cadastrado com sucesso")
                    self.listar()
            else:
                self.tela.mensagem_erro("Código já em uso, tente outro código")


    def alteracao(self, ingrediente: Ingrediente):
        dados = self.dados_ingrediente(ingrediente)
        botao, dados = self.tela.altera(dados)
        if botao == "volta":
            return
        else:
            self.altera(ingrediente, dados)
        

    def altera(self, ingrediente: Ingrediente, dados):
        if ingrediente.codigo != dados["codigo"]:
            if dados["codigo"] not in self.__ingredientes.keys():
                self.__ingredientes.pop(ingrediente.codigo)
                self.__ingredientes[dados["codigo"]] = ingrediente
                ingrediente.codigo = dados["codigo"]
            else:
                self.tela.mensagem_erro("Código em uso, as alteraçoes não serão realizadas")
                return
        if dados["nome"] != ingrediente.nome:
            for ing in self.__ingredientes.values():
                if dados["nome"].lower() == ing.nome.lower() and ing != ingrediente:
                    self.tela.mensagem_erro("Nome duplicado, alterações não serão realizadas")
                    return
        ingrediente.nome = dados["nome"]
        ingrediente.unidade_medida = dados["unidade_medida"]
        ingrediente.preco_unitario = dados["preco_unitario"] 
        self.tela.mensagem("Alterações realizadas com sucesso")


