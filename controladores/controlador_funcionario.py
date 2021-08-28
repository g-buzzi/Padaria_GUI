from typing import List

from controladores.controlador_abstrato import Controlador
from telas.tela_funcionario import TelaFuncionario
from entidades.funcionario import Funcionario


class ControladorFuncionario(Controlador):

    def __init__(self, controlador_central):
        super().__init__(TelaFuncionario(self))
        self.__funcionarios: List[Funcionario] = []
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
            resposta = self.verifica_se_ja_existe_funcionario_com_matricula(dados_funcionario['matricula'])
            if resposta:
                self.tela.mensagem_erro('Já existe funcionário com essa matrícula.')
                break
            else:
                self.salva_dados_funcionario(dados_funcionario)
            
            opcao = self.tela.mostra_opcoes(opcoes)
            if opcao == 0:
                break
            
    def verifica_se_ja_existe_funcionario_com_matricula(self, matricula):
        for funcionario in self.__funcionarios:
            if matricula == funcionario.matricula:
                return funcionario                
        else:
            return None
        
    def salva_dados_funcionario(self, dados_funcionario):
        self.__funcionarios.append(Funcionario(
            dados_funcionario['matricula'],
            dados_funcionario['nome'],
            dados_funcionario['cpf'],
            dados_funcionario['telefone'],
            dados_funcionario['email'],
            dados_funcionario['salario']
        ))

    def lista_funcionarios(self):
        self.tela.adiciona_cabecalho('Lista Funcionários')

        for funcionario in self.__funcionarios:
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
                self.__funcionarios.remove(funcionario)
                self.tela.mensagem("Funcionário removido com sucesso") 
            else:
                self.tela.mensagem_erro('Funcionário não encontrado!')
            
            opcao = self.tela.mostra_opcoes(opcoes)
            if opcao == 0:
                break

    def seleciona_funcionario_por_matricula(self):

        matricula = self.tela.solicita_matricula_funcionario('Pesquisa Funcionário')

        for funcionario in self.__funcionarios:
            if funcionario.matricula == matricula:
                self.tela.mostra_funcionario({
                    'matricula': funcionario.matricula,
                    'nome': funcionario.nome,
                    'cpf': funcionario.cpf,
                    'telefone': funcionario.telefone,
                    'email': funcionario.email,
                    'salario': funcionario.salario
                })

    def altera_funcionario(self):
        opcoes = {1: "Continuar alterando", 0: "Voltar"}

        while True:
            matricula = self.tela.solicita_matricula_funcionario('Altera Funcionário')

            funcionario = self.verifica_se_ja_existe_funcionario_com_matricula(matricula)
            
            if isinstance(funcionario, Funcionario):

                dados_atualizados = self.tela.recebe_dados_funcionarios()
                resposta = self.verifica_se_ja_existe_funcionario_com_matricula(dados_atualizados['matricula'])
                
                if funcionario.matricula == dados_atualizados['matricula'] or resposta is None:

                    funcionario.matricula = dados_atualizados['matricula']
                    funcionario.nome = dados_atualizados['nome']
                    funcionario.cpf = dados_atualizados['cpf']
                    funcionario.telefone = dados_atualizados['telefone']
                    funcionario.email = dados_atualizados['email']
                    funcionario.salario = dados_atualizados['salario']
                    
                    self.tela.mensagem("Alterações realizadas com sucesso") 
                    
                else:
                    self.tela.mensagem_erro('Essa matrícula já existe. Tente novamente!')
                    break
            else:
                self.tela.mensagem_erro('Funcionário não encontrado!')
                break
            opcao = self.tela.mostra_opcoes(opcoes)
            if opcao == 0:
                break