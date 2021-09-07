class NotFoundException(Exception):
    def __init__(self, entidade: str, mensagem_personalizada: str = None):
        super().__init__(mensagem_personalizada if mensagem_personalizada else "{} não encontrado(a)".format(entidade.capitalize()))