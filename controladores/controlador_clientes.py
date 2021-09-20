from excecoes.not_found_exception import NotFoundException
from excecoes.duplicated_exception import DuplicatedException
from excecoes.input_error import InputError
from telas.tela_mostra_cliente import TelaMostraCliente
from telas.tela_lista_cliente import TelaListaCliente
from controladores.controlador_abstrato import Controlador
from entidades.cliente import Cliente
from DAOs.cliente_dao import ClienteDao

class ControladorClientes(Controlador):
    __instancia = None

    def __new__(cls):
        if ControladorClientes.__instancia is None:
            ControladorClientes.__instancia = object.__new__(cls)
        return ControladorClientes.__instancia
    
    def __init__(self):
        super().__init__(TelaListaCliente())
        self.__dao = ClienteDao()
        self.__pesquisa = False
        self.__lista = []

    def inicia(self):
        self.abre_tela_inicial()

    def dados_clientes(self):
        dados = []
        for cliente in self.__dao.get_objects():
            dados.append([cliente.cpf, cliente.nome,
                          cliente.telefone, cliente.email, 
                          cliente.endereco])
        return dados

    def listar(self, valores = None):
        self.__pesquisa = False

    def abre_tela_inicial(self, dados=None):
        switcher = {"cadastrar": self.cadastra_cliente, 
                    "pesquisar": self.pesquisar, 
                    "lista_clique_duplo": self.mostrar_cliente,
                    "listar": self.listar}
        self.listar()
        while True:
            if self.__pesquisa is False:
                self.__lista = self.dados_clientes()
            else:
                self.__lista = self.pesquisa_clientes(self.__pesquisa)
            self.tela = TelaListaCliente()
            botao, valores = self.tela.lista_clientes(self.__lista, self.__pesquisa)
            
            if botao == 'voltar':
                self.tela.close()
                break

            switcher[botao](valores)
        
    def cadastra_cliente(self, valores):
        while True:
            self.tela = TelaMostraCliente()
            botao, dados_cliente = self.tela.cadastrar()
            if botao != 'bt-voltar':
                try:
                    dados_cliente = self.tratar_dados(dados_cliente)
                except InputError as e:
                    self.tela.mensagem_erro(e.mensagem)
                    continue
                try:
                    self.verifica_se_ja_existe_cliente_com_cpf(dados_cliente['cpf'])
                    self.salva_dados_cliente(dados_cliente)
                    self.tela.mensagem('Cliente cadastrado com sucesso!')
                except DuplicatedException as e:
                    self.tela.mensagem_erro(str(e))
                    continue
            
            self.tela.close()
            break

    def mostrar_cliente(self, dados):
   
        selecionado = dados["lista"][0]
        cpf_cliente = self.__lista[selecionado][0]
       
        while True:
            try:
                cliente = self.__dao.get(cpf_cliente)
                self.tela = TelaMostraCliente()
                botao, dados = self.tela.mostrar(self.dados_cliente(cliente))
            except NotFoundException as e:
                self.tela.mensagem_erro(str(e))

            if botao == 'bt-remover':
                self.remove_cliente(cpf_cliente)
                break
            
            if botao == 'bt-alterar':
                self.alterar_cliente(self.dados_cliente(cliente))
                break

            if botao == 'bt-voltar':
                break
                
            self.tela.close

    def alterar_cliente(self, dados_cliente: dict):
        while True:
            self.tela = TelaMostraCliente()
            botao, dados = self.tela.alterar(dados_cliente)
            
            if botao == 'bt-voltar':
                break

            try:
                dados = self.tratar_dados(dados)          
            
                cliente_novo = Cliente(dados['cpf'], dados['nome'], dados['telefone'], dados['email'], dados['endereco'])
                if botao == 'bt-concluir':
                    try:
                        if dados['cpf'] != dados_cliente['cpf']:
                            self.verifica_se_ja_existe_cliente_com_cpf(dados['cpf'])
        
                        self.__dao.update(dados_cliente['cpf'], cliente_novo)
                        self.tela.mensagem("Cliente atualizado com sucesso")
                        break
                    except DuplicatedException as e:
                        self.tela.mensagem_erro(str(e))
            
            except InputError as e:
                self.tela.mensagem_erro(e.mensagem)
                continue


    def remove_cliente(self, cpf: str):
        self.__dao.remove(cpf)
        self.tela.mensagem("Cliente removido com sucesso")

    def pesquisar(self, valores = None):
        self.tela = TelaListaCliente()
        texto_pesquisado = self.tela.pesquisar('Nome ou cpf:')

        if texto_pesquisado:
            self.__pesquisa = texto_pesquisado
        else:
            self.tela.close()

    def pesquisa_clientes(self, texto_pesquisado: str):
        clientes: Cliente = []
        for cliente in self.__dao.get_objects():
            if texto_pesquisado.lower() in cliente.nome.lower() or texto_pesquisado.lower() in cliente.cpf.lower():
                clientes.append([cliente.cpf, cliente.nome,
                                    cliente.telefone, cliente.email, cliente.endereco])
        return clientes

    def dados_cliente(self, cliente: Cliente) -> dict:
        dados = {
            "cpf": cliente.cpf, 
            "nome": cliente.nome, 
            "telefone": cliente.telefone,
            "email": cliente.email, 
            "endereco": cliente.endereco
        }
        return dados

    def tratar_dados(self, dados: dict):
    
        dados["cpf"] = self.formata_string(dados["cpf"])
        dados["nome"] = self.formata_string(dados["nome"])
        dados["telefone"] = self.formata_int(dados["telefone"], "Telefone")
        dados["email"] = self.formata_string(dados["email"])
        dados["endereco"] = self.formata_string(dados["endereco"])
        return dados

            
    def verifica_se_ja_existe_cliente_com_cpf(self, cpf):
        for cliente in self.__dao.get_objects():
            if cpf == cliente.cpf:
                raise DuplicatedException(mensagem_personalizada='Já existe cliente com esse cpf.')
        
    def salva_dados_cliente(self, dados_cliente):
        self.__dao.add(Cliente(
        dados_cliente['cpf'],
        dados_cliente['nome'],
        dados_cliente['telefone'],
        dados_cliente['email'],
        dados_cliente['endereco']
    ))