from controladores.controlador_abstrato import Controlador
from entidades import ingrediente
from entidades.ingrediente import Ingrediente
from telas.tela_ingrediente import TelaIngrediente


class ControladorIngredientes(Controlador):
    def __init__(self, controlador_central):
        super().__init__(TelaIngrediente(self))
        self.__ingredientes = {}
        self.__controlador_central = controlador_central

    @property
    def ingredientes(self):
        return self.__ingredientes

    def abre_tela_inicial(self):
        switcher = {0: False, 1: self.registra_ingrediente, 2: self.altera_ingrediente, 3: self.remove_ingrediente, 4: self.lista_ingredientes, 5: self.pesquisa_ingrediente_por_nome}
        opcoes = {1: "Cadastrar", 2: "Alterar", 3: "Remover", 4: "Listar", 5:"Pesquisar", 0: "Voltar"}
        while True:
            opcao = self.tela.mostra_opcoes(opcoes, "--------- Ingredientes ---------")
            funcao_escolhida = switcher[opcao]
            if funcao_escolhida:
                funcao_escolhida()
            else:
                break

    def registra_ingrediente(self):
        opcoes = {1: "Continuar cadastrando", 0: "Voltar"}
        while True:
            dados = self.tela.registra_ingrediente()
            if dados["codigo"] not in self.__ingredientes.keys():
                for ingrediente in self.__ingredientes.values():
                    if dados["nome"].lower() == ingrediente.nome.lower():
                        self.tela.mensagem_erro("Nome duplicado, tente outro nome")
                        break
                else:
                    self.__ingredientes[dados["codigo"]] = Ingrediente(dados["codigo"], dados["nome"], dados["unidade_medida"], dados["preco_unitario"])
                    self.tela.mensagem("Ingrediente cadastrado com sucesso")
            else:
                self.tela.mensagem_erro("Código já em uso, tente outro código")
            opcao = self.tela.mostra_opcoes(opcoes)
            if opcao == 0:
                break


    def altera_ingrediente(self):
        opcoes_alteracao = {1: "Alteração completa", 2: "Alterar código", 3: "Alterar nome", 4: "Alterar unidade de medida", 5: "Alterar preço", 0:"Finalizar alteração"}
        funcoes_alteracao = {1: self.alteracao_completa, 2: self.altera_codigo, 3: self.altera_nome, 4: self.altera_unidade, 5: self.altera_preco, 0: False}
        opcoes = {1: "Alterar outro ingrediente", 0: "Voltar"}
        while True:
            codigo = self.tela.altera_ingrediente()
            try:
                ingrediente = self.__ingredientes[codigo]
            except KeyError:
                self.tela.mensagem_erro("Nenhum ingrediente com este código existe")
                continue
            while True:
                self.mostra_ingrediente(ingrediente)
                opcao = self.tela.mostra_opcoes(opcoes_alteracao, "---- Opções de Alteração ----")
                funcao = funcoes_alteracao[opcao]
                if funcao is False:
                    break
                funcao(ingrediente)
            opcao = self.tela.mostra_opcoes(opcoes)
            if opcao == 0:
                break
        

    def alteracao_completa(self, ingrediente: Ingrediente):
        dados = self.dados_ingrediente(ingrediente)
        dados = self.tela.alteracao_completa(dados)
        if dados["nome"] != ingrediente.nome:
            for ing in self.__ingredientes.values():
                if dados["nome"].lower() == ing.nome.lower() and ing != ingrediente:
                    self.tela.mensagem_erro("Nome duplicado, alterações não serão realizadas")
                    return
        if ingrediente.codigo != dados["codigo"]:
            if dados["codigo"] not in self.__ingredientes.keys():
                self.__ingredientes.pop(ingrediente.codigo)
                self.__ingredientes[dados["codigo"]] = ingrediente
                ingrediente.codigo = dados["codigo"]
            else:
                self.tela.mensagem_erro("Código em uso, as alteraçoes não serão realizadas")
                return
        ingrediente.nome = dados["nome"]
        ingrediente.unidade_medida = dados["unidade_medida"]
        ingrediente.preco_unitario = dados["preco_unitario"] 
        self.tela.mensagem("Alterações realizadas com sucesso") 

    def altera_codigo(self, ingrediente: Ingrediente):
        novo_codigo = self.tela.altera_codigo(ingrediente.codigo)
        if novo_codigo != ingrediente.codigo:
            if novo_codigo in self.__ingredientes.keys():
                self.tela.mensagem_erro("Código em uso, as alteraçoes não serão realizadas")
                return
            else:
                self.__ingredientes.pop(ingrediente.codigo)
        self.__ingredientes[novo_codigo] = ingrediente
        ingrediente.codigo = novo_codigo
        self.tela.mensagem("Alterações realizadas com sucesso") 
                
    def altera_nome(self, ingrediente: Ingrediente):
        novo_nome = self.tela.altera_nome(ingrediente.nome)
        if novo_nome != ingrediente.nome:
            for ing in self.__ingredientes.values():
                if ing.nome.lower() == novo_nome.lower() and ing != ingrediente:
                    self.tela.mensagem_erro("Nome duplicado, alterações não serão realizadas")
                    return
        ingrediente.nome = novo_nome
        self.tela.mensagem("Alterações realizadas com sucesso") 


    def altera_unidade(self, ingrediente: Ingrediente):
        nova_unidade = self.tela.altera_unidade(ingrediente.unidade_medida)
        ingrediente.unidade_medida = nova_unidade
        self.tela.mensagem("Alterações realizadas com sucesso") 

    def altera_preco(self, ingrediente: Ingrediente):
        novo_preco = self.tela.altera_preco(ingrediente.unidade_medida, ingrediente.preco_unitario)
        ingrediente.preco_unitario = novo_preco
        self.tela.mensagem("Alterações realizadas com sucesso") 

    def remove_ingrediente(self):
        opcoes_remover = {1: "Remover ingrediente", 0: "Cancelar"} 
        opcoes = {1: "Continuar removendo", 0: "Voltar"}
        while True:
            codigo = self.tela.remove_ingrediente()
            try:
                ingrediente = self.__ingredientes[codigo]
                self.mostra_ingrediente(ingrediente)
                opcao = self.tela.mostra_opcoes(opcoes_remover, "Remover o ingrediente?")
                if opcao == 0:
                    self.tela.mensagem("Remoção cancelada")
                else:
                    self.__controlador_central.controlador_receitas.remove_ingrediente_associado_receitas(self.__ingredientes[codigo])
                    self.__ingredientes.pop(codigo)
                    self.tela.mensagem("Ingrediente removido")
            except KeyError:
                self.tela.mensagem_erro("Nenhum ingrediente com este código existe")
            opcao = self.tela.mostra_opcoes(opcoes)
            if opcao == 0:
                break

    def lista_ingredientes(self):
        self.tela.cabecalho("Listar Ingredientes")
        for ingrediente in self.__ingredientes.values():
            self.mostra_ingrediente(ingrediente)

    def pesquisa_ingrediente_por_nome(self):
        opcoes = {1: "Continuar pesquisa", 0: "Voltar"}
        while True:
            pesquisa = self.tela.pesquisa_ingrediente_por_nome()
            resultados = False
            for ingrediente in self.__ingredientes.values():
                if pesquisa in ingrediente.nome.lower():
                    resultados = True
                    self.mostra_ingrediente(ingrediente)
            if not resultados:
                self.tela.mensagem("Nenhum ingrediente com esse nome foi encontrado") 
            opcao = self.tela.mostra_opcoes(opcoes)
            if opcao == 0:
                break


    def dados_ingrediente(self, ingrediente: Ingrediente) -> dict:
        dados = {"codigo": ingrediente.codigo, "nome": ingrediente.nome, "unidade_medida": ingrediente.unidade_medida, "preco_unitario": ingrediente.preco_unitario, "quantidade_estoque": ingrediente.quantidade_estoque}
        return dados

    def mostra_ingrediente(self, ingrediente: Ingrediente):
        dados = self.dados_ingrediente(ingrediente)
        self.tela.mostra_ingrediente(dados)

    def seleciona_ingrediente_por_codigo(self, codigo: int) -> Ingrediente:
        try:
            ingrediente = self.__ingredientes[codigo]
            return ingrediente
        except KeyError:
            return False


