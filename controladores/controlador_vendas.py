from collections import defaultdict
from excecoes.empty_field import EmptyFieldError
from entidades.item import Item
from controladores.controlador_produtos import ControladorProdutos
from controladores.controlador_clientes import ControladorClientes
from excecoes.not_found_exception import NotFoundException
from controladores.controlador_funcionarios import ControladorFuncionarios
from excecoes.duplicated_exception import DuplicatedException
from excecoes.input_error import InputError
from telas.tela_mostra_venda import TelaMostraVenda
from telas.tela_lista_venda import TelaListaVenda
from telas.tela_venda import TelaVenda
from entidades.venda import Venda
from controladores.controlador_abstrato import Controlador
from entidades.funcionario import Funcionario
from entidades.cliente import Cliente
from entidades.produto import Produto
from DAOs.venda_dao import VendaDao


class ControladorVendas(Controlador):

    __instancia = None

    def __new__(cls):
        if ControladorVendas.__instancia is None:
            ControladorVendas.__instancia = object.__new__(cls)
        return ControladorVendas.__instancia

    def __init__(self):
        super().__init__(TelaListaVenda())
        self.__dao = VendaDao()
        self.__pesquisa = False

    def inicia(self):
        self.abre_tela_inicial()

    def dados_vendas(self):
        dados = []
        for venda in self.__dao.get_objects():
            dados.append([venda.codigo, venda.atendente.nome, venda.cliente.nome if isinstance(venda.cliente, Cliente) else '--', venda.encomenda, venda.preco_final])
        return dados

    def listar(self, valores = None):
        self.__pesquisa = False
        self.tela = TelaListaVenda()
        self.__lista = self.dados_vendas()
        return self.tela.lista_vendas(self.__lista, self.__pesquisa)


    def abre_tela_inicial(self, dados=None):
        switcher = {"cadastrar": self.cadastra_venda, 
                    "pesquisar": self.listar, 
                    "lista_clique_duplo": self.mostrar_venda,
                    "listar": self.listar}
        
        while True:
            botao, valores = self.listar()
            
            if botao == 'voltar':
                self.tela.close()
                break

            switcher[botao](valores)

    def cadastra_venda(self, valores):
        self.tela = TelaMostraVenda()
        dados_venda = defaultdict(lambda : None)
        dados_venda['lista'] = []
        itens = []
        botao, tipo = self.tela.opcoes_vendas()
        continue_while = True

        if botao == 'bt-cancelar':
            self.tela.close()

        while True:
            botao_tela_cadastro, dados_form = self.tela.cadastrar(dados_venda, tipo='tipo_encomenda' if tipo['tipo_encomenda'] else 'tipo_venda')
            
            if botao_tela_cadastro == 'bt_adicionar_item':
           
                item = self.adicionar_item()
                if isinstance(item, Item):
                    dados_venda['lista'].append([item.produto.codigo, item.produto.nome, item.quantidade, item.produto.preco_venda ])
                    itens.append(item)
                botao_tela_cadastro = None           
            
                    
            if botao_tela_cadastro == 'bt-cadastrar':
                try:
                    dados_form['itens'] = itens
                    dados_venda = self.tratar_dados(dados_form, tipo='tipo_encomenda' if tipo['tipo_encomenda'] else 'tipo_venda')
                    self.salva_dados_venda(dados_form)
                    self.tela.mensagem('Venda cadastrada com sucesso!')
                    self.tela.close()
                    break
                except InputError as e:
                    self.tela.mensagem_erro(e.mensagem)
                    continue
                except DuplicatedException as e:
                    self.tela.mensagem_erro(str(e))
                    continue

            if botao_tela_cadastro == 'bt-voltar':
                self.tela.close()

    def mostrar_venda(self, dados):

        selecionado = dados["lista"][0]
        codigo_venda = self.__lista[selecionado][0]
       
        while True:

            try:
                venda = self.__dao.get(codigo_venda)
                self.tela = TelaMostraVenda()
                botao, dados = self.tela.mostrar(self.dados_venda(venda))
            except NotFoundException as e:
                self.tela.mensagem_erro(str(e))

            if botao == 'bt-entregar':
                self.conclui_encomenda(venda)
                break

            if botao == 'bt-cancelar':
                self.__dao.remove(codigo_venda)
                self.tela.mensagem("Encomenda cancelada com sucesso.")
                break
                
            if botao == 'bt-voltar':
                break
                
            self.tela.close
                
    def dados_venda(self, venda: Venda) -> dict:
        dados = {
            "codigo": venda.codigo,
            "atendente": venda.atendente.nome,
            "encomenda": venda.encomenda,
            "desconto": venda.desconto,
            "data_entrega": venda.data_entrega,
            "cliente": venda.cliente.nome if isinstance(venda.cliente, Cliente) else '--',
            "itens": venda.itens,
            "entregue": 'Sim' if venda.entregue else 'Não',
            "preco_final": venda.preco_final
        }
        return dados

    def adicionar_item(self):
        botao, valores = self.tela.adiciona_item_venda()
        codigo = self.formata_int(valores['codigo_produto'], 'Código')
        if botao == 'adicionar':
            try:
                item = Item(ControladorProdutos().seleciona_produto_por_codigo(codigo), valores['quantidade'])
                return item
            except NotFoundException as e:
                self.tela.mensagem_erro(str(e))
     
        self.tela.close()

    def salva_dados_venda(self, dados_venda):
        self.__dao.add(Venda(
                    dados_venda['codigo'],
                    dados_venda['atendente'],
                    dados_venda['encomenda'],
                    dados_venda['desconto'],
                    dados_venda['data_entrega'],
                    dados_venda['cliente'],
                    dados_venda['itens']
                ))

    def tratar_dados(self, dados: dict, tipo=None):
        dados['cliente'] = self.seleciona_cliente(dados['cliente'], tipo)
        dados['data_entrega'] = self.formata_string(dados['data_entrega']) if tipo == 'tipo_encomenda' else None
        dados["encomenda"] = True if tipo == 'tipo_encomenda' else False
        dados["atendente"] = self.seleciona_atendente(dados['atendente'])
        dados["desconto"] = self.formata_float(dados["desconto"] if dados["desconto"] else 0, 'Desconto')
        dados["codigo"] = self.formata_int(dados["codigo"], 'Código')
        dados["itens"] = self.trata_itens(dados["itens"])

        return dados

    def trata_itens(self, itens):

        if len(itens) == 0:
            raise EmptyFieldError("Obrigatório algum item para venda!")
        else:
            return itens

    def seleciona_atendente(self, matricula: int) -> Funcionario:
        try:
            matricula = self.formata_int(matricula, 'Atendente')
            funcionario = ControladorFuncionarios().seleciona_funcionario_por_matricula(matricula)
            return funcionario
        except NotFoundException as e:
            self.tela.mensagem_erro(str(e))

    def seleciona_cliente(self, cpf: str, tipo: str):
        try:
            cpf = self.formata_string(cpf) if tipo == 'tipo_encomenda' else self.formata_string(cpf, checar_se_vazio=False)
            cliente = ControladorClientes().seleciona_cliente_por_cpf(cpf)
            return cliente
        except NotFoundException:
            return None
      

    def mostra_itens(self, itens):
        self.tela.cabecalho("Itens")
        for item in itens:
            self.tela.mostra_item({
                'produto': item.produto.nome,
                'quantidade': item.quantidade,
                'valor_unitario': item.produto.preco_venda
            })


    def conclui_encomenda(self, venda: Venda):

        venda_atualizada = venda
        venda_atualizada.entregue = True
        self.__dao.update(venda.codigo, venda_atualizada)
        self.tela.mensagem("Encomenda entregue com sucesso.")
           

    def verifica_se_ja_existe_venda_com_codigo(self, codigo) -> Venda:
        for venda in self.__dao.get_all():
            if codigo == venda.codigo:
                return venda
        else:
            return None