from controladores.controlador_abstrato import Controlador
from entidades.ingrediente import Ingrediente
from telas.tela_ingrediente import TelaIngrediente


class ControladorIngredientes(Controlador):
    def __init__(self):
        super().__init__(TelaIngrediente(self))
        self.__ingredientes = {}

    def abre_tela_inicial(self):
        switcher = {0: "Give TypeError", 1: self.registra_ingrediente, 2: self.altera_ingrediente, 3: self.remove_ingrediente, 4: self.lista_ingredientes, 5: self.pesquisa_ingrediente_por_nome}
        while True:
            opcao = self.tela.mostra_opcoes()
            funcao_escolhida = switcher[opcao]
            try:
                funcao_escolhida()
            except TypeError:
                break

    def registra_ingrediente(self):
        while True:
            dados = self.tela.registra_ingrediente()
            if dados["codigo"] not in self.__ingredientes.keys():
                for ingrediente in self.__ingredientes.values():
                    if dados["nome"].lower() == ingrediente.nome.lower():
                        self.tela.mensagem_erro("Nome duplicado, tente outro nome")
                        break
                else:
                    self.__ingredientes[dados["codigo"]] = Ingrediente(dados["nome"], dados["unidade_medida"], dados["preco_unitario"])
                    self.tela.mensagem("Ingrediente cadastrado com sucesso")
                    break
            else:
                self.tela.mensagem_erro("Código já em uso, tente outro código")

    def altera_ingrediente(self):
        codigo, dados = self.tela.altera_ingrediente()
        nome_valido = True
        if dados["nome"] != self.__ingredientes[codigo].nome:
            for ingrediente in self.__ingredientes.values():
                if dados["nome"].lower() == ingrediente.nome.lower():
                    self.tela.mensagem_erro("Nome duplicado, alterações não serão realizadas")
                    nome_valido = False
                    break
        if nome_valido:
            ingrediente = self.__ingredientes[codigo]
            if codigo != dados["codigo"]:
                if dados["codigo"] not in self.__ingredientes.keys():
                    self.__ingredientes.pop(codigo)
                    self.__ingredientes[dados["codigo"]] = ingrediente
                    ingrediente.nome = dados["nome"]
                    ingrediente.unidade_medida = dados["unidade_medida"]
                    ingrediente.preco_unitario = dados["preco_unitario"]
                    self.tela.mensagem("Alterações realizadas com sucesso")
                else:
                    self.tela.mensagem_erro("Código em uso, as alteraçoes não serão realizadas")
            else:
                ingrediente.nome = dados["nome"]
                ingrediente.unidade_medida = dados["unidade_medida"]
                ingrediente.preco_unitario = dados["preco_unitario"] 
                self.tela.mensagem("Alterações realizadas com sucesso") 

    def remove_ingrediente(self):
        codigo = self.tela.remove_ingrediente()
        if codigo:
            self.__ingredientes.pop(codigo)

    def lista_ingredientes(self):
        dados_ingredientes = []
        for codigo, ingrediente in self.__ingredientes.items():
            dados = self.dados_ingrediente(codigo)
            dados_ingredientes.append(dados)
        self.tela.lista_ingredientes(dados_ingredientes)

    def pesquisa_ingrediente_por_nome(self):
        pesquisa = self.tela.pesquisa_ingrediente_por_nome()
        resultados = []
        for codigo in self.__ingredientes.keys():
            if pesquisa in self.__ingredientes[codigo].nome.lower():
                dados = self.dados_ingrediente(codigo)
                resultados.append(dados)
        if resultados:
            for dados in resultados:
                self.tela.mostra_ingrediente(dados)
        else:
            self.tela.mensagem_erro("Nenhum ingrediente com esse nome foi encontrado") 

    def dados_ingrediente(self, codigo: int):
        try:
            ingrediente = self.__ingredientes[codigo]
        except IndexError:
            return None
        dados = {"codigo": codigo, "nome": ingrediente.nome, "unidade_medida": ingrediente.unidade_medida, "preco_unitario": ingrediente.preco_unitario, "quantidade_estoque": ingrediente.quantidade_estoque}
        return dados


