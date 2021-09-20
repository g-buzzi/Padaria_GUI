class NotFoundException(Exception):
    def __init__(self, entidade: str = None, mensagem_personalizada: str = None): #Tem que ser None ou a expressão do if não funciona
        super().__init__(mensagem_personalizada if mensagem_personalizada else "{} não encontrado(a)".format(entidade.capitalize()))