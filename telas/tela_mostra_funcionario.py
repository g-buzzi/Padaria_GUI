from telas.tela_abstrata import Tela
from collections import defaultdict

class TelaMostraFuncionario(Tela):
    instancia = None

    def __new__(cls):
        if TelaMostraFuncionario.instancia is None:
            TelaMostraFuncionario.instancia = super().__new__(cls)
        return TelaMostraFuncionario.instancia

    def __init__(self):
        super().__init__()

    def campos(self, dados_funcionario = defaultdict(lambda: None), leitura = False):

        lb_matricula = self.label("Matrícula: ", tamanho=(17,1))
        in_matricula = self.entrada("matricula", dados_funcionario["codigo"], leitura= leitura, tamanho= (33, 1))

        lb_nome = self.label("Nome: ", tamanho=(17,1))
        in_nome = self.entrada("nome", dados_funcionario["nome"], leitura= leitura, tamanho= (33, 1))

        lb_cpf = self.label("CPF: ", tamanho=(17,1))
        in_cpf = self.entrada("cpf", dados_funcionario["cpf"], leitura= leitura, tamanho= (33, 1))

        lb_telefone = self.label("Telefone: ", tamanho=(17,1))
        in_telefone = self.entrada("telefone", dados_funcionario["telefone"], leitura= leitura, tamanho= (33, 1))

        lb_email = self.label("E-mail: ", tamanho=(17,1))
        in_email = self.entrada("email", dados_funcionario["email"], leitura= leitura, tamanho= (33, 1))

        lb_salario = self.label("Salário: ", tamanho=(17,1))
        in_salario = self.entrada("salario", dados_funcionario["salario"], leitura = leitura, tamanho= (33, 1))

        campos = [
                    [lb_matricula, in_matricula],
                    [lb_nome, in_nome],
                    [lb_cpf, in_cpf],
                    [lb_telefone, in_telefone],
                    [lb_email, in_email],
                    [lb_salario, in_salario]
                ]

        return campos

    
    def cadastra(self, dados_funcionario = defaultdict(lambda: None)):
        titulo = self.titulo("Cadastrar Funcionário")
        campos = self.campos(dados_funcionario)
        altera = self.botao("Cadastrar", "cadastra")
        voltar = self.botao("Voltar", "volta")
        layout = [[titulo]]
        for linha in campos:
            layout.append(linha)
        layout.append([altera, voltar])
        self.window = self.janela(layout)
        return self.read()