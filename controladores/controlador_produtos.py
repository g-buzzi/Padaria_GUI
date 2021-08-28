from telas.tela_produto import TelaProduto
from controladores.controlador_abstrato import Controlador
from entidades.produto import Produto

class ControladorProdutos(Controlador):
    def __init__(self, controlador_central: Controlador):
        super().__init__(TelaProduto(self))
        self.__produtos = {}
        self.__controlador_central = controlador_central

    @property
    def produtos(self):
        return self.__produtos

    def abre_tela_inicial(self):
        switcher = {0: False, 1: self.registra_produto, 2: self.altera_produto, 3: self.remove_produto, 4: self.lista_produtos, 5: self.pesquisa_produto_por_nome}
        opcoes = {1: "Cadastrar", 2: "Alterar", 3: "Remover", 4: "Listar", 5: "Pesquisar", 0: "Voltar"}
        while True:
            opcao = self.tela.mostra_opcoes(opcoes, "--------- Produtos ---------")
            funcao_escolhida = switcher[opcao]
            if funcao_escolhida:
                funcao_escolhida()
            else:
                break

    def registra_produto(self):
        opcoes = {1: "Continuar cadastrando", 0: "Voltar"}
        while True:
            dados = self.tela.registra_produto()
            if dados["codigo"] not in self.__produtos.keys():
                receita = self.__controlador_central.controlador_receitas.seleciona_receita_por_codigo(dados["codigo_receita"])
                for produto in self.__produtos.values():
                    if dados["nome"].lower() == produto.nome.lower():
                        self.tela.mensagem_erro("Nome duplicado")
                        continue
                if receita is False:
                    self.tela.mensagem_erro("Não exite receita com esse código")
                    continue
                if receita.produto_associado is not False:
                    self.tela.mensagem_erro("Receita já associada a um produto")
                    continue
                produto = Produto(dados["codigo"], dados["nome"], dados["preco_venda"], dados["descricao"], receita)
                self.__produtos[dados["codigo"]] = produto
                receita.produto_associado = produto
                self.tela.mensagem("Produto cadastrado com sucesso")
            else:
                self.tela.mensagem_erro("Código já em uso")
            opcao = self.tela.mostra_opcoes(opcoes)
            if opcao == 0:
                break


    def altera_produto(self):
        opcoes_alteracao = {1: "Alteração completa", 2: "Alterar código", 3: "Alterar nome", 4: "Alterar preço de venda", 5: "Alterar descricao", 6: "Alterar receita", 0:"Finalizar alteração"}
        funcoes_alteracao = {1: self.alteracao_completa, 2: self.altera_codigo, 3: self.altera_nome, 4: self.altera_preco_venda, 5: self.altera_descricao, 6: self.altera_receita, 0: False}
        opcoes = {1: "Alterar outro produto", 0: "Voltar"}
        while True:
            codigo = self.tela.altera_produto()
            try:
                produto = self.__produtos[codigo]
            except KeyError:
                self.tela.mensagem_erro("Nenhuma produto com este código existe")
                continue
            while True:
                self.mostra_produto(produto)
                opcao = self.tela.mostra_opcoes(opcoes_alteracao, "---- Opções de Alteração ----")
                funcao = funcoes_alteracao[opcao]
                if funcao is False:
                    break
                funcao(produto)
            opcao = self.tela.mostra_opcoes(opcoes)
            if opcao == 0:
                break

    def alteracao_completa(self, produto: Produto):
        dados_antigos = self.dados_produto(produto)
        dados = self.tela.alteracao_completa(dados_antigos)
        if dados["codigo"] != produto.codigo:
            if dados["codigo"] in self.__produtos.keys():
                self.tela.mensagem_erro("Código já em utilização")
                return
        if dados["nome"].lower() != produto.nome.lower():
            for prod in self.__produtos.values():
                if dados["nome"].lower() == prod.nome.lower() and prod != produto:
                    self.tela.mensagem_erro("Nome já em utilização")
                    return
        receita = self.__controlador_central.controlador_receitas.seleciona_receita_por_codigo(dados["codigo_receita"])
        if receita is False:
            self.tela.mensagem_erro("Não existe receita com este código")
            return
        if receita.produto_associado is not False:
            self.tela.mensagem_erro("A receita já está associada a um produto")
            return
        self.__produtos.pop(produto.codigo)
        produto.codigo = dados["codigo"]
        self.__produtos[produto.codigo] = produto
        produto.nome = dados["nome"]
        produto.preco_venda = dados["preco_venda"]
        produto.descricao = dados["descricao"]
        produto.receita = receita
        receita.produto_associado = produto

    def altera_codigo(self, produto: Produto):
        novo_codigo = self.tela.altera_codigo(produto.codigo)
        if novo_codigo != produto.codigo:
            if novo_codigo in self.__produtos.keys():
                self.tela.mensagem_erro("Código já em uso")
        self.__produtos.pop(produto.codigo)
        produto.codigo = novo_codigo
        self.__produtos[produto.codigo] = produto

    def altera_nome(self, produto: Produto):
        novo_nome = self.tela.altera_nome(produto.nome)
        if novo_nome.lower() != produto.nome.lower():
            for prod in self.__produtos.values():
                if novo_nome.lower() == prod.nome.lower() and prod != produto:
                    self.tela.mensagem_erro("Nome já em utilização")
                    return
        produto.nome = novo_nome

    def altera_preco_venda(self, produto: Produto):
        novo_preco = self.tela.altera_preco_venda(produto.preco_venda)
        produto.preco_venda = novo_preco

    def altera_descricao(self, produto: Produto):
        nova_descricao = self.tela.altera_descricao(produto.descricao)
        produto.descricao = nova_descricao
                
    def altera_receita(self, produto: Produto):
        if produto.receita:
            receita_codigo = produto.receita.codigo
        else:
            receita_codigo = "--"
        novo_codigo_receita = self.tela.altera_receita(receita_codigo)
        receita = self.__controlador_central.controlador_receitas.seleciona_receita_por_codigo(novo_codigo_receita)
        if receita is False:
            self.tela.mensagem_erro("Não existe receita com este código")
            return
        if receita.produto_associado is not False:
            self.tela.mensagem_erro("Receita já associada a um produto")
            return
        produto.receita = receita
            
    def remove_produto(self):
        opcoes = {1: "Continuar excluindo", 0: "Voltar"}
        opcoes_remocao = {1: "Confirmar exclusão", 0: "Cancelar"}
        while True:
            codigo = self.tela.remove_produto()
            try:
                produto = self.__produtos[codigo]
                if produto.receita is not False:
                    self.tela.mensagem("Este produto está associado a uma receita")
                opcao = self.tela.mostra_opcoes(opcoes_remocao, "Confirmar exclusão")
                if opcao == 1:
                    self.__produtos.pop(codigo)
                    if produto.receita is not False:
                        produto.receita.remove_produto_associado()
                    self.tela.mensagem("Produto excluido com sucesso")
                else:
                    self.tela.mensagem("Exclusão Cancelada")
            except KeyError:
                self.tela.mensagem_erro("Não existe produto com este código")
            opcao = self.tela.mostra_opcoes(opcoes)
            if opcao == 0:
                break


    def lista_produtos(self):
        self.tela.cabecalho("Lista de Produtos")
        for produto in self.__produtos.values():
            self.mostra_produto(produto)

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
            dados["custo_unitario"] = 0
        
        return dados


    def mostra_produto(self, produto: Produto):
        dados = self.dados_produto(produto)
        self.tela.mostra_produto(dados)

    def pesquisa_produto_por_nome(self):
        opcoes = {1: "Continuar pesquisa", 0: "Voltar"}
        while True:
            pesquisa = self.tela.pesquisa_produto_por_nome()
            resultados = False
            for produto in self.__produtos.values():
                if pesquisa in produto.nome.lower():
                    resultados = True
                    self.mostra_produto(produto)
            if not resultados:
                self.tela.mensagem("Nenhum produto com esse nome foi encontrado") 
            opcao = self.tela.mostra_opcoes(opcoes)
            if opcao == 0:
                break
            
    def seleciona_produto_por_codigo(self, codigo: int):
        try:
            return self.__produtos[codigo]
        except KeyError:
            return False
