from DAOs.dao_abstrato import DAO
from entidades.ingrediente import Ingrediente
from DAOs.receita_dao import ReceitaDAO
from excecoes.not_found_exception import NotFoundException

class IngredienteDAO(DAO):
    __instancia = None

    def __new__(cls):
        if cls.__instancia is None:
            cls.__instancia = object.__new__(cls)
        return cls.__instancia
    
    def __init__(self) -> None:
        super().__init__(datasource="ingredientes.pkl")

    def add(self, ingrediente: Ingrediente):
        if (ingrediente is not None and isinstance(ingrediente, Ingrediente)):
            super().add(ingrediente.codigo, ingrediente)

    def remove(self, ingrediente: Ingrediente):
        if isinstance(ingrediente.codigo, int):
            super().remove(ingrediente.codigo, "Ingrediente")
            ReceitaDAO().remove_ingrediente(ingrediente.codigo)

    def get(self, codigo: int):
        if isinstance(codigo, int):
            return super().get(codigo, "Ingrediente")

    def alter(self, ingrediente: Ingrediente, codigo_antigo: int):
        if isinstance(ingrediente, Ingrediente) and isinstance(codigo_antigo, int):
            ReceitaDAO().update_ingredientes(ingrediente, codigo_antigo)
            super().alter(codigo_antigo, ingrediente.codigo, ingrediente)

                


        