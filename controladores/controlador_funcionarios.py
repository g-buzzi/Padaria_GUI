from excecoes.not_found_exception import NotFoundException
from excecoes.duplicated_exception import DuplicatedException
from excecoes.input_error import InputError
from telas.tela_mostra_funcionario import TelaMostraFuncionario
from controladores.controlador_abstrato import Controlador
from entidades.funcionario import Funcionario
from DAOs.funcionario_dao import FuncionarioDao
from telas.tela_lista_funcionario import TelaListaFuncionario
from excecoes.empty_field import EmptyFieldError


class ControladorFuncionarios(Controlador):
 
    __instancia = None

    def __new__(cls):
        if ControladorFuncionarios.__instancia is None:
            ControladorFuncionarios.__instancia = object.__new__(cls)
        return ControladorFuncionarios.__instancia

    def __init__(self):
        super().__init__(TelaListaFuncionario())
        self.__dao = FuncionarioDao()
        self.__pesquisa = False
        self.__lista = []

    def inicia(self):
        self.abre_tela_inicial()

    def dados_funcionarios(self):
        dados = []
        for funcionario in self.__dao.get_objects():
            dados.append([funcionario.matricula, funcionario.nome, funcionario.cpf,
                          funcionario.telefone, funcionario.email, funcionario.salario])
        return dados

    def listar(self, valores = None):
        self.__pesquisa = False


    def abre_tela_inicial(self, dados=None):
        switcher = {"cadastrar": self.cadastra_funcionario, 
                    "pesquisar": self.pesquisar, 
                    "lista_clique_duplo": self.mostrar_funcionario,
                    "listar": self.listar}
        self.listar()
        while True:
            if self.__pesquisa is False:
                self.__lista = self.dados_funcionarios()
            else:
                self.__lista = self.pesquisa_funcionarios(self.__pesquisa)
            self.tela = TelaListaFuncionario()
            botao, valores = self.tela.lista_funcionarios(self.__lista, self.__pesquisa)
            
            if botao == 'voltar':
                self.tela.close()
                break

            switcher[botao](valores)


    def pesquisar(self, valores = None):
        self.tela = TelaListaFuncionario()
        texto_pesquisado = self.tela.pesquisar('Nome ou matrícula:')

        if texto_pesquisado:
            self.__pesquisa = texto_pesquisado
        else:
            self.tela.close()
    
    def pesquisa_funcionarios(self, texto_pesquisado):
        funcionarios = []
        for funcionario in self.__dao.get_objects():
            if texto_pesquisado.lower() in funcionario.nome.lower() or texto_pesquisado in str(funcionario.matricula):
                funcionarios.append([funcionario.matricula, funcionario.nome, funcionario.cpf,
                                    funcionario.telefone, funcionario.email, funcionario.salario])
        return funcionarios


    def tratar_dados(self, dados: dict):
        
        dados["matricula"] = self.formata_int(dados["matricula"], "Matrícula")
        dados["nome"] = self.formata_string(dados["nome"])
        dados["cpf"] = self.formata_string(dados["cpf"])
        dados["email"] = self.formata_string(dados["email"])
        dados["telefone"] = self.formata_int(dados["telefone"], "Telefone")
        dados["salario"] = self.formata_float(dados["salario"], "Salário")
        return dados

    def cadastra_funcionario(self, valores):
        while True:
            self.tela = TelaMostraFuncionario()
            botao, dados_funcionario = self.tela.cadastra()
            if botao != 'volta':
                try:
                    dados_funcionario = self.tratar_dados(dados_funcionario)
                except InputError as e:
                    self.tela.mensagem_erro(e.mensagem)
                    continue
                try:
                    self.verifica_se_ja_existe_funcionario_com_matricula(dados_funcionario['matricula'])
                    self.verifica_se_ja_existe_funcionario_com_cpf(dados_funcionario['cpf'])
                    self.salva_dados_funcionario(dados_funcionario)
                    self.tela.mensagem('Funcionário cadastrado com sucesso!')
                except DuplicatedException as e:
                    self.tela.mensagem_erro(str(e))
                    continue
            
            self.tela.close()
            break

    def mostrar_funcionario(self, dados):
   
        selecionado = dados["lista"][0]
        matricula_funcionario = self.__lista[selecionado][0]
       
        while True:
            try:
                funcionario = self.__dao.get(matricula_funcionario)
                self.tela = TelaMostraFuncionario()
                botao, dados = self.tela.mostra(self.dados_funcionario(funcionario))
            except NotFoundException as e:
                self.tela.mensagem_erro(str(e))

            if botao == 'remove':
                self.remove_funcionario(matricula_funcionario)
                break
            
            if botao == 'inicia_alteracao':
                self.alterar_funcionario(self.dados_funcionario(funcionario))
                break

            if botao == 'volta':
                break
                
            self.tela.close


    def dados_funcionario(self, funcionario: Funcionario) -> dict:
        dados = {
            "matricula": funcionario.matricula, 
            "nome": funcionario.nome, 
            "cpf": funcionario.cpf, 
            "email": funcionario.email, 
            "telefone": funcionario.telefone,
            "salario": funcionario.salario
        }
        return dados
            
    def verifica_se_ja_existe_funcionario_com_matricula(self, matricula):
        for funcionario in self.__dao.get_objects():
            if matricula and matricula == funcionario.matricula:
                raise DuplicatedException(mensagem_personalizada='Já existe funcionário com essa matrícula.')
        
    def verifica_se_ja_existe_funcionario_com_cpf(self, cpf):
        for funcionario in self.__dao.get_objects():
            if cpf == funcionario.cpf:
                raise DuplicatedException(mensagem_personalizada='Já existe funcionário com esse cpf.')
        
    def seleciona_funcionario_por_matricula(self, matricula: int) -> Funcionario:
        
        for funcionario in self.__dao.get_objects():
            if matricula == funcionario.matricula:
                funcionario_encontrado = funcionario
        
        if not funcionario_encontrado:
            raise NotFoundException(entidade='Funcionário')

        return funcionario_encontrado

    def salva_dados_funcionario(self, dados_funcionario):
        self.__dao.add(Funcionario(
            dados_funcionario['matricula'],
            dados_funcionario['nome'],
            dados_funcionario['cpf'],
            dados_funcionario['telefone'],
            dados_funcionario['email'],
            dados_funcionario['salario']
        ))

    def lista_funcionarios(self):
        self.tela = TelaListaFuncionario()
        self.tela.lista_funcionarios(self.dados_funcionarios())

    def remove_funcionario(self, matricula: int):
        self.__dao.remove(matricula)
        self.tela.mensagem("Funcionário removido com sucesso")
  

    def alterar_funcionario(self, dados_funcionario: dict):
        while True:
            self.tela = TelaMostraFuncionario()
            botao, dados = self.tela.altera(dados_funcionario)
            
            if botao == 'volta':
                break

            try:
                dados = self.tratar_dados(dados)          
            
                funcionario_novo = Funcionario(dados['matricula'], dados['nome'], dados['cpf'], dados['telefone'], dados['email'], dados['salario'])
                if botao == 'conclui_alteracao':
                    try:
                        if dados['matricula'] != dados_funcionario['matricula']:
                            self.verifica_se_ja_existe_funcionario_com_matricula(dados['matricula'])
                        if dados['cpf'] != dados_funcionario['cpf']:
                            self.verifica_se_ja_existe_funcionario_com_cpf(dados['cpf'])
        
                        self.__dao.update(dados_funcionario['matricula'], funcionario_novo)
                        self.tela.mensagem("Funcionário atualizado com sucesso")
                        break
                    except DuplicatedException as e:
                        self.tela.mensagem_erro(str(e))
            
            except InputError as e:
                self.tela.mensagem_erro(e.mensagem)
                continue