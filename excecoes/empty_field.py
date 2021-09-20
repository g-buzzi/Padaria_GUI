from excecoes.input_error import InputError

class EmptyFieldError(InputError):
    def __init__(self, mensagem = "Preencha todos os campos", *args: object) -> None:
        super().__init__(mensagem, *args)
