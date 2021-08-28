from telas.tela_venda import TelaVenda
from entidades.venda import Venda
from controladores.controlador_abstrato import Controlador
from entidades.item import Item
from entidades.funcionario import Funcionario
from entidades.cliente import Cliente
from entidades.produto import Produto


class ControladorVendas(Controlador):
    def __init__(self, controlador_central: Controlador):
        super().__init__(TelaVenda(self))
        self.__vendas: list[Venda] = []
        self.__controlador_central = controlador_central
        self.__codigo_atual = 0
        
    def abre_tela_inicial(self):
        switcher = {
            0: False, 
            1: self.cadastra_venda,
            2: self.lista_vendas,
            3: self.lista_encomendas,
            4: self.conclui_encomenda,
            5: self.cancela_encomenda, 
            6: self.lista_vendas_por_cliente,
            7: self.lista_vendas_por_funcionario,
            8: self.seleciona_venda_por_codigo}

        opcoes = {
            1: "Cadastrar Venda", 
            2: "Listar Vendas", 
            3: "Listar Encomendas", 
            4: 'Concluir Encomenda', 
            5: "Cancelar Encomenda", 
            6: 'Listar Vendas por Cliente', 
            7: 'Listar Vendas por Funcionário',
            8: "Pesquisar Venda", 
            0: "Voltar"
        }
        
        while True:
            opcao = self.tela.mostra_opcoes(opcoes, "--------- Vendas ---------")
            funcao_escolhida = switcher[opcao]
            if funcao_escolhida:
                funcao_escolhida()
            else:
                break
            
    def cadastra_venda(self):
        opcoes = {1: "Continuar cadastrando venda", 0: "Voltar"}

        while True:
            dados_venda = self.tela.recebe_dados_venda('Cadastra Venda')
                
            funcionario = self.__controlador_central.controlador_funcionarios.verifica_se_ja_existe_funcionario_com_matricula(dados_venda['atendente'])
            if isinstance(funcionario, Funcionario):
                dados_venda['atendente'] = funcionario
            else:
                self.tela.mensagem_erro('Obrigatório informar um atendente.')
                break
            
            venda_inicializada = self.inicializa_venda(dados_venda)
            self.tela.quebra_linha()

            if dados_venda['encomenda'] == 's':
                venda_inicializada = self.solicita_dados_encomenda(venda_inicializada)
            else:
                data = self.solicita_cliente(venda_inicializada)
                if isinstance(data, Venda):
                    venda_inicializada = data
        
            self.tela.quebra_linha()

            venda_inicializada = self.solicita_itens(venda_inicializada)
            
            if isinstance(venda_inicializada, Venda) and venda_inicializada.itens:                
                venda_inicializada = self.solicita_desconto(venda_inicializada)
            else:
                self.tela.mensagem_erro('Cadastro de venda cancelado!')
                break
            
            if isinstance(venda_inicializada, Venda):
                try:
                    if dados_venda["encomenda"] == "s":
                        self.__controlador_central.controlador_estoque.processa_venda(venda_inicializada)
                    self.__vendas.append(venda_inicializada)
                    self.__codigo_atual += 1
                    self.tela.mensagem('Venda cadastrada com sucesso!')  
                except ValueError:
                    self.tela.mensagem("Venda cancelada")
            
            opcao = self.tela.mostra_opcoes(opcoes)
            if opcao == 0:
                break
        
    def solicita_cliente(self, venda: Venda):
        opcoes = {1: "Sim", 0: "Não"}
        opcao = self.tela.mostra_opcoes(opcoes, "----- Cadastrar cliente? -----")
        
        while opcao == 1:
            opcoes = {1: "Tentar novamente", 0: "Voltar"}
            cpf_cliente = self.tela.solicita_cpf_cliente()
            cliente = self.__controlador_central.controlador_clientes.verifica_se_ja_existe_cliente_com_cpf(cpf_cliente)
            if isinstance(cliente, Cliente):
                venda.cliente = cliente
                return venda
            else:
                self.tela.mensagem_erro('Não existe esse cliente cadastrado com esse cpf no sistema.')
                opcao = self.tela.mostra_opcoes(opcoes)
                if opcao == 0:
                    break
        
            
    def solicita_desconto(self, venda):
        
        desconto = self.tela.solicita_desconto()
        venda.desconto = desconto
        return venda
                    
    
    def solicita_dados_encomenda(self, venda):
                
        dados_encomenda = self.tela.solicita_dados_encomenda()
        cliente = self.__controlador_central.controlador_clientes.verifica_se_ja_existe_cliente_com_cpf(dados_encomenda['cliente'])
        if isinstance(cliente, Cliente):
            venda.data_entrega = dados_encomenda['data_entrega']
            venda.cliente = cliente
            venda.entregue = False
            return venda
                          
            
    def solicita_itens(self, venda):
        while True:
            dados_item = self.tela.solicita_item()
            self.tela.quebra_linha()
            if dados_item['quantidade'] > 0:
                produto = self.__controlador_central.controlador_produtos.seleciona_produto_por_codigo(dados_item['produto'])
                if isinstance(produto, Produto):
                    venda.inclui_item(produto, dados_item['quantidade'])
                    opcoes = {1: "Continuar", 0: "Voltar" }
                    opcao = self.tela.mostra_opcoes(opcoes)
                else:
                    self.tela.mensagem_erro('Tente novamente, produto não encontrado.')
                    opcoes = {1: "Tentar novamente", 0: "Concluir" if len(venda.itens) > 0 else "Cancelar cadastro da venda" }
                    opcao = self.tela.mostra_opcoes(opcoes)
                    
            else:
                self.tela.mensagem_erro('Digite uma quantidade maior que zero!')
                opcoes = {1: "Tentar novamente", 0: "Voltar" if len(venda.itens) > 0 else "Cancelar cadastro da venda" }
                opcao = self.tela.mostra_opcoes(opcoes)
                
            if opcao == 0:
                break    
        
        return venda if venda.itens else None
        
    def inicializa_venda(self, dados_venda) -> Venda:
        if dados_venda['encomenda'] == 's':
            encomenda = True
        else:
            encomenda = False
            
        venda =  Venda(
            self.__codigo_atual,
            dados_venda['atendente'],
            encomenda
        )
        return venda
        
    def lista_vendas(self):
        self.tela.cabecalho('Lista Vendas')

        if len(self.__vendas) > 0:
            for venda in self.__vendas:
                self.lista_venda(venda)
        
        else:
            self.tela.mensagem_erro('Nenhuma venda encontrada.')
            
                
    def lista_venda(self, venda): 
        self.tela.cabecalho("Encomenda" if venda.encomenda else "Venda")
        
        if venda.encomenda == True:
            self.tela.mostra_dados_encomenda({
                'data_entrega': venda.data_entrega,
                'entregue': 'Sim' if venda.entregue else 'Não'
            })
            
        self.tela.mostra_venda({
            'codigo': venda.codigo,
            'atendente': venda.atendente.nome,
            'encomenda': 'Sim' if venda.encomenda else 'Não'
        })
                
        if venda.cliente or venda.encomenda == True:
            self.tela.mostra_cliente(
                venda.cliente.nome
            )       
       
        
        self.mostra_itens(venda.itens)
        
        self.tela.mostra_valores({
            'preco_final': venda.preco_final,
            'desconto': venda.desconto,
        })
        
    def mostra_itens(self, itens):
        self.tela.cabecalho("Itens")
        for item in itens:
            self.tela.mostra_item({
                'produto': item.produto.nome,
                'quantidade': item.quantidade,
                'valor_unitario': item.produto.preco_venda
            })
            
    def lista_encomendas(self):
        self.tela.cabecalho('Lista Encomendas')
        encomenda = False
        
        for venda in self.__vendas:
            if venda.encomenda == True and venda.entregue == False:
                self.lista_venda(venda) 
                encomenda = True  
        if encomenda is False:
            self.tela.mensagem_erro('Nenhuma encomenda encontrada.')
            
                
            
                        
    def lista_vendas_por_cliente(self):
        opcoes = {1: "Listar novamente", 0: "Voltar"}
        while True:
            cpf = self.tela.solicita_cpf_cliente()
            self.tela.quebra_linha()
            encontrada = False
            if len(self.__vendas) > 0:
                for venda in self.__vendas:
                    if venda.cliente and venda.cliente.cpf == cpf:
                        self.lista_venda(venda)
                        encontrada = True
                if encontrada is False:
                    self.tela.mensagem("Nenhuma venda deste cliente encontrada")
            else:
                self.tela.mensagem_erro('Nenhuma venda encontrada.')
                break
            
            opcao = self.tela.mostra_opcoes(opcoes)
            if opcao == 0:
                break
       
            
    def lista_vendas_por_funcionario(self):
        opcoes = {1: "Listar novamente", 0: "Voltar"}
        while True:
            encontrada = False
            matricula = self.tela.solicita_matricula_funcionario()
            self.tela.quebra_linha()
            if len(self.__vendas) > 0:
                for venda in self.__vendas:
                    if venda.atendente and venda.atendente.matricula == matricula:
                        self.lista_venda(venda)
                        encontrada = True
                if encontrada is False:
                    self.tela.mensagem("Nenhuma venda deste funcionário encontrada")
            else:
                self.tela.mensagem_erro('Nenhuma venda encontrada.')
                break
            
            opcao = self.tela.mostra_opcoes(opcoes)
            if opcao == 0:
                break
            
    
    def conclui_encomenda(self):
        codigo_venda = self.tela.solicita_codigo_venda('Concluir encomenda')
        venda = self.verifica_se_ja_existe_venda_com_codigo(codigo_venda)
        self.tela.quebra_linha()
        
        if isinstance(venda, Venda) and venda.encomenda == True:
            if venda.entregue == False:
                try:
                    self.__controlador_central.controlador_estoque.processa_venda(venda)
                    venda.entregue = True
                except ValueError:
                    self.tela.mensagem_erro("Entrega cancelada")
                self.tela.mensagem("Encomenda concluída com sucesso.")
            else:
                self.tela.mensagem("Encomenda já entregue.")
        else:
            self.tela.mensagem_erro('Não existe encomenda com esse código.')
            
    def cancela_encomenda(self):
        codigo_venda = self.tela.solicita_codigo_venda('Cancelar encomenda')
        venda = self.verifica_se_ja_existe_venda_com_codigo(codigo_venda)
        self.tela.quebra_linha()
        
        if isinstance(venda, Venda) and venda.encomenda == True:
            if venda.entregue == False:
                self.__vendas.remove(venda)
                self.tela.mensagem("Encomenda cancelada com sucesso.")
            else:
                self.tela.mensagem("Encomenda não pode ser cancelada pois já foi entregue.")
        else:
            self.tela.mensagem_erro('Não existe encomenda com esse código.')
            
        
                 
    def seleciona_venda_por_codigo(self):
        
        codigo = self.tela.solicita_codigo_venda('Pesquisa Venda')       
        venda = self.verifica_se_ja_existe_venda_com_codigo(codigo)
        
        if isinstance(venda, Venda):
            self.lista_venda(venda)
        else:
            self.tela.mensagem_erro('Não existe venda com este código.')

    def verifica_se_ja_existe_venda_com_codigo(self, codigo) -> Venda:
        for venda in self.__vendas:
            if codigo == venda.codigo:
                return venda                
        else:
            return None