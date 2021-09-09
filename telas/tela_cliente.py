from telas.tela_abstrata import Tela

class TelaCliente(Tela):
    
    def __init__(self, controlador):
        super().__init__()
        
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
        cpf = self.le_string('Cpf: ')
        print()
        return cpf
    
    
    def alteracao_cliente(self, dados_antigos: dict):
        dados = {}
        
        dados["nome"] = self.altera_string(dados_antigos["nome"], 'Nome antigo: ', 'Novo nome: ')
        dados["cpf"] = self.altera_string(dados_antigos["cpf"], 'Cpf antigo: ', 'Novo Cpf: ')
        dados["telefone"] = self.altera_inteiro(dados_antigos["telefone"], 'Telefone antigo: ', 'Novo telefone: ')
        dados["email"] = self.altera_string(dados_antigos["email"], 'E-mail antigo: ', 'Novo e-mail: ')
        dados["endereco"] = self.altera_string(dados_antigos["endereco"], 'Endereço antigo: ', 'Novo endereço: ')
        print()
        return dados

    def altera_inteiro(self, dado_antigo: int, msg_dado_antigo: str, msg_dado_novo: str):
        print(msg_dado_antigo + "{}".format(dado_antigo))
        dado_novo = self.le_num_inteiro(msg_dado_novo)
        print()
        return dado_novo
    
    def altera_string(self, dado_antigo: int, msg_dado_antigo: str, msg_dado_novo: str):
        print(msg_dado_antigo + "{}".format(dado_antigo))
        dado_novo = self.le_string(msg_dado_novo)
        print()
        return dado_novo