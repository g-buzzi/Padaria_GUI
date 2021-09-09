from telas.tela_abstrata import Tela


class TelaFuncionario(Tela):

    def __init__(self, controlador):
        super().__init__()

    def recebe_dados_funcionarios(self, mensagem: str = None):
        if mensagem:
            self.cabecalho(mensagem)

        return {
            'matricula': self.le_num_inteiro('Matrícula: '),
            'nome': self.le_string('Nome: '),
            'cpf': self.le_string('CPF: '),
            'telefone': self.le_num_inteiro('Telefone: '),
            'email': self.le_string('E-mail: '),
            'salario': self.le_num_fracionario('Salário: ')
        }
        
    def alteracao_funcionario(self, dados_antigos: dict):
        dados = {}
        dados["matricula"] = self.altera_inteiro(dados_antigos["matricula"], 'Matrícula antiga: ', 'Nova matrícula: ')
        dados["nome"] = self.altera_string(dados_antigos["nome"], 'Nome antigo: ', 'Novo nome: ')
        dados["cpf"] = self.altera_string(dados_antigos["cpf"], 'Cpf antigo: ', 'Novo Cpf: ')
        dados["telefone"] = self.altera_inteiro(dados_antigos["telefone"], 'Telefone antigo: ', 'Novo telefone: ')
        dados["email"] = self.altera_string(dados_antigos["email"], 'E-mail antigo: ', 'Novo e-mail: ')
        dados["salario"] = self.altera_fracionario(dados_antigos["salario"], 'Salário antigo: ', 'Novo salário: ')
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
    
    def altera_fracionario(self, dado_antigo: float, msg_dado_antigo: str, msg_dado_novo: str):
        print(msg_dado_antigo + "{}".format(dado_antigo))
        dado_novo = self.le_num_fracionario(msg_dado_novo)
        print()
        return dado_novo

    def mostra_funcionario(self, dados_funcionario):

        print(
            'Matrícula:', dados_funcionario['matricula'],
            '\nNome:', dados_funcionario['nome'],
            '\nCPF:', dados_funcionario['cpf'],
            '\nTelefone:', dados_funcionario['telefone'],
            '\nE-mail:', dados_funcionario['email'],
            '\nSalário:', dados_funcionario['salario'],
            '\n'
            '\n---------------------------------------'
            '\n'
        )

    def solicita_matricula_funcionario(self, mensagem: str):
        self.cabecalho(mensagem)
        matricula = self.le_num_inteiro('Matrícula: ')
        print()
        return matricula

