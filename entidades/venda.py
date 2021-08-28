from entidades.funcionario import Funcionario
from entidades.cliente import Cliente
from entidades.item import Item

class Venda():
   
    def __init__(
        self, 
        codigo: int, 
        atendente: Funcionario,
        encomenda: bool):
        
        self.__codigo = codigo 
        self.__atendente = atendente
        self.__encomenda = encomenda
        self.__itens: list[Item] = []
        self.__preco_final = None,
        self.__desconto: float = None
        self.__cliente: Cliente = None
        self.__data_entrega = None
        self.__entregue: bool = None
        
    
    @property
    def codigo(self) -> int:
        return self.__codigo
    
    @codigo.setter
    def codigo(self, codigo):
        self.__codigo = codigo
        
    @property
    def itens(self) -> list:
        return self.__itens
    
    @itens.setter 
    def itens(self, item):
        self.itens.append(item)
        
    @property
    def preco_final(self) -> float:
        self.calcula_preco_final()
        
        return self.__preco_final
    
    def calcula_preco_final(self):
        total = 0.0
        for item in self.__itens:
            total = total + (item.quantidade * item.produto.preco_venda)
            
        if self.__desconto > 0:
            total = total - (total * self.__desconto/100)
            
        self.__preco_final = total
            
        
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
    def data_entrega(self):
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
    
    
    