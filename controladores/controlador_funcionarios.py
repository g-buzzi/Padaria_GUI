from controladores.controlador_abstrato import Controlador
from telas.tela_funcionario import TelaFuncionario
from entidades.funcionario import Funcionario
from DAOs.funcionario_dao import FuncionarioDao


class ControladorFuncionarios(Controlador):

    def __init__(self, controlador_central):
        super().__init__(TelaFuncionario(self))
        self.__dao = FuncionarioDao()
        self.__controlador_central = controlador_central

    def abre_tela_inicial(self):
        switcher = {0: False, 1: self.cadastra_funcionario, 2: self.altera_funcionario, 3: self.remove_funcionario,
                    4: self.lista_funcionarios, 5: self.seleciona_funcionario_por_matricula}

        opcoes = {1: "Cadastrar", 2: "Alterar", 3: "Remover", 4: "Listar", 5: "Pesquisar", 0: "Voltar"}
        while True:
            opcao = self.tela.mostra_opcoes(opcoes, "--------- Funcionários ---------")
            funcao_escolhida = switcher[opcao]
            if funcao_escolhida:
                funcao_escolhida()
            else:
                break

    def cadastra_funcionario(self):
        opcoes = {1: "Continuar cadastrando", 0: "Voltar"}

        while True:
            dados_funcionario = self.tela.recebe_dados_funcionarios('Cadastra')
            self.tela.quebra_linha()
            resposta_matricula = self.verifica_se_ja_existe_funcionario_com_matricula(dados_funcionario['matricula'])
            resposta_cpf = self.verifica_se_ja_existe_funcionario_com_cpf(dados_funcionario['cpf'])
            if resposta_matricula:
                self.tela.mensagem_erro('Já existe funcionário com essa matrícula.')
                break
            elif resposta_cpf:
                self.tela.mensagem_erro('Já existe funcionário com esse cpf.')
                break
            else:
                self.salva_dados_funcionario(dados_funcionario)
                self.tela.mensagem('Funcionário cadastrado com sucesso!')
            
            opcao = self.tela.mostra_opcoes(opcoes)
            if opcao == 0:
                break
            
    def verifica_se_ja_existe_funcionario_com_matricula(self, matricula):
        for funcionario in self.__dao.get_all():
            if matricula == funcionario.matricula:
                return funcionario                
        else:
            return None
        
    def verifica_se_ja_existe_funcionario_com_cpf(self, cpf):
        for funcionario in self.__dao.get_all():
            if cpf == funcionario.cpf:
                return funcionario                
        else:
            return None
        
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
        self.tela.cabecalho('Lista Funcionários')

        for funcionario in self.__dao.get_all():
            self.tela.mostra_funcionario({
                'matricula': funcionario.matricula,
                'nome': funcionario.nome,
                'cpf': funcionario.cpf,
                'telefone': funcionario.telefone,
                'email': funcionario.email,
                'salario': funcionario.salario
            })

    def remove_funcionario(self):
        opcoes = {1: "Continuar removendo", 0: "Voltar"}
        while True:
            matricula = self.tela.solicita_matricula_funcionario('Remove Funcionário')

            funcionario = self.verifica_se_ja_existe_funcionario_com_matricula(matricula)
            if isinstance(funcionario, Funcionario):
                self.__dao.remove(funcionario.matricula)
                self.tela.mensagem("Funcionário removido com sucesso") 
            else:
                self.tela.mensagem_erro('Funcionário não encontrado!')
            
            opcao = self.tela.mostra_opcoes(opcoes)
            if opcao == 0:
                break

    def seleciona_funcionario_por_matricula(self):

        matricula = self.tela.solicita_matricula_funcionario('Pesquisa Funcionário')

        for funcionario in self.__dao.get_all():
            if funcionario.matricula == matricula:
                self.tela.mostra_funcionario({
                    'matricula': funcionario.matricula,
                    'nome': funcionario.nome,
                    'cpf': funcionario.cpf,
                    'telefone': funcionario.telefone,
                    'email': funcionario.email,
                    'salario': funcionario.salario
                })
                break
        else:
            self.tela.mensagem("Nenhum funcionário com essa matrícula encontrada")

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