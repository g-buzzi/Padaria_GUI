from telas.tela_abstrata import Tela


class TelaListaFuncionario(Tela):
    __instancia = None

    def __new__(cls):
        if cls.__instancia is None:
            cls.__instancia = super().__new__(cls)
        return cls.__instancia

    def __init__(self):
        super().__init__()

    def lista_funcionarios(self, dados_funcionarios=[], pesquisa=False):
   
        layout = [
                    [self.titulo("Pesquisa '" + pesquisa + "'") if pesquisa is not False else self.titulo("Funcionários")], 
                    self.opcoes(botoes= {"Listar": "listar", "Cadastrar": "cadastrar", "Pesquisar": "pesquisar", "Voltar": "voltar"}, selecionado= "" if pesquisa else "listar"), 
                    [self.lista(["Matrícula", "Nome", "CPF", "Telefone", "E-mail", "Salário R$"], dados_funcionarios, chave="lista")]
                ]
                
        self.window = self.janela(layout=layout, background="#FC9326")
        self.configura_lista("lista")
        return self.read()
