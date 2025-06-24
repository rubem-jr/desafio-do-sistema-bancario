# Desafio Dio - Santander BootCamp 2025
# Criar um Sistema Bancario
#
# 
# v2:
#   Novas Funcionalidades:
#       - criar usuario:
#           Deve armazenar os usuarios em uma lista
#           Composto por:
#               nome, data_de_nascimento, cpf, endereço
#               o endereço é uma str com o formato: "logradouro, n° - bairro - cidade/sigla estado".
#               Deve ser armazenado somente os numeros do CPF
#               Não podemos ter CPF repetido
# 
# 
#       - criar conta
#           Deve armazenar as contas em uma lista
#           Composto por:
#               agência, numero da conta, usuário
#               o numero da agencia(ag) é fixo:"0001"
#               o numero da conta é sequencial iniciando em 1
#               o usuario pode ter mais de uma conta, porem uma conta só pode ter 1 usuario
# 
# 
# 
#   obs: para conferir versões anteriores, consultar o perfil no GitHub
# 
# 
# 
# Informações:
# Realizado por: Rubem Junior
# Usuario GitHub: rubem-jr
# Usuario Dio: juniorrubem50



def criar_usuario(): # #9
    nome = input("Digite seu nome: ")
    data_nascimento = input("Digite sua data de nascimento(DD/MM/AAAA): ")
    cpf = input("Digite seu CPF (somente numeros): ")
    endereco = input('Digite seu endereço("logradouro, n° - bairro - cidade/sigla estado"): ')
    novo_usuario = {"nome": nome, "data_nascimento":data_nascimento, "cpf":cpf, "endereco":endereco, "contas":[]}
    print("\nConta Criada com sucesso!")
    return novo_usuario


def criar_conta_corrente(lista_usuarios, lista_contas):# #8
    # Modelo Padrão de conta
    conta_corrente = {"agencia": "0001", "conta" : 0, "usuario" : "", "cpf": ""}

    procurar_cpf = input("Digite seu CPF para vincular a nova conta: ")
    for cliente in lista_usuarios:
        if cliente["cpf"] == procurar_cpf:
            # Pega as informações do cliente e vincula ele direto a conta
            conta_corrente["conta"] = len(cliente["contas"]) + 1
            conta_corrente["usuario"] = cliente["nome"]
            conta_corrente["cpf"] = cliente["cpf"]
            cliente["contas"].append(conta_corrente) # Cliente está dentro da lista de usuario

            #Guarda a conta em uma outra lista separada para atualizações futuras
            lista_contas.append(conta_corrente)
            print("\nConta Criada com sucesso!")
            return lista_usuarios, lista_contas
        
        else:
            print("Não foi possivel criar a conta, tente novamente!")
            return lista_usuarios, lista_contas
        
    
def deposito_usuario(saldo, extrato, contador_depositos):# #1
    valor = float(input("Digite o valor que deseja depositar (em R$): "))
    if valor > 0:
        saldo += valor
        extrato = extrato + f"✅ {contador_depositos}° Depósito: +R$ {valor:.2f}\n"
        contador_depositos += 1
        print("\nDepósito realizado com sucesso!")
        return saldo, extrato, contador_depositos
        
    else:
        print("Valor invalido! Tente novamente!")
        return saldo, extrato, contador_depositos


def saque_usuario(*,saldo,numero_saques,limite,extrato,LIMITE_SAQUE):# #2
    if numero_saques <= LIMITE_SAQUE:
        valor = float(input("Digite o valor que deseja sacar (em R$): "))
        if valor > 0:
            if valor <= limite:
                if valor <= saldo:
                    saldo -= valor
                    extrato = extrato + f"❌ {numero_saques}° Saque: -R$ {valor:.2f}\n"
                    numero_saques += 1
                    print("\nSaque realizado com sucesso!")
                    return saldo, extrato, numero_saques
                else:
                    print("Saldo insuficiente!")
                    return saldo, extrato, numero_saques
                    
            else:
                print("Seu limite de saque é de R$ 500, tente novamente!")
                return saldo, extrato, numero_saques
        else:
            print("Valor invalido! Tente novamente!")
            return saldo, extrato, numero_saques
    else:
        print("Operação Invalida! Você atingiu o limite de operações de saques do dia!")
        return saldo, extrato, numero_saques


def extrato_usuario(saldo,/,*,extrato):# #3
        print("------------------Meu extrato------------------")
        print(extrato)
        print("-----------------------------------------------")
        print(f"Saldo atual: {saldo:.2f}")
        # obs:
        #     "*" -> utilizado para dizer que os argumentos são keywords-only (ex: limite=500)
        #     "*" -> utilizado para dizer que os argumentos são positional-only (padrão)


def listar_contas(lista_contas):# #5
    print("=" * 50 )
    print(" "*22 + "CONTAS" + " "*22)
    for conta in lista_contas:
        print("=" * 50)
        print(f'''
            Agencia:\t{conta["agencia"]} 
            C/c:\t{conta["conta"]} 
            Titular:\t{conta["usuario"]} 
            ''')
        

def listar_usuarios(lista_usuarios):# #4:
    print("=" * 50 )
    print(" "*21 + "USUARIOS" + " "*21)
    for usuarios in lista_usuarios:
        print("=" * 50)
        print(f'''
            Nome:                  {usuarios["nome"]} 
            CPF:                   {usuarios["cpf"]}
            Data de Nascimento:    {usuarios["data_nascimento"]} 
            Endereço:              {usuarios["endereco"]}
            Contas:                {usuarios["contas"] if usuarios["contas"] else "N/A"} 
            ''')
        # if usuarios["contas"]:
        #     print(f"Contas:                {usuarios["contas"]}")


def main():
    
    menu = """
    ================ MENU ================
    
    Escolha a opção desejada:
    [1] -> Realizar Depósito
    [2] -> Realizar Saque
    [3] -> Visualizar Extrato
    [4] -> Vizualizar Lista de usuarios
    [5] -> Vizualizar Lista de contas
    [8] -> Criar nova conta corrente
    [9] -> Cadastrar-se
    [0] -> Sair

    """

    # Variaveis Globais:
    saldo = float(0)
    limite = float(500)
    numero_saques = int(1)
    LIMITE_SAQUE = int(3)
    extrato = ""
    contador_depositos = 1
    lista_usuarios = []
    lista_contas = []


    # Inicio do programa
    while True:

        opcao_usuario = input(menu)
        print("\n")


        # Operação de deposito: 
        if opcao_usuario == "1":
            saldo, extrato, contador_depositos = deposito_usuario(saldo, extrato, contador_depositos)


        # Operação de saque
        elif opcao_usuario == "2":
            saldo, extrato, numero_saques = saque_usuario(saldo=saldo,numero_saques=numero_saques,limite=limite,extrato=extrato,LIMITE_SAQUE=LIMITE_SAQUE)


        # Operação de extrato
        elif opcao_usuario == "3":
            extrato_usuario(saldo,extrato=extrato)


        # Vizualizar lista de usuarios
        elif opcao_usuario == "4":
            listar_usuarios(lista_usuarios)


        # Vizualizar lista de Contas
        elif opcao_usuario == "5":
            listar_contas(lista_contas)


        # Cadastro de conta corrente 
        elif opcao_usuario == "8":
            lista_usuarios,lista_contas = criar_conta_corrente(lista_usuarios,lista_contas)


        # Cadastro de usuário
        elif opcao_usuario == "9":
            lista_usuarios.append(criar_usuario())


        # Sair do sistema
        elif opcao_usuario == "0":
            print(f"Até a proxima!\nSeu saldo final é de R$ {saldo:.2f}")
            break
        
        else:
            print("Operação invalida!!! Por favor selecione novamente a operação desejada")



# Chamada final.
main()




    
