from telas.tela_abstrata import Tela

class TelaEstoque(Tela):
    def __init__(self, controlador):
        super().__init__(controlador)


    def le_quantidade(self) -> int:
        quantidade = self.le_num_inteiro("Quantidade: ")
        print()
        return quantidade

    def le_codigo(self, tipo: str):
        codigo = self.le_num_inteiro("Código do " + tipo +": ")
        print()
        return codigo

    def mostra_movimentacao(self, dados: dict):
        print("--------- {} ---------".format(dados["tipo"]))
        print("Data: {}".format(dados["data"]))
        print("Produto: {}".format(dados["nome_produto"]))
        print("Quantidade: {}".format(dados["quantidade"]))
        print("Valor: {:.2f}".format(dados["valor_total"]))
        print()

    def mostra_estoque(self, dados: dict, tipo: str):
        print(dados["nome"].ljust(40), "{}".format(dados["quantidade"]).ljust(8))

    def cabecalho_estoque(self, tipo: str):
        print(tipo.ljust(40), "Quantidade".ljust(8))

    def balanco(self, balanco: float):
        print("Balanço: ".ljust(40), "R${:.2f}".format(balanco).ljust(8))
        print()