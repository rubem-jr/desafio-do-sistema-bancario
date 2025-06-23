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
# Informações:
# Realizado por: Rubem Junior
# Usuario: juniorrubem50

menu = """

    Escolha a opção desejada:
    [1] -> Realizar Depósito
    [2] -> Realizar Saque
    [3] -> Visualizar Extrato
    [0] -> Sair

"""

# Variaveis:
saldo = 0
limite = 500
numero_saques = 1
LIMITE_SAQUE = 3
extrato = ""
# Extras descartaveis
contador_depositos = 1
while True:

    opcao_usuario = input(menu)
    print("\n")
    deposito = 0
    
    # Operação de deposito: 
    if opcao_usuario == "1":
        deposito = float(input("Digite o valor que deseja depositar (em R$): "))
        if deposito > 0:
            saldo += deposito
            extrato = extrato + f"✅ {contador_depositos}° Depósito: +R$ {deposito:.2f}\n"
            contador_depositos += 1
            print("\nDeposito realizado com sucesso!")
        else:
            print("Valor invalido! Tente novamente!")
    
    # Operação de saque
    elif opcao_usuario == "2":
        if numero_saques <= LIMITE_SAQUE:
            saque = float(input("Digite o valor que deseja sacar (em R$): "))
            if saque > 0:   
                if saque <= limite:
                    if saque <= saldo:
                        saldo -= saque
                        extrato = extrato + f"❌ {numero_saques}° Saque: +R$ {saque:.2f}\n"
                        numero_saques += 1
                        print("\nSaque realizado com sucesso!")
                    else:
                        print("Saldo insuficiente!")
                else:
                    print("Seu limite de saque é de R$ 500, tente novamente!")
            else:
                print("Valor invalido! Tente novamente!")
        else:
            print("Operação Invalida! Você atingiu o limite de operações de saques do dia!")


    
    # Operação de extrato
    elif opcao_usuario == "3":
        print("------------------Meu extrato------------------")
        print(extrato)
        print("-----------------------------------------------")
        print(f"Saldo atual: {saldo:.2f}")

    # Sair do sistema
    elif opcao_usuario == "0":
        print(f"Até a proxima!\nSeu saldo final é de R$ {saldo:.2f}")
        break
    
    else:
        print("Operação invalida!!! Por favor selecione novamente a operação desejada")

    