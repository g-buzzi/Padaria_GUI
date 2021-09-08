class InputError(Exception):
    def __init__(self, mensagem = "Um erro ocorreu", *args: object) -> None:
        self.__mensagem = mensagem
        super().__init__(*args)

    @property
    def mensagem(self):
        return self.__mensagem
    