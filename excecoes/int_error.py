from excecoes.input_error import InputError

class IntError(InputError):
    def __init__(self, campo: str, *args: object) -> None:
        super().__init__("{} deve ser um número inteiro maior ou igual a zero".format(campo.capitalize()), *args)