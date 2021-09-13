class DuplicatedException(Exception):
    def __init__(self, entidade: str = None, mensagem_personalizada: str = None):
        super().__init__(mensagem_personalizada if mensagem_personalizada else "{} já cadastrado(a)".format(entidade.capitalize()))