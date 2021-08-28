from abc import ABC, abstractmethod


class Tela(ABC):
    @abstractmethod
    def __init__(self, controlador):
        self.__controlador = controlador

    @property
    def controlador(self):
        return self.__controlador

    def mostra_opcoes(self, opcoes: dict, titulo = "--------- Opções ---------") -> int:
        print(titulo)
        for numero, opcao in opcoes.items():
            print("{}: {}".format(numero, opcao))
        print()
        opcao = self.le_num_inteiro("Opção: ", opcoes.keys())
        print()
        return opcao

    def le_num_inteiro(self, mensagem: str = "Escolha uma opção: ", valores_validos: list = None) -> int:
        while True:
            try:
                inteiro = input(mensagem)
                inteiro = int(inteiro) 
                if valores_validos and inteiro not in valores_validos:
                    raise ValueError
                if inteiro < 0:
                    self.mensagem_erro("Valor incorreto. Digite um valor maior que 0")
                else:
                    return inteiro
            except ValueError:
                self.mensagem_erro("Valor incorreto. Digite um número inteiro válido")

    def le_num_fracionario(self, mensagem: str = "Digite um valor", digitos: int = 2):
        while True:
            try:
                fracionario = round(float(input(mensagem)), digitos)
                if fracionario >= 0:
                    return fracionario
                self.mensagem_erro("Valor incorreto. Digite um número maior que 0.")
            except ValueError:
                self.mensagem_erro("Valor incorreto. Digite um número fracionário válido.")
    
    def le_string(self, mensagem: str = "Digite algo"):
        string = input(mensagem)
        return string.strip()

    def cabecalho(self, mensagem: str):
        print("-------- " + mensagem + " --------")
        print()

    def mensagem_erro(self, mensagem: str):
        print()
        print("### ERRO ###")
        print(mensagem)
        print()

    def mensagem(self, mensagem: str):
        print("- {} -".format(mensagem))
        print()

    def quebra_linha(self):
        print()


