import textwrap

class InputError(Exception):
    def __init__(self, mensagem = "Um erro ocorreu", *args: object) -> None:
        mensagem = textwrap.fill(mensagem, width= 50)
        super().__init__(mensagem, *args)
    