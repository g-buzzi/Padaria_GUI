from telas.tela_abstrata import Tela


class TelaCentral(Tela):

    def __init__(self, controlador):
        super().__init__(controlador)

    def mostra_opcoes(self) -> int:
        while True:
            print("--------- Opções ---------")
            print("1: Ingredientes")
            print("0: Sair")
            print()
            opcao = self.le_num_inteiro(valores_validos= range(6))
            print()
            return opcao