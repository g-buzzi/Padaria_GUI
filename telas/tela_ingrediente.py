from entidades.ingrediente import Ingrediente
from telas.tela_abstrata import Tela

class TelaIngrediente(Tela):
    def __init__(self, controlador):
        super().__init__(controlador)

    def registra_ingrediente(self):
        dados = {}
        print("------- Cadastro de Ingrediente -------")
        dados["codigo"] = self.le_num_inteiro("Código: ")
        dados["nome"] = self.le_string("Nome: ")
        dados["unidade_medida"] = self.le_string("Unidade de medida: ")
        dados["preco_unitario"] = self.le_num_fracionario("Preço por {}: R$".format(dados["unidade_medida"]))
        print()
        return dados

    def altera_ingrediente(self):
        print("------- Alterar Ingrediente -------")
        print()
        codigo = self.le_num_inteiro("Digite o código do ingrediente a ser alterado: ")
        print() 
        return codigo

    def alteracao_completa(self, dados_antigos: dict):
        novos_dados = {}
        print("Código anterior: {}".format(dados_antigos["codigo"]))
        novos_dados["codigo"] = self.le_num_inteiro("Novo código: ")
        print()
        print("Nome anterior: {}".format(dados_antigos["nome"]))
        novos_dados["nome"] = self.le_string("Novo nome: ")
        print()
        print("Unidade de medida anterior: {}".format(dados_antigos["unidade_medida"]))
        novos_dados["unidade_medida"] = self.le_string("Nova unidade de medida: ")
        print()
        print("Preço por {} anterior: R${:.2f}".format(dados_antigos["unidade_medida"], dados_antigos["preco_unitario"]))
        novos_dados["preco_unitario"] = self.le_num_fracionario("Novo preço por {}: R$".format(novos_dados["unidade_medida"]))
        print()
        return novos_dados

    def altera_codigo(self, codigo: int):
        print("Código anterior: {}".format(codigo))
        codigo = self.le_num_inteiro("Novo código: ")
        print()
        return codigo

    def altera_nome(self, nome: str):
        print("Nome anterior: {}".format(nome))
        nome = self.le_string("Novo nome: ")
        print()
        return nome

    def altera_unidade(self, unidade: str):
        print("Unidade de medida anterior: {}".format(unidade))
        unidade = self.le_string("Nova unidade de medida: ")
        print()
        return unidade

    def altera_preco(self, unidade: str, preco: float):
        print("Preço por {} anterior: R${:.2f}".format(unidade, preco))
        preco = self.le_num_fracionario("Novo preço por {}: R$".format(unidade))
        print()
        return preco

    def remove_ingrediente(self):
        print("------- Remover Ingrediente -------")
        print()
        codigo = self.le_num_inteiro("Digite o código do ingrediente: ")
        print()
        return codigo   

    def lista_ingredientes(self, dados_ingredientes: list):
        print("------- Listar Ingredientes -------")
        print()
        for dados_ingrediente in dados_ingredientes:
            self.mostra_ingrediente(dados_ingrediente)

    def mostra_ingrediente(self, dados_ingrediente: list):
        print("---- {} ----".format(dados_ingrediente["nome"]))
        print("Código: {}".format(dados_ingrediente["codigo"]))
        print("Unidade de Medida: {}".format(dados_ingrediente["unidade_medida"]))
        print("Preço em {}: R${:.2f}".format(dados_ingrediente["unidade_medida"], dados_ingrediente["preco_unitario"]))
        print()

    def pesquisa_ingrediente_por_nome(self):
        print("------- Pesquisar Ingredientes -------")
        pesquisa = self.le_string("Digite o nome do produto para pesquisa: ")
        print()
        print("---- Resultados para '{}' ----".format(pesquisa))
        print()
        return pesquisa.lower()
