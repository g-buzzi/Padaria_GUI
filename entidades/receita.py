from entidades.ingrediente import Ingrediente


class Receita:
    def __init__(self, codigo: int, modo_preparo: str, tempo_preparo: float, rendimento: int):
        self.__codigo = codigo
        self.__modo_preparo = modo_preparo
        self.__tempo_preparo = tempo_preparo
        self.__rendimento = rendimento
        self.__ingredientes_receita = {}
        self.__produto_associado = False

    @property
    def codigo(self) -> int:
        return self.__codigo

    @codigo.setter
    def codigo(self, codigo: int):
        self.__codigo = codigo

    @property
    def modo_preparo(self) -> str:
        return self.__modo_preparo

    @modo_preparo.setter
    def modo_preparo(self, modo_preparo: str):
        self.__modo_preparo = modo_preparo
    
    @property
    def tempo_preparo(self) -> float:
        return self.__tempo_preparo

    @tempo_preparo.setter
    def tempo_preparo(self, tempo_preparo: float):
        self.__tempo_preparo = tempo_preparo

    @property
    def rendimento(self) -> int:
        return self.__rendimento

    @rendimento.setter
    def rendimento(self, rendimento: int):
        self.__rendimento = rendimento
    
    @property
    def ingredientes_receita(self) -> dict:
        return self.__ingredientes_receita

    @property
    def produto_associado(self):
        return self.__produto_associado

    @produto_associado.setter
    def produto_associado(self, produto_associado):
        self.__produto_associado = produto_associado

    def remove_produto_associado(self):
        self.__produto_associado = False

    def inclui_ingrediente(self, ingrediente: Ingrediente, quantidade: float):
        self.__ingredientes_receita[ingrediente] = quantidade

    def remove_ingrediente(self, ingrediente: Ingrediente):
        self.__ingredientes_receita.pop(ingrediente)

    @property
    def custo_preparo(self) -> float:
        custo = 0
        for ingrediente, quantidade in self.__ingredientes_receita.items():
            custo += ingrediente.preco_unitario * quantidade
        return custo
