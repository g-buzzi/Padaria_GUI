from entidades.ingrediente import Ingrediente
from controladores.controlador_abstrato import Controlador
from entidades.receita import Receita
from telas.tela_receita import TelaReceita



class ControladorReceitas(Controlador):
    def __init__(self, controlador_central: Controlador):
        super().__init__(TelaReceita(self))
        self.__receitas = {}
        self.__controlador_central = controlador_central

    @property
    def receitas(self):
        return self.__receitas

    def abre_tela_inicial(self):
        switcher = {0: False, 1: self.registra_receita, 2: self.altera_receita, 3: self.remove_receita, 4: self.lista_receitas, 5: self.pesquisa_por_ingrediente}
        opcoes = {1: "Cadastrar", 2: "Alterar", 3: "Remover", 4: "Listar", 5: "Pesquisar", 0: "Voltar"}
        while True:
            opcao = self.tela.mostra_opcoes(opcoes, "--------- Receitas ---------")
            funcao_escolhida = switcher[opcao]
            if funcao_escolhida:
                funcao_escolhida()
            else:
                break

    def registra_receita(self):
        opcoes = {1: "Continuar cadastrando", 0: "Voltar"}
        opcoes_ingredientes = {1: "Adicionar Ingrediente à receita", 2: "Remover Ingrediente da receita", 0: "Finalizar"}
        switcher = {1: self.inclui_ingrediente_receita, 2: self.remove_ingrediente_receita, 0: False}
        while True:
            dados = self.tela.registra_receita()
            if dados["codigo"] not in self.__receitas.keys():
                receita = Receita(dados["codigo"], dados["modo_preparo"], dados["tempo_preparo"], dados["rendimento"])
                self.__receitas[dados["codigo"]] = receita
                self.tela.mensagem("Receita cadastrada com sucesso")
                while True:
                    opcao = self.tela.mostra_opcoes(opcoes_ingredientes)
                    funcao = switcher[opcao]
                    if funcao is False:
                        break
                    funcao(receita)
            else:
                self.tela.mensagem_erro("Código já em uso")
            opcao = self.tela.mostra_opcoes(opcoes)
            if opcao == 0:
                break

    
    def inclui_ingrediente_receita(self, receita: Receita):
        codigo_ingrediente = self.tela.le_codigo_ingrediente()
        ingrediente = self.__controlador_central.controlador_ingredientes.seleciona_ingrediente_por_codigo(codigo_ingrediente)
        if ingrediente:
            self.__controlador_central.controlador_ingredientes.mostra_ingrediente(ingrediente)
            if ingrediente not in self.__receitas[receita.codigo].ingredientes_receita.keys():
                quantidade = self.tela.le_quantidade_ingrediente()
                if quantidade != 0:
                    self.__receitas[receita.codigo].inclui_ingrediente(ingrediente, quantidade)
                    self.tela.mensagem("Ingrediente adicionado com sucesso")
                else:
                    self.tela.mensagem_erro("Quantidade igual a 0, inclusão cancelada")
            else:
                self.tela.mensagem_erro("Ingrediente já adicionado")
        else:
            self.tela.mensagem_erro("Não existe ingrediente com este código")

    def remove_ingrediente_receita(self, receita: Receita):
        codigo_ingrediente = self.tela.remove_ingrediente_receita()
        ingrediente = self.__controlador_central.controlador_ingredientes.seleciona_ingrediente_por_codigo(codigo_ingrediente)
        if ingrediente:
            if ingrediente in receita.ingredientes_receita.keys():
                receita.ingredientes_receita.pop(ingrediente)
                self.tela.mensagem("Ingrediente removido com sucesso")
            else:
                self.tela.mensagem_erro("Nenhum ingrediente com este código associado à receita")
        else:
            self.tela.mensagem_erro("Não existe ingrediente com este código")


    def altera_receita(self):
        opcoes_alteracao = {1: "Alteração completa", 2: "Alterar código", 3: "Alterar modo de preparo", 4: "Alterar tempo de preparo", 5: "Alterar rendimento", 6: "Alterar ingredientes", 0:"Finalizar alteração"}
        funcoes_alteracao = {1: self.alteracao_completa, 2: self.altera_codigo, 3: self.altera_modo_preparo, 4: self.altera_tempo_preparo, 5: self.altera_rendimento, 6: self.altera_ingredientes, 0: False}
        opcoes = {1: "Alterar outra receita", 0: "Voltar"}
        while True:
            codigo = self.tela.altera_receita()
            try:
                receita = self.__receitas[codigo]
            except KeyError:
                self.tela.mensagem_erro("Nenhuma receita com este código existe")
                continue
            while True:
                self.mostra_receita(receita)
                opcao = self.tela.mostra_opcoes(opcoes_alteracao, "---- Opções de Alteração ----")
                funcao = funcoes_alteracao[opcao]
                if funcao is False:
                    break
                funcao(receita)
            opcao = self.tela.mostra_opcoes(opcoes)
            if opcao == 0:
                break

    def alteracao_completa(self, receita: Receita):
        dados_antigos = self.dados_receita(receita)
        dados = self.tela.alteracao_completa(dados_antigos)
        if receita.codigo != dados["codigo"]:
            if dados["codigo"] in self.__receitas.keys():
                self.tela.mensagem_erro("Código já em uso")
                return 
            else:
                self.__receitas.pop(receita.codigo)
                receita.codigo = dados["codigo"]
                self.__receitas[dados["codigo"]] = receita
        receita.modo_preparo = dados["modo_preparo"]
        receita.tempo_preparo = dados["tempo_preparo"]
        receita.rendimento = dados["rendimento"]
        self.altera_ingredientes(receita)


    def altera_codigo(self, receita: Receita):
        codigo_novo = self.tela.altera_codigo(receita.codigo)
        if receita.codigo != codigo_novo:
            if codigo_novo in self.__receitas.keys():
                self.tela.mensagem_erro("Código já em uso")
                return
        self.__receitas.pop(receita.codigo)
        receita.codigo = codigo_novo
        self.__receitas[codigo_novo] = receita
        self.tela.mensagem("Alteração Realizada com sucesso")

    def altera_modo_preparo(self, receita: Receita):
        modo_preparo_novo = self.tela.altera_modo_preparo(receita.modo_preparo)
        receita.modo_preparo = modo_preparo_novo
        self.tela.mensagem("Alteração Realizada com sucesso")

    def altera_tempo_preparo(self, receita: Receita):
        tempo_preparo_novo = self.tela.altera_tempo_preparo(receita.tempo_preparo)
        receita.tempo_preparo = tempo_preparo_novo
        self.tela.mensagem("Alteração Realizada com sucesso")

    def altera_rendimento(self, receita: Receita):
        rendimento_novo = self.tela.altera_rendimento(receita.rendimento)
        receita.rendimento = rendimento_novo
        self.tela.mensagem("Alteração Realizada com sucesso")

    def altera_ingredientes(self, receita: Receita):
        opcoes = {1: "Adicionar ingrediente", 2: "Remover ingrediente", 3: "Alterar quantidade", 0: "Voltar"}
        switcher = {1: self.inclui_ingrediente_receita, 2: self.remove_ingrediente_receita, 3: self.altera_quantidade_ingrediente, 0: False}
        while True:
            opcao = self.tela.mostra_opcoes(opcoes, "---- Alterar Ingredientes ----")
            funcao = switcher[opcao]
            if funcao is False:
                break
            funcao(receita)

    def altera_quantidade_ingrediente(self, receita: Receita):
        codigo_ingrediente = self.tela.altera_quantidade_pegar_codigo()
        ingrediente = self.__controlador_central.controlador_ingredientes.seleciona_ingrediente_por_codigo(codigo_ingrediente)
        if ingrediente is False:
            self.tela.mensagem_erro("Não existe ingrediente com este código")
            return
        try:
            quantidade = receita.ingredientes_receita[ingrediente]
        except KeyError:
            self.tela.mensagem_erro("A receita não possui o ingrediente")
            return
        quantidade_ingrediente = self.tela.altera_quantidade_pegar_quantidade(quantidade)
        receita.ingredientes_receita[ingrediente] = quantidade_ingrediente
        self.tela.mensagem("Alteração Realizada com sucesso")

    def remove_receita(self):
        opcoes = {1: "Continuar excluindo", 0: "Voltar"}
        opcoes_remocao = {1: "Confirmar exclusão", 0: "Cancelar"}
        while True:
            codigo_receita = self.tela.remove_receita()
            try:
                receita = self.__receitas[codigo_receita]
                if receita.produto_associado:
                    self.tela.mensagem("Esta receita está associada a um produto")
                opcao = self.tela.mostra_opcoes(opcoes_remocao, "Confirmar Exclusão")
                if opcao == 1:
                    self.__receitas.pop(codigo_receita)
                    if receita.produto_associado:
                        receita.produto_associado.remove_receita()
                    self.tela.mensagem("Receita excluida com sucesso")
                else:
                    self.tela.mensagem("Exclusão Cancelada")
            except KeyError:
                self.tela.mensagem_erro("Não existe ingrediente com este código")
            opcao = self.tela.mostra_opcoes(opcoes)
            if opcao == 0:
                break

    def lista_receitas(self):
        self.tela.cabecalho("Lista de Receitas")
        for receita in self.__receitas.values():
            self.mostra_receita(receita)

    def dados_receita(self, receita: Receita):
        dados = {}
        dados_ingredientes = []
        dados["codigo"] = receita.codigo
        if receita.produto_associado is not False:
            dados["produto_associado"] = receita.produto_associado.nome
        else:
            dados["produto_associado"] = False
        dados["modo_preparo"] = receita.modo_preparo
        dados["tempo_preparo"] = receita.tempo_preparo
        dados["rendimento"] = receita.rendimento
        dados["custo_preparo"] = receita.custo_preparo
        for ingrediente, quantidade in receita.ingredientes_receita.items():
            dados_ingrediente = self.__controlador_central.controlador_ingredientes.dados_ingrediente(ingrediente)
            dados_ingrediente["quantidade"] = quantidade
            dados_ingredientes.append(dados_ingrediente)
        dados["dados_ingredientes"] = dados_ingredientes
        return dados

    def mostra_receita(self, receita):
        dados = self.dados_receita(receita)
        self.tela.mostra_receita(dados)

    def pesquisa_por_ingrediente(self):
        opcoes = {1: "Continuar a pesquisar", 0: "Voltar"}
        while True:
            codigo_ingrediente = self.tela.pesquisa_por_ingrediente()
            ingrediente = self.__controlador_central.controlador_ingredientes.seleciona_ingrediente_por_codigo(codigo_ingrediente)
            if ingrediente is False:
                self.tela.mensagem_erro("Não existe ingrediente com este código")
            else:
                for receita in self.__receitas.values():
                    try:
                        receita.ingredientes_receita[ingrediente]
                        self.mostra_receita(receita)
                    except KeyError:
                        continue
            opcao = self.tela.mostra_opcoes(opcoes)
            if opcao == 0:
                break
            
    def seleciona_receita_por_codigo(self, codigo: int):
        try:
            return self.__receitas[codigo]
        except KeyError:
            return False

    def remove_ingrediente_associado_receitas(self, ingrediente_removido: Ingrediente):
        for receita in self.__receitas.values():
            try:
                receita.ingredientes_receita[ingrediente_removido]
                receita.ingredientes_receita.pop(ingrediente_removido)
            except KeyError:
                pass
