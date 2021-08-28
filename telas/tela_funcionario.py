from telas.tela_abstrata import Tela


class TelaFuncionario(Tela):

    def __init__(self, controlador):
        super().__init__(controlador)

    def recebe_dados_funcionarios(self, mensagem: str = None):
        if mensagem:
            self.adiciona_cabecalho(mensagem)

        return {
            'matricula': self.le_num_inteiro('Matrícula: '),
            'nome': self.le_string('Nome: '),
            'cpf': self.le_string('CPF: '),
            'telefone': self.le_num_inteiro('Telefone: '),
            'email': self.le_string('E-mail: '),
            'salario': self.le_num_fracionario('Salário: ')
        }

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

    def adiciona_cabecalho(self, mensagem: str):
        print('------- ' + mensagem + ' -------')

    def solicita_matricula_funcionario(self, mensagem: str):
        self.adiciona_cabecalho(mensagem)
        return self.le_num_inteiro('Matrícula: ')

