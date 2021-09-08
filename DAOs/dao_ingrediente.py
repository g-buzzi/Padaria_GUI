from DAOs.dao_abstrato import DAO
from entidades.ingrediente import Ingrediente

class IngredienteDAO(DAO):
    
    def __init__(self, datasource) -> None:
        super().__init__(datasource="ingredientes.pkl")

    def add(self, ingrediente: Ingrediente):
        if (ingrediente is not None and isinstance(ingrediente, Ingrediente)):
            super().add(ingrediente.codigo, ingrediente)

    def remove(self, codigo: int):
        if isinstance(codigo, int):
            try:
                super().remove(codigo)
            except KeyError:
                pass

    def get(self, codigo: int):
        if isinstance(codigo, int):
            try:
                super().get(codigo)
            except KeyError:
                pass

        