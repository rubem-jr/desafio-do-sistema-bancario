# Desafio Dio - Santander BootCamp 2025
# Criar um sistema bancario
# v1:
#   O sistema deve conter as operações de Deposito, saque e extrato
#   
#   Deposito -> deve armazenar todas as informações.
#   
#   Saque -> limite de 3 saques diarios e valor limite de R$ 500, se passar do valor ou limite diario ou saldo da conta a baixo, alertar ao usuario.
# 
#   Extrato -> deve listar todas as operações realizadas e ao final exibir o valor da conta 
# 
# v1.2: 
#   Criar funções para as funcionalidades ja existentes (depositar, sacar e visualizar extrato), e criar as funções de Usuário(cliente do banco) 
#   e criar conta corrente(vincular com usuário)
#   
#   saque -> receber argumentos apenas por nome (ex: limite=500)
#   
#   deposito -> receber argumentos apenas por posição (padrão)
#   
#   extrato -> receber argumentos por posição e nome, saldo(posicional) e extrato(nomeado)
# 
# ...
# 
# Informações:
# Realizado por: Rubem Junior
# Usuario GitHub: rubem-jr
# Usuario Dio: juniorrubem50

menu = """

    Escolha a opção desejada:
    [1] -> Realizar Depósito
    [2] -> Realizar Saque
    [3] -> Visualizar Extrato
    [0] -> Sair

"""

# Variaveis Globais:
saldo = 0
limite = 500
numero_saques = 1
LIMITE_SAQUE = 3
extrato = ""
contador_depositos = 1


def deposito_usuario(saldo, extrato, contador_depositos):
    valor = float(input("Digite o valor que deseja depositar (em R$): "))
    if valor > 0:
        saldo += valor
        extrato = extrato + f"✅ {contador_depositos}° Depósito: +R$ {valor:.2f}\n"
        contador_depositos += 1
        return saldo, extrato, contador_depositos
        
    else:
        print("Valor invalido! Tente novamente!")
    
    #     print("\nDeposito realizado com sucesso!")
    # else:
    #     print("Valor invalido! Tente novamente!")


def saque_usuario(*,saldo,numero_saques,limite,extrato,LIMITE_SAQUE):
    if numero_saques <= LIMITE_SAQUE:
        valor = float(input("Digite o valor que deseja sacar (em R$): "))
        if valor > 0:   
            if valor <= limite:
                if valor <= saldo:
                    saldo -= valor
                    extrato = extrato + f"❌ {numero_saques}° Saque: +R$ {valor:.2f}\n"
                    numero_saques += 1
                    return saldo, extrato, numero_saques
                    # print("\nSaque realizado com sucesso!")
                else:
                    print("Saldo insuficiente!")
            else:
                print("Seu limite de saque é de R$ 500, tente novamente!")
        else:
            print("Valor invalido! Tente novamente!")
    else:
        print("Operação Invalida! Você atingiu o limite de operações de saques do dia!")


def extrato_usuario(saldo,/,*,extrato):
        print("------------------Meu extrato------------------")
        print(extrato)
        print("-----------------------------------------------")
        print(f"Saldo atual: {saldo:.2f}")
        # obs:
        #     "*" -> utilizado para dizer que os argumentos são keywords-only (ex: limite=500)
        #     "*" -> utilizado para dizer que os argumentos são positional-only (padrão)
while True:

    opcao_usuario = input(menu)
    print("\n")


    # Operação de deposito: 
    if opcao_usuario == "1":
        saldo, extrato, contador_depositos = deposito_usuario(saldo, extrato, contador_depositos)
        print("\nDeposito realizado com sucesso!")
    # Operação de saque
    elif opcao_usuario == "2":
        saldo, extrato, numero_saques = saque_usuario(saldo=saldo,numero_saques=numero_saques,limite=500,extrato=extrato,LIMITE_SAQUE=LIMITE_SAQUE)
        print("\nSaque realizado com sucesso!")

    # Operação de extrato
    elif opcao_usuario == "3":
        extrato_usuario(saldo,extrato=extrato)

    # Sair do sistema
    elif opcao_usuario == "0":
        print(f"Até a proxima!\nSeu saldo final é de R$ {saldo:.2f}")
        break
    
    else:
        print("Operação invalida!!! Por favor selecione novamente a operação desejada")

    
