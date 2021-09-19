from telas.tela_abstrata import Tela


class TelaListaCliente(Tela):
    __instancia = None

    def __new__(cls):
        if TelaListaCliente.__instancia is None:
            TelaListaCliente.__instancia = object.__new__(cls)
        return TelaListaCliente.__instancia

    def __init__(self):
        super().__init__()

    def lista_clientes(self, dados_clientes=[], pesquisa=False):
    
        layout = [
                    [self.titulo("Pesquisa '" + pesquisa + "'") if pesquisa is not False else self.titulo("Clientes")], 
                    self.opcoes(botoes={"Listar": "listar", "Cadastrar": "cadastrar", "Pesquisar": "pesquisar", "Voltar": "voltar"}, selecionado="" if pesquisa else "listar"), 
                    [self.lista(["CPF", "Nome", "Telefone", "E-mail", "Endereço"], dados_clientes, chave="lista")]
                ]
        
        self.window = self.janela(layout, background="#FC9326")
        self.configura_lista("lista")

        return self.read()
