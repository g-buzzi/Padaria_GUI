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
        if pesquisa is not False:
            titulo = self.titulo("Pesquisa '" + pesquisa + "'")
        else:
            titulo = self.titulo("Funcionários")
        botoes = {"Listar": "listar", "Cadastrar": "cadastrar", "Pesquisar": "pesquisar", "Voltar": "voltar"}
        selecionado = "listar"
        if pesquisa:
            selecionado = ""
        opcoes = self.opcoes(botoes, selecionado=selecionado)
        lista = self.lista(["Matrícula", "Nome", "CPF", "Telefone", "E-mail", "Salário"], dados_funcionarios, chave="lista")
        layout = [[titulo], opcoes, [lista]]
        self.window = self.janela(layout=layout, background="#FC9326")
        self.configura_lista("lista")
        return self.read()
