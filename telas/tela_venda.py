from telas.tela_abstrata import Tela

class TelaVenda(Tela):
    def __init__(self, controlador):
        super().__init__(controlador)
        
    def recebe_dados_venda(self, mensagem: str = None):
        if mensagem:
            self.cabecalho(mensagem)

        return {
            'atendente': self.le_num_inteiro('Matrícula do atendente: '),
            'encomenda': self.le_string('Encomenda (s/n): ')
        }
      
    def mostra_dados_encomenda(self, dados_encomenda):
        print(
            'Data de entrega:', dados_encomenda['data_entrega'],
            '\nEntregue:', dados_encomenda['entregue']
        )
        print()
        
    def mostra_cliente(self, cliente: str):
        print(
            'Cliente:', cliente,
            '\n'
        )
          
    def mostra_venda(self, dados_venda):
        
        print(
            
            'Código:', dados_venda['codigo'],
            '\nAtendente:', dados_venda['atendente'],
            '\nEncomenda:', dados_venda['encomenda'],
        )
        print()
        
    def mostra_item(self, dados_item):
        print('Produto:', dados_item['produto'], '\nQuantidade:', dados_item['quantidade'], '\nValor unitário R$:', dados_item['valor_unitario'])
        print()
        print("---------------------")
        print()
            
    def mostra_valores(self, dados_valores):
        print(
            'Desconto na venda (%):', dados_valores['desconto'],
            '\nPreço final R$:', dados_valores['preco_final'],
            '\n'
        )
        
    def solicita_codigo_venda(self, mensagem: str):
        self.cabecalho(mensagem)
        return self.le_num_inteiro('Código da venda: ')
    
    def solicita_item(self):
        self.cabecalho('Dados do item: ')
        
        return {
            'produto': self.le_num_inteiro('Código do produto: '),
            'quantidade': self.le_num_inteiro('Quantidade: ')
        }
        
    def solicita_dados_encomenda(self):
        self.cabecalho('Dados da encomenda: ')
        
        return {
            'data_entrega': self.le_string('Data de entrega: '),
            'cliente': self.le_string('Cpf do cliente: ')
        }
        
    def solicita_desconto(self):
        print('------------------------------')
        desconto = self.le_num_fracionario('\nDesconto na venda (%): ')
        print('\n------------------------------')
        print()
        return desconto
    
    def solicita_cpf_cliente(self):
        return self.le_string('Cpf do cliente: ')
    
    def solicita_matricula_funcionario(self):        
        return self.le_num_inteiro('Matrícula do atendente: ')