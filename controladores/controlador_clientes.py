from controladores.controlador_abstrato import Controlador
from telas.tela_cliente import TelaCliente
from entidades.cliente import Cliente

class ControladorClientes(Controlador):

    def __init__(self, controlador_central):
        super().__init__(TelaCliente(self))
        self.__clientes: list[Cliente] = []
        self.__controlador_central = controlador_central
        
    def abre_tela_inicial(self):
        switcher = {
            0: False, 
            1: self.cadastra_cliente, 
            2: self.altera_cliente,
            3: self.remove_cliente,
            4: self.lista_clientes,
            5: self.seleciona_cliente_por_cpf}

        opcoes = {1: "Cadastrar", 2: "Alterar", 3: "Remover", 4: "Listar", 5: "Pesquisar", 0: "Voltar"}
        while True:
            opcao = self.tela.mostra_opcoes(opcoes, "--------- Clientes ---------")
            funcao_escolhida = switcher[opcao]
            if funcao_escolhida:
                funcao_escolhida()
            else:
                break
            
    def cadastra_cliente(self):
        opcoes = {1: "Continuar cadastrando", 0: "Voltar"}

        while True:
            dados_cliente = self.tela.recebe_dados_cliente('Cadastra Cliente')
            self.tela.quebra_linha()
            resposta = self.verifica_se_ja_existe_cliente_com_cpf(dados_cliente['cpf'])
            if resposta:
                self.tela.mensagem_erro('Já existe cliente com esse cpf.')
                break
            else:
                self.salva_dados_cliente(dados_cliente)
                self.tela.mensagem("Cliente cadastrado com sucesso!")
            
            opcao = self.tela.mostra_opcoes(opcoes)
            if opcao == 0:
                break
            
    def verifica_se_ja_existe_cliente_com_cpf(self, cpf):
        for cliente in self.__clientes:
            if cpf == cliente.cpf:
                return cliente                
        else:
            return None
        
    def salva_dados_cliente(self, dados_cliente):
        self.__clientes.append(Cliente(
        dados_cliente['nome'],
        dados_cliente['cpf'],
        dados_cliente['telefone'],
        dados_cliente['email'],
        dados_cliente['endereco']
    ))
        
    def lista_clientes(self):
        self.tela.cabecalho('Lista Clientes')

        for cliente in self.__clientes:
            self.tela.mostra_cliente({
                'nome': cliente.nome,
                'cpf': cliente.cpf,
                'telefone': cliente.telefone,
                'email': cliente.email,
                'endereco': cliente.endereco
            })
            
    def remove_cliente(self):
        opcoes = {1: "Continuar removendo", 0: "Voltar"}
        while True:
            cpf = self.tela.solicita_cpf_cliente('Remove Cliente')
            self.tela.quebra_linha()

            cliente = self.verifica_se_ja_existe_cliente_com_cpf(cpf)
            if isinstance(cliente, Cliente):
                self.__clientes.remove(cliente)
                self.tela.mensagem("Cliente removido com sucesso") 
            else:
                self.tela.mensagem_erro('Cliente não encontrado!')
                
            opcao = self.tela.mostra_opcoes(opcoes)
            if opcao == 0:
                break
            
    def seleciona_cliente_por_cpf(self):
    
        cpf = self.tela.solicita_cpf_cliente('Pesquisa Cliente')

        for cliente in self.__clientes:
            if cliente.cpf == cpf:
                self.tela.mostra_cliente({
                    'nome': cliente.nome,
                    'cpf': cliente.cpf,
                    'telefone': cliente.telefone,
                    'email': cliente.email,
                    'endereco': cliente.endereco
                })
                break
        else:
            self.tela.mensagem_erro("Nenhum cliente com este cpf cadastrado")

    def altera_cliente(self):
        opcoes = {1: "Continuar alterando", 0: "Voltar"}

        while True:
            cpf = self.tela.solicita_cpf_cliente('Altera Cliente')

            cliente = self.verifica_se_ja_existe_cliente_com_cpf(cpf)
            
            if isinstance(cliente, Cliente):

                dados_atualizados = self.tela.alteracao_cliente({
                    'nome': cliente.nome,
                    'cpf': cliente.cpf,
                    'telefone': cliente.telefone,
                    'email': cliente.email,
                    'endereco': cliente.endereco
                })
                resposta = self.verifica_se_ja_existe_cliente_com_cpf(dados_atualizados['cpf'])
                
                if cliente.cpf == dados_atualizados['cpf'] or resposta is None:

                    cliente.nome = dados_atualizados['nome']
                    cliente.cpf = dados_atualizados['cpf']
                    cliente.telefone = dados_atualizados['telefone']
                    cliente.email = dados_atualizados['email']
                    cliente.endereco = dados_atualizados['endereco']
                    
                    self.tela.mensagem("Alterações realizadas com sucesso") 
                    
                else:
                    self.tela.mensagem_erro('Esse cpf já existe. Tente novamente!')
                    break
            else:
                self.tela.mensagem_erro('Cliente não encontrado!')
                break
            opcao = self.tela.mostra_opcoes(opcoes)
            if opcao == 0:
                break