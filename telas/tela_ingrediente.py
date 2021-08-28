from entidades.ingrediente import Ingrediente
from telas.tela_abstrata import Tela

class TelaIngrediente(Tela):
    def __init__(self, controlador):
        super().__init__(controlador)

    def mostra_opcoes(self) -> int:
        while True:
            print("--------- Opções ---------")
            print("1: Cadastrar ingrediente")
            print("2: Alterar ingrediente")
            print("3: Remover ingrediente")
            print("4: Listar Ingredientes")
            print("5: Pesquisar ingredientes")
            print("0: Voltar")
            print()
            opcao = self.le_num_inteiro(valores_validos= range(6))
            print()
            return opcao
        

    def registra_ingrediente(self):
        dados = {}
        print("------- Cadastro de Ingrediente -------")
        dados["codigo"] = self.le_num_inteiro("Digite o código do ingrediente: ")
        dados["nome"] = self.le_string("Digite o nome do ingrediente: ")
        dados["unidade_medida"] = self.le_string("Digite a unidade de medida do ingrediente: ")
        dados["preco_unitario"] = self.le_num_fracionario("Digite o preço de compra do ingrediente: ")
        print()
        return dados

    def altera_ingrediente(self):
        while True:
            print("------- Alterar Ingrediente -------")
            print()
            print("Pesquisar pelo ingrediente?")
            print("1: Sim")
            print("2: Não")
            print("0: Voltar")
            print()
            opcao = self.le_num_inteiro("Opção: ", range(3))
            print()
            if opcao == 0:
                break
            if opcao == 1:
                self.controlador.pesquisa_ingrediente_por_nome()
                print()
            codigo = self.le_num_inteiro("Digite o código do ingrediente: ")
            print()
            dados_antigos = self.controlador.dados_ingrediente(codigo)
            if dados_antigos:
                novos_dados = {}
                print("Código anterior: {}".format(dados_antigos["codigo"]))
                novos_dados["codigo"] = self.le_num_inteiro("Digite o novo código: ")
                print()
                print("Nome anterior: {}".format(dados_antigos["nome"]))
                novos_dados["nome"] = self.le_string("Digite o novo nome: ")
                print()
                print("Unidade de medida anterior: {}".format(dados_antigos["unidade_medida"]))
                novos_dados["unidade_medida"] = self.le_string("Digite a nova unidade de medida: ")
                print()
                print("Preço de compra anterior: {:.2f}".format(dados_antigos["preco_unitario"]))
                novos_dados["preco_unitario"] = self.le_num_fracionario("Digite o novo preço de compra: ")
                return codigo, novos_dados
            else:
                self.mensagem_erro("Nenhum ingrediente com este código existe")



    def remove_ingrediente(self):
        while True:
            print("------- Remover Ingrediente -------")
            print()
            print("Pesquisar pelo ingrediente?")
            print("1: Sim")
            print("2: Não")
            print("0: Voltar")
            print()
            opcao = self.le_num_inteiro("Opção: ", range(3))
            print()
            if opcao == 0:
                break
            if opcao == 1:
                self.controlador.pesquisa_ingrediente_por_nome()
                print()
            codigo = self.le_num_inteiro("Digite o código do ingrediente: ")
            print()
            ingrediente = self.controlador.dados_ingrediente(codigo)
            if ingrediente:
                print("Remover este ingrediente?")
                self.mostra_ingrediente(ingrediente)
                print("0: Sim")
                print("1: Não")
                print()
                opcao = self.le_num_inteiro("Opção: ", range(2))
                print()
                if opcao == 0:
                    print("Ingrediente Removido")
                    print()
                    return codigo
                else:
                    print("Remoção Cancelada")
                    print()
            else:
                self.mensagem_erro("Nenhum ingrediente com este código existe")

            

    def lista_ingredientes(self, dados_ingredientes: list):
        print("------- Listar Ingredientes -------")
        print()
        for dados_ingrediente in dados_ingredientes:
            self.mostra_ingrediente(dados_ingrediente)

    def mostra_ingrediente(self, dados_ingrediente: list):
        print("---- {} ----".format(dados_ingrediente["nome"]))
        print("Código: {}".format(dados_ingrediente["codigo"]))
        print("Unidade Medida: {}".format(dados_ingrediente["unidade_medida"]))
        print("Preço Unitário: {:.2f}".format(dados_ingrediente["preco_unitario"]))
        print()

    def pesquisa_ingrediente_por_nome(self):
        print("------- Pesquisar Ingredientes -------")
        pesquisa = self.le_string("Digite o nome do produto para pesquisa: ")
        print()
        print("---- Resultados para '{}' ----".format(pesquisa))
        print()
        return pesquisa.lower()
