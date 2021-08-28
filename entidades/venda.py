from entidades.funcionario import Funcionario
from entidades.cliente import Cliente
from entidades.item import Item

class Venda():
   
    def __init__(
        self, 
        codigo: int, 
        itens: Item,
        preco_final: float, 
        atendente: Funcionario,
        encomenda: bool):
        
        self.__codigo = codigo 
        self.__itens = [itens]
        self.__preco_final = preco_final,
        self.__atendente = atendente
        self.__encomenda = encomenda
        self.__desconto: float = None
        self.__cliente: Cliente = None
        self.__data_entrega: Date = None
        self.__entregue: bool = None
        
    
    @property
    def codigo(self) -> int:
        return self.__codigo
    
    @codigo.setter
    def codigo(self, codigo):
        self.__codigo = codigo
        
    @property
    def itens(self) -> List[Item]:
        return self.__itens
    
    @itens.setter 
    def itens(self, item):
        self.itens.append(item)
        
    @property
    def preco_final(self) -> float:
        return self.__preco_final
    
    @preco_final.setter 
    def preco_final(self, preco_final):
        self.__preco_final = preco_final
        
    @property
    def atendente(self) -> Funcionario:
        return self.__atendente
    
    @atendente.setter 
    def atendente(self, atendente):
        self.__atendente = atendente
        
    @property
    def encomenda(self) -> bool:
        return self.__encomenda
    
    @encomenda.setter 
    def encomenda(self, encomenda):
        self.__encomenda = encomenda
        
    @property
    def desconto(self) -> float:
        return self.__desconto
    
    @desconto.setter 
    def desconto(self, desconto):
        self.__desconto = desconto
        
    @property
    def cliente(self) -> Cliente:
        return self.__cliente
    
    @cliente.setter 
    def cliente(self, cliente):
        self.__cliente = cliente
        
    @property
    def data_entrega(self) -> Date:
        return self.__data_entrega
    
    @data_entrega.setter 
    def data_entrega(self, data_entrega):
        self.__data_entrega = data_entrega
        
    @property
    def entregue(self) -> bool:
        return self.__entregue
    
    @entregue.setter 
    def entregue(self, entregue):
        self.__entregue = entregue
    
    
    