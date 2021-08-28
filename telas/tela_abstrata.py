from abc import ABC, abstractmethod


class Tela(ABC):
    def __init__(self, controlador):
        self.__controlador = controlador

    @property
    def controlador(self):
        return self.__controlador

    @abstractmethod
    def mostra_opcoes(self) -> int:
        pass

    def le_num_inteiro(self, mensagem: str = "Escolha uma opção: ", valores_validos: list = None) -> int:
        while True:
            try:
                inteiro = int(input(mensagem))
                if valores_validos and inteiro not in valores_validos:
                    raise ValueError
                return inteiro
            except ValueError:
                self.mensagem_erro("Valor incorreto. Digite um número inteiro válido")
                if valores_validos:
                    print("Valores Válidos:", end=" ")
                    for valor in valores_validos[:-1]:
                        print(valor, end=", ")
                    print(valores_validos[-1])
                    print()

    def le_num_fracionario(self, mensagem: str = "Digite um valor"):
        while True:
            try:
                fracionario = float(input(mensagem))
                return fracionario
            except ValueError:
                self.mensagem_erro("Valor incorreto. Digite um número fracionário.")
    
    def le_string(self, mensagem: str = "Digite algo"):
        string = input(mensagem)
        return string

    def mensagem_erro(self, mensagem: str):
        print()
        print("### ERRO ###")
        print(mensagem)
        print()

    def mensagem(self, mensagem: str):
        print("- {} -".format(mensagem))
        print()


