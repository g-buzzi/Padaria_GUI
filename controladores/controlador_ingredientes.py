from controladores.controlador_abstrato import Controlador
from entidades.ingrediente import Ingrediente
from telas.tela_ingrediente import TelaIngrediente



class ControladorIngredientes(Controlador):
    def __init__(self):
        super().__init__(TelaIngrediente(self))
        self.__ingredientes = {}

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
                else:
                    self.__ingredientes[dados["codigo"]] = Ingrediente(dados["nome"], dados["unidade_medida"], dados["preco_unitario"])
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
            dados = self.dados_ingrediente(codigo)
            if dados is False:
                self.tela.mensagem_erro("Nenhum ingrediente com este código existe")
                continue
            while True:
                self.tela.mostra_ingrediente(dados)
                opcao = self.tela.mostra_opcoes(opcoes_alteracao, "---- Opções de Alteração ----")
                funcao = funcoes_alteracao[opcao]
                if funcao is False:
                    break
                codigo = funcao(codigo)
                dados = self.dados_ingrediente(codigo)
            opcao = self.tela.mostra_opcoes(opcoes)
            if opcao == 0:
                break
        

    def alteracao_completa(self, codigo: int):
        dados = self.dados_ingrediente(codigo)
        dados = self.tela.alteracao_completa(dados)
        ingrediente = self.__ingredientes[codigo]
        if dados["nome"] != ingrediente.nome:
            for ing in self.__ingredientes.values():
                if dados["nome"].lower() == ing.nome.lower():
                    self.tela.mensagem_erro("Nome duplicado, alterações não serão realizadas")
                    return codigo
        if codigo != dados["codigo"]:
            if dados["codigo"] not in self.__ingredientes.keys():
                self.__ingredientes.pop(codigo)
                self.__ingredientes[dados["codigo"]] = ingrediente
                ingrediente.nome = dados["nome"]
                ingrediente.unidade_medida = dados["unidade_medida"]
                ingrediente.preco_unitario = dados["preco_unitario"]
                self.tela.mensagem("Alterações realizadas com sucesso")
                return dados["codigo"]
            else:
                self.tela.mensagem_erro("Código em uso, as alteraçoes não serão realizadas")
                return codigo
        else:
            ingrediente.nome = dados["nome"]
            ingrediente.unidade_medida = dados["unidade_medida"]
            ingrediente.preco_unitario = dados["preco_unitario"] 
            self.tela.mensagem("Alterações realizadas com sucesso") 
            return codigo

    def altera_codigo(self, codigo: int):
        novo_codigo = self.tela.altera_codigo(codigo)
        ingrediente = self.__ingredientes[codigo]
        if novo_codigo != codigo:
            if novo_codigo in self.__ingredientes.keys():
                self.tela.mensagem_erro("Código em uso, as alteraçoes não serão realizadas")
                return codigo
            else:
                self.__ingredientes.pop(codigo)
        self.__ingredientes[novo_codigo] = ingrediente
        return novo_codigo
                
    def altera_nome(self, codigo: int):
        ingrediente = self.__ingredientes[codigo]
        novo_nome = self.tela.altera_nome(ingrediente.nome)
        if novo_nome != ingrediente.nome:
            for ing in self.__ingredientes.values():
                if ing.nome.lower() == novo_nome.lower():
                    self.tela.mensagem_erro("Nome duplicado, alterações não serão realizadas")
                    return codigo
        ingrediente.nome = novo_nome
        return codigo


    def altera_unidade(self, codigo: int):
        ingrediente = self.__ingredientes[codigo]
        nova_unidade = self.tela.altera_unidade(ingrediente.unidade_medida)
        ingrediente.unidade_medida = nova_unidade
        return codigo

    def altera_preco(self, codigo: int):
        ingrediente = self.__ingredientes[codigo]
        novo_preco = self.tela.altera_preco(ingrediente.unidade_medida, ingrediente.preco_unitario)
        ingrediente.preco_unitario = novo_preco
        return codigo

    def remove_ingrediente(self):
        opcoes_remover = {1: "Remover ingrediente", 0: "Cancelar"} 
        opcoes = {1: "Continuar removendo", 0: "Voltar"}
        while True:
            codigo = self.tela.remove_ingrediente()
            try:
                dados = self.dados_ingrediente(codigo)
                if dados is False:
                    raise KeyError
                self.tela.mostra_ingrediente(dados)
                opcao = self.tela.mostra_opcoes(opcoes_remover, "Remover o ingrediente?")
                if opcao == 0:
                    self.tela.mensagem("Remoção cancelada")
                else:
                    self.__ingredientes.pop(codigo)
                    self.tela.mensagem("Ingrediente removido")
            except KeyError:
                self.tela.mensagem_erro("Nenhum ingrediente com este código existe")
            opcao = self.tela.mostra_opcoes(opcoes)
            if opcao == 0:
                break

    def lista_ingredientes(self):
        dados_ingredientes = []
        for codigo in self.__ingredientes.keys():
            dados = self.dados_ingrediente(codigo)
            dados_ingredientes.append(dados)
        self.tela.lista_ingredientes(dados_ingredientes)

    def pesquisa_ingrediente_por_nome(self):
        opcoes = {1: "Continuar pesquisa", 0: "Voltar"}
        while True:
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
                self.tela.mensagem("Nenhum ingrediente com esse nome foi encontrado") 
            opcao = self.tela.mostra_opcoes(opcoes)
            if opcao == 0:
                break


    def dados_ingrediente(self, codigo: int):
        try:
            ingrediente = self.__ingredientes[codigo]
        except KeyError:
            return False
        dados = {"codigo": codigo, "nome": ingrediente.nome, "unidade_medida": ingrediente.unidade_medida, "preco_unitario": ingrediente.preco_unitario, "quantidade_estoque": ingrediente.quantidade_estoque}
        return dados


