from entidades.produto import Produto
from entidades.funcionario import Funcionario
from entidades.cliente import Cliente
from entidades.item import Item

class Venda():
   
    def __init__(
        self, 
        codigo: int, 
        atendente: Funcionario,
        encomenda: bool, desconto: float, data_entrega: str, cliente: Cliente):
        
        self.__codigo = codigo 
        self.__atendente = atendente
        self.__encomenda = encomenda
        self.__desconto = desconto
        self.__data_entrega = data_entrega
        self.__cliente = cliente
        self.__itens: list[Item] = []
        self.__entregue: bool = False
        
    
    @property
    def codigo(self) -> int:
        return self.__codigo
    
    @codigo.setter
    def codigo(self, codigo):
        self.__codigo = codigo
        
    @property
    def itens(self) -> list:
        return self.__itens
        
    @property
    def preco_final(self) -> float:
        total = 0.0
        for item in self.__itens:
            total = total + (item.quantidade * item.produto.preco_venda)
            
        if self.__desconto > 0:
            total = total - (total * self.__desconto/100)
        return total    
        
    @property
    def atendente(self) -> Funcionario:
        return self.__atendente
    
    @atendente.setter 
    def atendente(self, atendente):
        self.__atendente = atendente
        
    @property
    def encomenda(self) -> str:
        return 'Sim' if self.__encomenda else 'Não'
    
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

    def inclui_item(self, produto: Produto, quantidade: int):
        self.__itens.append(Item(produto, quantidade))
    
    
    