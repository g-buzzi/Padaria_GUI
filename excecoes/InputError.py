class InputError(Exception):
    def __init__(self, mensagem= "Ocorreu um erro!", *args: object) -> None:
        self.mensagem = mensagem
        super().__init__(*args)