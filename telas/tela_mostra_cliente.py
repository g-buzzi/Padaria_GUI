from telas.tela_abstrata import Tela
from collections import defaultdict

class TelaMostraCliente(Tela):
    __instancia = None

    def __new__(cls):
        if TelaMostraCliente.__instancia is None:
            TelaMostraCliente.__instancia = object.__new__(cls)
        return TelaMostraCliente.__instancia

    def __init__(self):
        super().__init__()

    def campos(self, dados_cliente = defaultdict(lambda: None), leitura = False):

        lb_cpf = self.label("CPF: ", tamanho=(17,1))
        in_cpf = self.entrada("cpf", dados_cliente["cpf"], leitura= leitura, tamanho= (33, 1))

        lb_nome = self.label("Nome: ", tamanho=(17,1))
        in_nome = self.entrada("nome", dados_cliente["nome"], leitura= leitura, tamanho= (33, 1))

        lb_telefone = self.label("Telefone: ", tamanho=(17,1))
        in_telefone = self.entrada("telefone", dados_cliente["telefone"], leitura= leitura, tamanho= (33, 1))

        lb_email = self.label("E-mail: ", tamanho=(17,1))
        in_email = self.entrada("email", dados_cliente["email"], leitura= leitura, tamanho= (33, 1))

        lb_endereco = self.label("Endereço: ", tamanho=(17,1))
        in_endereco = self.entrada("endereco", dados_cliente["endereco"], leitura = leitura, tamanho= (33, 1))

        campos = [
                    [lb_cpf, in_cpf],
                    [lb_nome, in_nome],
                    [lb_telefone, in_telefone],
                    [lb_email, in_email],
                    [lb_endereco, in_endereco]
                ]

        return campos

    
    def cadastrar(self, dados_cliente = defaultdict(lambda: None)):
            
        layout = [
                    [self.titulo("Cadastrar Cliente")],
                    list(map(lambda campo : campo, self.campos(dados_cliente))),
                    [
                        self.botao("Cadastrar", "bt-cadastrar", tamanho=(20,1)), 
                        self.botao("Voltar", "bt-voltar", tamanho=(20, 1))
                    ]
                ]

        self.window = self.janela(layout)
        return self.read()

    def mostrar(self, dados_cliente = {}):

        layout = [
                    [self.titulo(dados_cliente["nome"])],
                    list(map(lambda campo : campo, self.campos(dados_cliente, leitura = True))),
                    [
                        self.botao("Alterar", "bt-alterar", tamanho=(12,1)), 
                        self.botao("Remover", "bt-remover", tamanho=(12,1)), 
                        self.botao("Voltar", "bt-voltar", tamanho=(12,1))
                    ]
                ]
       
        self.window = self.janela(layout)
        return self.read()

    def alterar(self, dados_cliente = {}):
        
        layout = [
                    [self.titulo(dados_cliente["nome"])],
                    list(map(lambda campo : campo, self.campos(dados_cliente))),
                    [
                        self.botao("Concluir", "bt-concluir", tamanho=(20,1)), 
                        self.botao("Voltar", "bt-voltar", tamanho=(20,1))
                    ]
                ]
        
        self.window = self.janela(layout)
        
        return self.read()