from excecoes.duplicated_exception import DuplicatedException
from excecoes.input_error import InputError
from telas.tela_mostra_funcionario import TelaMostraFuncionario
from controladores.controlador_abstrato import Controlador
from entidades.funcionario import Funcionario
from DAOs.funcionario_dao import FuncionarioDao
from telas.tela_lista_funcionario import TelaListaFuncionario


class ControladorFuncionarios(Controlador):
    instancia = None

    def __init__(self, controlador_central):
        super().__init__(TelaListaFuncionario())
        self.__dao = FuncionarioDao()
        self.__controlador_central = controlador_central
        self.__pesquisa = False

    def inicia(self):
        self.abre_tela_inicial()

    def dados_funcionarios(self):
        dados = []
        for funcionario in self.__dao.get_objects():
            dados.append([funcionario.matricula, funcionario.nome, funcionario.cpf,
                          funcionario.telefone, funcionario.email, funcionario.salario])
        return dados

    # ============================================ Listar Funcionários =============================

    def abre_tela_inicial(self, dados=None):
        switcher = {"cadastrar": self.cadastra_funcionario, "pesquisar": self.cadastra_funcionario, "lista_clique_duplo": self.mostrar_funcionario,
                    "listar": self.cadastra_funcionario}
        while True:
            self.tela = TelaListaFuncionario()
            self.__lista = self.dados_funcionarios()
            botao, valores = self.tela.lista_funcionarios(self.__lista, self.__pesquisa)
            
            if botao == 'voltar':
                self.tela.close()
                break

            switcher[botao](valores)


    ###############################################################################################


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
            
            self.tela.close()
            break

    def mostrar_funcionario(self, dados):
        try:
            selecionado = dados["lista"][0]
            matricula_funcionario = self.__lista[selecionado][0]
            funcionario = self.__dao.get(matricula_funcionario)
            self.tela = TelaMostraFuncionario()
            botao, dados = self.tela.mostra(self.dados_funcionario(funcionario))
        except IndexError:
            return

        if botao == 'remove':
            self.remove_funcionario(matricula_funcionario)

        self.tela.close()

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

    def remove_funcionario(self, matricula):
        try:
            self.seleciona_funcionario_por_matricula(matricula)
            self.__dao.remove(matricula)
            self.tela.mensagem("Funcionário removido com sucesso")
        except IndexError as e:
            self.tela.mensagem_erro(e.mensagem)
            

    def seleciona_funcionario_por_matricula(self, matricula: int):
        for funcionario in self.__dao.get_objects():
            if funcionario.matricula == matricula:
                return funcionario
            else:
                raise IndexError(mensagem="Não existe funcionário com essa matrícula")

    def altera_funcionario(self):
        opcoes = {1: "Continuar alterando", 0: "Voltar"}

        while True:
            matricula = self.tela.solicita_matricula_funcionario('Altera Funcionário')

            funcionario = self.verifica_se_ja_existe_funcionario_com_matricula(matricula)
            
            if isinstance(funcionario, Funcionario):

                dados_atualizados = self.tela.alteracao_funcionario({
                    'matricula': funcionario.matricula,
                    'nome': funcionario.nome,
                    'cpf': funcionario.cpf,
                    'telefone': funcionario.telefone,
                    'email': funcionario.email,
                    'salario': funcionario.salario
                })
                resposta_matricula = self.verifica_se_ja_existe_funcionario_com_matricula(dados_atualizados['matricula'])
                resposta_cpf = self.verifica_se_ja_existe_funcionario_com_cpf(dados_atualizados['cpf'])
                
                if funcionario.matricula == dados_atualizados['matricula'] or resposta_matricula is None:
                    if funcionario.cpf == dados_atualizados['cpf'] or resposta_cpf is None:

                        self.__dao.remove(funcionario.matricula)
                        self.__dao.add(Funcionario(dados_atualizados['matricula'],
                                                   dados_atualizados['nome'],
                                                   dados_atualizados['cpf'],
                                                   dados_atualizados['telefone'],
                                                   dados_atualizados['email'],
                                                   dados_atualizados['salario']
                                                   ))
                        
                        self.tela.mensagem("Alterações realizadas com sucesso") 
                    
                    else:
                        self.tela.mensagem_erro('Esse cpf já está em uso por outro funcionário!')
                        break
                    
                else:
                    self.tela.mensagem_erro('Essa matrícula já está em uso por outro funcionário!')
                    break
            else:
                self.tela.mensagem_erro('Funcionário não encontrado!')
                break
            opcao = self.tela.mostra_opcoes(opcoes)
            if opcao == 0:
                break