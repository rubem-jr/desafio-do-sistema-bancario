# Desafio Dio - Santander BootCamp 2025
# Criar um sistema bancario
#
# 
# v4:
#   Implementação das funcionalidades:
#       - Decorador de log: decordor aplicado a todas as funções de transações. O decorador registra(printa) 
#                           a data e hora de cda transação, e tipo de transação
#
#       - Gerador de relatorios: gerador que permite iterar sobre as transações de conta e retornar uma a uma, as transações que foram realiadas.
#                                tambem filtra as transações de acordo com seu tipo
#      
#       - Iterador personalizado: permite iterar sobre todas s contas do banco, retornando informações basicas de cada conta(numero,saldo atual,etc).
#
# 
# 
# Informações:
# Realizado por: Rubem Junior
# Usuario GitHub: rubem-jr
# Usuario Dio: juniorrubem50


# Importa as bibliotecas para o funcionamento
from abc import ABC,abstractmethod
from datetime import datetime

class ContasIterador:
    def __init__(self,contas):
        self.contas = contas
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            conta = self.contas[self._index]
            return f"""\
            Agência:\t{conta.agencia}
            Número:\t\t{conta.numero_conta}
            Titular:\t{conta.cliente.nome}
            Saldo:\t\tR$ {conta.saldo:.2f}
        """
        except IndexError:
            raise StopIteration
        finally:
            self._index += 1


class Cliente:
    def __init__(self,endereco):
        self.endereco = endereco
        self.contas = []
        self.indice_contas = 0


    def realizar_transacao(self, conta, transacao):
        if len(conta.historico.transacoes_do_dia()) >= 10: #limite diario de transacoes estipulado = 10
            print("--- Você excedeu o numero de transacões permitidas para hoje! ---")
            return
        
        transacao.registrar(conta)

    def adicionar_conta(self,conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self,cpf,nome,data_nascimento,endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento
        

class Conta:
    def __init__(self,numero_conta,cliente):
        self._saldo = 0
        self._numero_conta = numero_conta
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
    
    @classmethod
    def nova_conta(cls,cliente,numero_conta):
        return cls(numero_conta, cliente)
                
    @property
    def saldo(self):
        return self._saldo
    

    @property
    def numero_conta(self):
        return self._numero_conta
    

    @property
    def agencia(self):
        return self._agencia
    

    @property
    def cliente(self):
        return self._cliente
    

    @property
    def historico(self):
        return self._historico


    def sacar(self,valor):
        saldo = self.saldo
        passou_saldo = valor > saldo

        if passou_saldo:
            print("\n===Operação Falhou. Você não possui saldo suficiente!===")

        elif valor > 0:
            self._saldo -= valor
            print("---Saque realizado com sucesso!!---")
            return True
        
        else:
            print("\n===Operação Falhou. Valor informado invalido!!===")
            return False



    def depositar(self,valor):
        if valor > 0:
            self._saldo += valor
            print("+++Deposito realizado com sucesso!!+++")
            return True
        
        else:
            print("\n===Operação Falhou. Valor informado invalido!!===")
            return False
    

class Conta_Corrente(Conta):
    def __init__(self, numero_conta, cliente, limite=500,limite_saques=3):
        super().__init__(numero_conta,cliente)
        self.limite = limite
        self.limite_saques = limite_saques


    def sacar(self,valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]) # "Saque.__name__" poderia ser trocado por "Saque"
        
        passou_limite = valor > self.limite
        passou_saques = numero_saques >= self.limite_saques

        if passou_limite:
            print("\n===Operação Falhou. O valor do saque ultrapassa o limite!===")

        elif passou_saques:
            print("\n===Operação Falhou. Número de saques diarios esgotados!===")

        else:
            return super().sacar(valor) # retorna a função sacar da classe pai, assim "autorizando" o saque
        
        return False
    
    def __str__(self):
        return f'''
            Agência:\t{self.agencia}
            C/c:\t{self.numero_conta}
            Titular:\t{self.cliente.nome}
        '''


class Historico:
    def __init__(self):
        self._transacoes = []
    
    
    @property
    def transacoes(self):
        return self._transacoes


    def adicionar_transacao(self,transacao):
        #armazena os dados de transação como dicionario
        self._transacoes.append(
            {   
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d/%m/%Y - %H:%M:%S"),
            }
        )
    
    
    # Parte do decorador de logs
    def transacoes_do_dia(self):
        data_atual = datetime.now().date()
        transacoes = []
        for transacao in self._transacoes:
            data_transacao = datetime.strptime(transacao["data"], "%d/%m/%Y - %H:%M:%S").date()
            if data_atual == data_transacao:
                transacoes.append(transacao)
        return transacoes
    
    
    # parte do gerador de relatorios
    def gerar_relatorio(self, tipo_transacao=None):
        for transacao in self._transacoes:
            if tipo_transacao is None or transacao["tipo"].lower() == tipo_transacao.lower():
                yield transacao


class Transacao(ABC): # Classe abstrata
    
    @property
    @abstractmethod
    def valor(self):
        pass

    
    @classmethod
    @abstractmethod #antigo @abstractcalssmethod
    def registrar(self,conta):
        pass


class Saque(Transacao):
    def __init__(self,valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self,conta):
        sucesso_transacao = conta.sacar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self,valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self,conta):
        sucesso_transacao = conta.depositar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


############## Funções ##############

def log_transacao(func):
    def envelope(*args, **kwargs):
        resultado = func(*args, **kwargs)
        print(f"{datetime.now()}: {func.__name__.upper()}")
        return resultado

    return envelope


def menu():
    menu = """
    ================ MENU ================
    
    Escolha a opção desejada:
    [1] -> Realizar Depósito
    [2] -> Realizar Saque
    [3] -> Visualizar Extrato
    [4] -> Vizualizar Lista de contas
    [8] -> Criar nova conta corrente
    [9] -> Cadastrar-se
    [0] -> Sair
    """
    return input(menu)


def recuperar_conta_cliente(cliente):
    # Verifica se o cliente possui contas
    if not cliente.contas:
        print("\n--- Cliente não possui conta!! ---")
        return
    
    # OBS: Ainda não permite escolher a conta
    return cliente.contas[0]


def filtrar_cliente(cpf,clientes):
    # Filtra a lista de clientes procurando o cliente em questão.
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    
    # Se encontrado, retorna os dados do cliente, se não, retorna None
    return clientes_filtrados[0] if clientes_filtrados else None


@log_transacao
def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    # verifica se o cliente existe 
    if not cliente:
        print("\n---Cliente não encontrado!!---")
        return
    
    valor = float(input("Digite o valor que deseja depositar (em R$): "))
    transacao = Deposito(valor)

    # Puxa os dados da conta do usuario, se houver    #obs: futuramente, permite escolher a conta para realizar a ação 
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    # Caso todas as informações estejam corretas, conclui a ação
    cliente.realizar_transacao(conta,transacao)


@log_transacao
def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    # verifica se o cliente existe 
    if not cliente:
        print("\n---Cliente não encontrado!!---")
        return
    
    valor = float(input("Digite o valor que deseja sacar (em R$): "))
    transacao = Saque(valor)

    # Puxa os dados da conta do usuario, se houver    #obs: futuramente, permite escolher a conta para realizar a ação 
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    # Caso todas as informações estejam corretas, conclui a ação
    cliente.realizar_transacao(conta,transacao)


@log_transacao
def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    # verifica se o cliente existe 
    if not cliente:
        print("\n---Cliente não encontrado!!---")
        return
    
    # verifica se possui contas
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("------------------Meu extrato------------------")
    transacoes = conta.historico.transacoes

    extrato = ""
    tem_transacao = False
    for transacao in conta.historico.gerar_relatorio():
        tem_transacao = True
        extrato += f"\n{transacao["data"]}\n{transacao["tipo"]}:\n\tR${transacao["valor"]:.2f}\n"
    
    if not tem_transacao:
        extrato = "Sem Movimentações."
            


    print(extrato)
    print(f"\nSaldo atual:\n\tR$ {conta.saldo:.2f}")
    print("-----------------------------------------------")


@log_transacao
def criar_cliente(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n---Já existe cliente com esse CPF!!---")
        return
    
    nome = input("Digite seu nome: ")
    data_nascimento = input("Digite sua data de nascimento(DD/MM/AAAA): ")
    endereco = input('Digite seu endereço("logradouro, n° - bairro - cidade/sigla estado"): ')

    cliente = PessoaFisica(cpf=cpf, nome=nome, data_nascimento=data_nascimento, endereco=endereco)
    clientes.append(cliente)

    print("\n=== Cliente Criado com Sucesso!! ===")


@log_transacao
def criar_conta(numero_conta,clientes,contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    # verifica se o cliente existe 
    if not cliente:
        print("\n---Cliente não encontrado!!---")
        return
    
    conta = Conta_Corrente.nova_conta(cliente=cliente,numero_conta=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\nConta Criada com sucesso!")



def listar_contas(contas):
    for conta in ContasIterador(contas):
        print("="*70)
        # print(textwrap.dedent(str(conta)))
        print(str(conta))



def main():
    clientes = []
    contas = []

    while True:

        opcao_usuario = menu()
        print("\n")

        # Operação de deposito: 
        if opcao_usuario == "1":
            depositar(clientes)


        # Operação de saque
        elif opcao_usuario == "2":
            sacar(clientes)


        # Operação de extrato
        elif opcao_usuario == "3":
            exibir_extrato(clientes)


        # Vizualizar lista de Contas
        elif opcao_usuario == "4":
            listar_contas(contas)


        # Cadastro de conta corrente 
        elif opcao_usuario == "8":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)


        # Cadastro de usuário
        elif opcao_usuario == "9":
            criar_cliente(clientes)


        # Sair do sistema
        elif opcao_usuario == "0":
            break
        
        else:
            print("Operação invalida!!! Por favor selecione novamente a operação desejada")


main()
