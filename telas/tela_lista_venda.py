from telas.tela_abstrata import Tela

class TelaListaVenda(Tela):
    __instancia = None

    def __new__(cls):
        if TelaListaVenda.__instancia is None:
            TelaListaVenda.__instancia = object.__new__(cls)
        return TelaListaVenda.__instancia

    def __init__(self):
        super().__init__()

    def lista_vendas(self, dados_vendas=[], pesquisa=False):
   
        layout = [
                    [self.titulo("Pesquisa '" + pesquisa + "'") if pesquisa is not False else self.titulo("Vendas")], 
                    self.opcoes(botoes= {"Listar": "listar", "Cadastrar": "cadastrar", "Pesquisar": "pesquisar", "Voltar": "voltar"}, selecionado= "" if pesquisa else "listar"), 
                    [self.lista(["Código", "Atendente", "Cliente", "Encomenda", "Total R$"], dados_vendas, chave="lista")]
                ]
                
        self.window = self.janela(layout=layout, background="#FC9326")
        self.configura_lista("lista")
        return self.read()