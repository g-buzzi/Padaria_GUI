class NotFoundException(Exception):
    def __init__(self, entidade: str = None, mensagem_personalizada: str = "Nada encontrado."):
        super().__init__(mensagem_personalizada if mensagem_personalizada else "{} não encontrado(a)".format(entidade.capitalize()))