from excecoes.input_error import InputError
from entidades.ingrediente import Ingrediente
from controladores.controlador_abstrato import Controlador
from entidades.receita import Receita
from telas.tela_mostra_receita import TelaMostraReceita
from telas.tela_lista_receita import TelaListaReceita
from DAOs.receita_dao import ReceitaDAO
from excecoes.not_found_exception import NotFoundException
from collections import defaultdict


class ControladorReceitas(Controlador):
    def __init__(self, controlador_central: Controlador):
        super().__init__(TelaListaReceita())
        self.__dao = ReceitaDAO()
        self.__controlador_central = controlador_central
        self.__lista = []
        self.__pesquisa = False

#============================================ Listar Receitas =============================

    def abre_tela_inicial(self):
        switcher = {"cadastrar": self.cadastrar, "listar": self.listar, "pesquisar": self.pesquisar, "lista_clique_duplo": self.mostrar}
        self.listar()
        while True:
            self.tela = TelaListaReceita()
            self.tela.close()
            if self.__pesquisa is not False:
                self.__lista = self.pesquisa_por_ingrediente(self.__pesquisa[0])
            else:
                self.__lista = self.dados_receitas()
            botao, valores = self.tela.lista_receitas(self.__lista, self.__pesquisa)
            if botao == "voltar":
                self.tela.close()
                break
            switcher[botao](valores)


    def pesquisar(self, dados = None):
        self.tela = TelaListaReceita()
        codigo_ingrediente = ""
        while True:
            botao, valores = self.tela.pesquisa_receita(codigo_ingrediente)
            if botao is None or botao == "voltar":
                break
            if botao == "pesquisar":
                try:
                    codigo_ingrediente = self.formata_int(valores["codigo_ingrediente"], "Código do ingrediente")
                except InputError as e:
                    self.tela.mensagem_erro(e.mensagem)
                    continue
                try:
                    ingrediente = self.__controlador_central.controlador_ingredientes.seleciona_ingrediente_por_codigo(codigo_ingrediente)
                except NotFoundException as e:
                    self.tela.mensagem_erro(str(e))
                    continue
                self.__pesquisa = (ingrediente.codigo, ingrediente.nome)
                break
            if botao == "seleciona_ingrediente":
                dados_ingrediente = self.__controlador_central.controlador_ingredientes.seleciona_ingrediente()
                if dados_ingrediente is not None:
                    codigo_ingrediente = dados_ingrediente["codigo"]

#============================================ Receitas individuais =============================


    def cadastrar(self, dados = None):
        switcher = {"adicionar_ingrediente": self.adiciona_ingrediente_receita, "remover_ingrediente": self.remove_ingrediente_receita}
        dados_receita = defaultdict(lambda: None)
        dados_receita["ingredientes_receita"] = []
        self.tela = TelaMostraReceita()
        while True:
            self.tela.close()
            botao, valores = self.tela.cadastra(dados_receita)
            if botao == "voltar":
                self.tela.close()
                break
            dados_receita["codigo"] = valores["codigo"]
            dados_receita["tempo_preparo"] = valores["tempo_preparo"]
            dados_receita["rendimento"] = valores["rendimento"]
            dados_receita["modo_preparo"] = valores["modo_preparo"]
            if botao == "cadastrar":
                try:
                    dados_receita = self.tratar_dados(dados_receita)
                except InputError as e:
                    self.tela.mensagem_erro(e.mensagem)
                    continue
                if dados_receita["codigo"] in self.__dao.get_keys():
                    self.tela.mensagem_erro("Código já em uso!")
                    continue
                receita = Receita(dados_receita["codigo"], dados_receita["modo_preparo"], dados_receita["tempo_preparo"], dados_receita["rendimento"], dados_receita["ingredientes_receita"])
                self.__dao.add(receita)
                self.tela.mensagem("Receita cadastrada com sucesso")
                self.tela.close()
                break
            else:
                switcher[botao](dados_receita, valores)

    def mostrar(self, dados):
        try:
            selecionado = dados["lista"][0]
        except IndexError:
            return
        selecionado = self.__lista[selecionado][0]
        receita = self.__dao.get(selecionado)
        switcher = {"voltar": False, "alterar": self.alteracao, "remover": self.remove}
        while True:
            self.tela = TelaMostraReceita()
            botao, dados = self.tela.mostra(self.dados_receita(receita))
            self.tela.close()
            if switcher[botao] is False:
                break
            else:
                switcher[botao](receita)
                if botao == "remover":
                    break

    def remove(self, receita: Receita):
        self.__dao.remove(receita)

    def alteracao(self, receita: Receita):
        switcher = {"adicionar_ingrediente": self.adiciona_ingrediente_receita, "remover_ingrediente": self.remove_ingrediente_receita}
        self.tela = TelaMostraReceita()
        dados_receita = self.dados_receita(receita)
        while True:
            botao, valores = self.tela.altera(dados_receita)
            dados_receita["codigo"] = valores["codigo"]
            dados_receita["tempo_preparo"] = valores["tempo_preparo"]
            dados_receita["rendimento"] = valores["rendimento"]
            dados_receita["modo_preparo"] = valores["modo_preparo"]
            if botao == "voltar":
                self.tela.close()
                break
            elif botao == "alterar":
                if self.altera(receita, dados_receita):
                    self.tela.mensagem("Alterações realizadas com sucesso")
                    self.tela.close()
                    break
            else:
                switcher[botao](dados_receita, valores)
            self.tela.close()

    def altera(self, receita: Receita, dados):
        try:
            dados = self.tratar_dados(dados)
        except InputError as e:
            self.tela.mensagem_erro(e.mensagem)
            return False
        if receita.codigo != dados["codigo"]:
            if dados["codigo"] in self.__receitas.keys():
                self.tela.mensagem_erro("Código já em uso")
                return False
        codigo_antigo = receita.codigo
        receita.codigo = dados["codigo"]
        receita.modo_preparo = dados["modo_preparo"]
        receita.tempo_preparo = dados["tempo_preparo"]
        receita.rendimento = dados["rendimento"]
        receita.ingredientes_receita = dados["ingredientes_receita"]
        self.__dao.alter(receita, codigo_antigo)
        return True

 #============================================ Lidar com os dados =============================

    def listar(self, valores = None):
        self.__pesquisa = False

    def dados_receita(self, receita: Receita):
        dados = {}
        dados_ingredientes = []
        dados["codigo"] = receita.codigo
        if receita.produto_associado is not False:
            dados["produto_associado"] = receita.produto_associado.nome
        else:
            dados["produto_associado"] = "-----"
        dados["modo_preparo"] = receita.modo_preparo
        dados["tempo_preparo"] = receita.tempo_preparo
        dados["rendimento"] = receita.rendimento
        dados["custo_preparo"] = receita.custo_preparo
        for ingrediente, quantidade in receita.ingredientes_receita.items():
            dados_ingrediente = self.__controlador_central.controlador_ingredientes.dados_ingrediente(ingrediente)
            dados_ingrediente["quantidade"] = quantidade
            dados_ingrediente  = [dados_ingrediente["codigo"], dados_ingrediente["nome"], dados_ingrediente["quantidade"], dados_ingrediente["unidade_medida"]]
            dados_ingredientes.append(dados_ingrediente)
        dados["ingredientes_receita"] = dados_ingredientes
        return dados

    def dados_receitas(self):
        dados = []
        for receita in self.__dao.get_objects():
            dados_receita = [receita.codigo]
            if receita.produto_associado is not False:
                dados_receita.append(receita.produto_associado.nome)
            else:
                dados_receita.append("-----")
            dados_receita.append(receita.tempo_preparo)
            dados_receita.append(receita.rendimento)
            dados_receita.append(receita.custo_preparo)
            dados.append(dados_receita)
        return dados

    def remove_ingrediente_receita(self, dados_receita: dict, valores: dict):
        try:
            dados_receita["ingredientes_receita"].pop(valores["lista"][0])
        except IndexError:
            pass

    def adiciona_ingrediente_receita(self, dados_receita: dict, valores: dict):
        dados_ingrediente_receita = defaultdict(lambda: None)
        while True:
            botao, valores = self.tela.adiciona_ingrediente_receita(dados_ingrediente_receita)
            if botao == "cancelar" or botao == None:
                break
            elif botao == "seleciona_ingrediente":
                try:
                    codigo_ingrediente = self.__controlador_central.controlador_ingredientes.seleciona_ingrediente()["codigo"]
                    dados_ingrediente_receita["codigo_ingrediente"] = codigo_ingrediente
                except IndexError:
                    continue
            else:
                try:
                    codigo_ingrediente = self.formata_int(valores["codigo_ingrediente"], "Código do ingrediente")
                    quantidade = self.formata_float(valores["quantidade"], "Quantidade")
                except InputError as e:
                    self.tela.mensagem_erro(e.mensagem)
                    continue
                try:
                    ingrediente = self.__controlador_central.controlador_ingredientes.seleciona_ingrediente_por_codigo(codigo_ingrediente)
                except NotFoundException as e:
                    self.tela.mensagem_erro(str(e))
                for valores in dados_receita["ingredientes_receita"]:
                    if valores[0] == ingrediente.codigo:
                        self.tela.mensagem_erro("Este ingrediente já está associado à receita")
                        break
                else:
                    dados_receita["ingredientes_receita"].append([ingrediente.codigo, ingrediente.nome, quantidade, ingrediente.unidade_medida])
                    break

    def tratar_dados(self, dados: dict):
        dados["codigo"] = self.formata_int(dados["codigo"], "Código")
        dados["tempo_preparo"] = self.formata_int(dados["tempo_preparo"], "Tempo de preparo")
        dados["rendimento"] = self.formata_int(dados["rendimento"], "Rendimento")
        dados["modo_preparo"] = self.formata_string(dados["modo_preparo"])
        ingredientes_receita = {}
        for valores in dados["ingredientes_receita"]:
            ingrediente = self.__controlador_central.controlador_ingredientes.seleciona_ingrediente_por_codigo(valores[0])
            ingredientes_receita[ingrediente] = valores[2]
        dados["ingredientes_receita"] = ingredientes_receita
        return dados

    def pesquisa_por_ingrediente(self, codigo_ingrediente: int):
        try:
            ingrediente = self.__controlador_central.controlador_ingredientes.seleciona_ingrediente_por_codigo(codigo_ingrediente)
        except NotFoundException as e:
            self.tela.mensagem_erro(e)
            self.__pesquisa = False
        else:
            dados = []
            for receita in self.__dao.get_objects():
                for ingrediente_receita in receita.ingredientes_receita.keys():
                    if ingrediente_receita.codigo == ingrediente.codigo:
                        break
                else:
                    continue
                dados_receita = [receita.codigo]
                if receita.produto_associado is not False:
                    dados_receita.append(receita.produto_associado.nome)
                else:
                    dados_receita.append("-----")
                dados_receita.append(receita.tempo_preparo)
                dados_receita.append(receita.rendimento)
                dados_receita.append(receita.custo_preparo)
                dados.append(dados_receita)
            return dados
            
#============================================ Contato externo =============================

    def seleciona_receita(self) -> dict:
        self.tela = TelaListaReceita()
        lista = self.dados_receitas()
        posicao = self.tela.seleciona_receita(lista)
        if posicao is None:
            return None
        try:
            receita = self.__dao.get(lista[posicao][0])
            return self.dados_receita(receita)
        except NotFoundException:
            return None

    def seleciona_receita_por_codigo(self, codigo: int):
        try:
            return self.__dao.get(codigo)
        except KeyError:
            return None
