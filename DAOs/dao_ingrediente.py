from DAOs.dao_abstrato import DAO
from entidades.ingrediente import Ingrediente
from excecoes.not_found_exception import NotFoundException
from DAOs.receita_dao import ReceitaDAO

class IngredienteDAO(DAO):
    instancia = None

    def __new__(cls):
        if IngredienteDAO.instancia is None:
            IngredienteDAO.instancia = super().__new__(cls)
        return IngredienteDAO.instancia
    
    def __init__(self) -> None:
        super().__init__(datasource="ingredientes.pkl")

    def add(self, ingrediente: Ingrediente):
        if (ingrediente is not None and isinstance(ingrediente, Ingrediente)):
            super().add(ingrediente.codigo, ingrediente)

    def remove(self, ingrediente: Ingrediente):
        if isinstance(ingrediente.codigo, int):
            try:
                super().remove(ingrediente.codigo)
                ReceitaDAO().remove_ingrediente(ingrediente.codigo)
            except KeyError:
                raise NotFoundException("Ingrediente")

    def get(self, codigo: int):
        if isinstance(codigo, int):
            try:
                return super().get(codigo)
            except KeyError:
                raise NotFoundException("Ingrediente")

    def alter(self, ingrediente: Ingrediente, codigo_antigo: int):
        if isinstance(ingrediente, Ingrediente) and isinstance(codigo_antigo, int):
            ReceitaDAO().update_ingredientes(ingrediente, codigo_antigo)
            super().alter(codigo_antigo, ingrediente.codigo, ingrediente)

                


        