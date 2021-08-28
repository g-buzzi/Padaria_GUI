from telas.tela_abstrata import Tela

class TelaCliente(Tela):
    
    def __init__(self, controlador):
        super().__init__(controlador)
        
    def recebe_dados_cliente(self, mensagem: str = None):
        if mensagem:
            self.cabecalho(mensagem)

        return {
            'nome': self.le_string('Nome: '),
            'cpf': self.le_string('CPF: '),
            'telefone': self.le_num_inteiro('Telefone: '),
            'email': self.le_string('E-mail: '),
            'endereco': self.le_string('Endereço: ')
        }
        
    def mostra_cliente(self, dados_cliente):
    
        print(
            'Nome:', dados_cliente['nome'],
            '\nCPF:', dados_cliente['cpf'],
            '\nTelefone:', dados_cliente['telefone'],
            '\nE-mail:', dados_cliente['email'],
            '\nEndereço:', dados_cliente['endereco'],
            '\n'
            '\n---------------------------------------'
            '\n'
        )
        
    def solicita_cpf_cliente(self, mensagem: str):
        self.cabecalho(mensagem)
        return self.le_string('Cpf: ')