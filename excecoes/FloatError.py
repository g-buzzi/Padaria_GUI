from excecoes.InputError import InputError

class FloatError(InputError):
    def __init__(self, campo: str, *args: object) -> None:
        super().__init__("{} deve ser um número real maior ou igual a 0".format(campo.capitalize()), *args)