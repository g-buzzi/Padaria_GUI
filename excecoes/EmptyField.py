from excecoes.InputError import InputError

class EmptyFieldError(InputError):
    def __init__(self, *args: object) -> None:
        super().__init__("Preencha todos os campos!", *args)
