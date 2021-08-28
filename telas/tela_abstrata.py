from abc import ABC, abstractmethod
from controladores.controlador_abstrato import Controlador

class Tela(ABC):
    def __init__(self, controlador: Controlador):
        self.__controlador = controlador

    @abstractmethod
    def mostra_opcoes() -> int:
        pass

    def le_num_inteiro(self, mensagem: str = "Escolha uma opção:", valores_validos: list = None) -> int:
        while True:
            try:
                inteiro = int(input(mensagem))
                if valores_validos and inteiro not in valores_validos:
                    raise ValueError
                return inteiro
            except ValueError:
                print("Valor incorreto. Digite um número inteiro válido")
                if valores_validos:
                    print("Valores Válidos:", end=" ")
                    for valor in valores_validos[:-1]:
                        print(valor, end=", ")
                    print(valores_validos[-1])

    def mensagem_erro(mensagem: str):
        print(mensagem)


