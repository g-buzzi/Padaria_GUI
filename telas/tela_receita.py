from telas.tela_abstrata import Tela

class TelaReceita(Tela):
    def __init__(self, controlador):
        super().__init__(controlador)

    def registra_receita(self) -> dict:
        dados = {}
        self.cabecalho("Cadastro de Receita")
        dados["codigo"] = self.le_num_inteiro("Código: ")
        dados["modo_preparo"] = self.le_string("Modo de preparo: ")
        dados["tempo_preparo"] = self.le_num_inteiro("Tempo de preparo: ")
        dados["rendimento"] = self.le_num_inteiro("Rendimento: ")
        print()
        return dados

    def le_codigo_ingrediente(self):
        print("--- Adicionar Ingrediente ---")
        codigo = self.le_num_inteiro("Código do Ingrediente: ")
        print()
        return codigo

    def le_quantidade_ingrediente(self):
        quantidade = self.le_num_fracionario("Quantidade: ")
        print()
        return quantidade

    def remove_ingrediente_receita(self):
        print("--- Remover ingrediente ---")
        codigo = self.le_num_inteiro("Código do Ingrediente: ")
        print()
        return codigo

    def altera_receita(self):
        self.cabecalho("Alterar receita")
        codigo = self.le_num_inteiro("Código da receita a ser alterada: ")
        print()
        return codigo

    def alteracao_completa(self, dados_antigos: dict):
        dados = {}
        dados["codigo"] = self.altera_codigo(dados_antigos["codigo"])
        dados["modo_preparo"] = self.altera_modo_preparo(dados_antigos["modo_preparo"])
        dados["tempo_preparo"] = self.altera_tempo_preparo(dados_antigos["tempo_preparo"])
        dados["rendimento"] = self.altera_rendimento(dados_antigos["rendimento"])
        print()
        return dados

    def altera_codigo(self, codigo_antigo: int):
        print("Código anterior: {}".format(codigo_antigo))
        novo_codigo = self.le_num_inteiro("Novo código: ")
        print()
        return novo_codigo

    def altera_modo_preparo(self, modo_preparo_antigo: str):
        print("Modo de preparo antigo: {}".format(modo_preparo_antigo))
        novo_modo_preparo = self.le_string("Novo modo de preparo: ")
        print()
        return novo_modo_preparo

    def altera_tempo_preparo(self, tempo_preparo_antigo: float):
        print("Tempo de preparo antigo: {:.2f} min".format(tempo_preparo_antigo))
        novo_tempo_preparo = self.le_num_fracionario("Novo tempo de preparo: ")
        print()
        return novo_tempo_preparo

    def altera_rendimento(self, rendimento_antigo: int):
        print("Rendimento antigo: {}".format(rendimento_antigo))
        novo_rendimento = self.le_num_inteiro("Novo rendimento: ")
        print()
        return novo_rendimento

    def altera_quantidade_pegar_codigo(self):
        print("-- Alterar Quantidade --")
        codigo = self.le_num_inteiro("Código do ingrediente: ")
        print()
        return codigo

    def altera_quantidade_pegar_quantidade(self, quantidade_antiga: int):
        print("Quantidade anterior: {}".format(quantidade_antiga))
        nova_quantidade = self.le_num_inteiro("Nova quantidade: ")
        print()
        return nova_quantidade

    def remove_receita(self):
        self.cabecalho("Remover receita")
        codigo = self.le_num_inteiro("Código da receita a ser removida: ")
        print()
        return codigo

    def pesquisar_por_ingrediente(self):
        self.cabecalho("Pesquisar por ingrediente")
        codigo_ingrediente = self.le_num_inteiro("Codigo do ingrediente: ")
        print()
        return codigo_ingrediente

    def mostra_receita(self, dados: dict):
        if dados["produto_associado"] is not False:
            print("--------- Receita de {} ---------".format(dados["produto_associado"]))
        else:
            print("------------------------")
        print("Código: {}".format(dados["codigo"]))
        print("Modo de preparo: {}".format(dados["modo_preparo"]))
        print("Tempo de preparo: {} min".format(dados["tempo_preparo"]))
        print("Rendimento: {} unidades".format(dados["rendimento"]))
        print("Custo de preparo: R${:.2f}".format(dados["custo_preparo"]))
        print()
        print("-- Ingredientes --")
        print()
        for dados_ingrediente in dados["dados_ingredientes"]:
            print("Ingrediente: {}".format(dados_ingrediente["nome"]))
            print("Quantidade: {:.2f}{}".format(dados_ingrediente["quantidade"], dados_ingrediente["unidade_medida"]))
            print()
