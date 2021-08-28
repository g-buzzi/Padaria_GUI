from telas.tela_abstrata import Tela

class TelaProduto(Tela):
    def __init__(self, controlador):
        super().__init__(controlador)

    def cadastra_produto(self):
        self.cabecalho("Cadastrar Produto")
        dados = {}
        dados["codigo"] = self.le_num_inteiro("Código do produto: ")
        dados["nome"] = self.le_string("Nome: ")
        dados["preco_venda"] = self.le_num_fracionario("Preço de Venda: R$")
        dados["descricao"] = self.le_string("Descrição: ")
        dados["codigo_receita"] = self.le_num_inteiro("Código da receita: ")
        print()
        return dados


    def altera_produto(self) -> int:
        self.cabecalho("Alterar")
        codigo = self.le_num_inteiro("Código do produto a ser alterado: ")
        print()
        return codigo

    def alteracao_completa(self, dados_antigos: dict) -> dict:
        dados = {}
        dados["codigo"] = self.altera_codigo(dados_antigos["codigo"])
        dados["nome"] = self.altera_nome(dados_antigos["nome"])
        dados["preco_venda"] = self.altera_preco_venda(dados_antigos["preco_venda"])
        dados["descricao"] = self.altera_descricao(dados_antigos["descricao"])
        dados["codigo_receita"] = self.altera_receita(dados_antigos["codigo_receita"])
        print()
        return dados

    def altera_codigo(self, codigo_antigo: int):
        print("Código antigo: {}".format(codigo_antigo))
        novo_codigo = self.le_num_inteiro("Novo código do produto: ")
        print()
        return novo_codigo
        

    def altera_nome(self, nome_antigo: str):
        print("Nome antigo: {}".format(nome_antigo))
        novo_nome = self.le_string("Novo nome: ")
        print()
        return novo_nome

    def altera_preco_venda(self, preco_antigo: float):
        print("Preço de venda antigo: R${:.2f}".format(preco_antigo))
        novo_preco = self.le_num_fracionario("Novo preço de Venda: R$")
        print()
        return novo_preco

    def altera_descricao(self, descricao_antiga: str):
        print("Descrição antiga: {}".format(descricao_antiga))
        nova_descricao = self.le_string("Nova descrição: ")
        print()
        return nova_descricao
                
    def altera_receita(self, codigo_receita_antiga: int):
        print("Código da receita antiga: {}".format(codigo_receita_antiga))
        novo_codigo_receita = self.le_num_inteiro("Novo código da receita: ")
        print()
        return novo_codigo_receita
            
    def remove_produto(self):
        self.cabecalho("Excluir")
        codigo = self.le_num_inteiro("Código do produto a ser excluido: ")
        print()
        return codigo

    def mostra_produto(self, dados: dict):
        print("---- {} ----".format(dados["nome"]))
        print("Código: {}".format(dados["codigo"]))
        print("Descrição: {}".format(dados["descricao"]))
        print("Preço de Venda: R${:.2f}".format(dados["preco_venda"]))
        print("Custo de preparo: R${:.2f}".format(dados["custo_unitario"]))
        print()

    def pesquisa_produto_por_nome(self):
        self.cabecalho("Pesquisar Produtos")
        pesquisa = self.le_string("Digite o nome do produto para pesquisa: ")
        print()
        print("---- Resultados para '{}' ----".format(pesquisa))
        print()
        return pesquisa.lower()
