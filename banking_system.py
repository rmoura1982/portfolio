from datetime import datetime


balance = []
subtract_number = 0
menu = ["[0] - SAIR", "[1] - SAQUE", "[2] - DEPÓSITO", "[3] - EXTRATO"]

def get_menu(text): # Executa a interação com o menu
    operation = input(f"{text}").strip()
    if operation in ["0", "1", "2", "3"]:
        operation = int(operation)
        return operation
    else:
        print(f"'{operation.upper()}' é uma opção INVÁLIDA!")

def get_subtract(): # Executa um saque
    atual_balance = 0
    for type, balance_item in balance:
        if type == "S":
            atual_balance -= balance_item
        elif type == "A":
            atual_balance += balance_item
    if atual_balance <= 0:
        print(f"SALDO INSULFICIENTE!\n")
        return None
    else:
        print(f"SALDO: R$ {atual_balance:.2f}")
        subtract = float(input("DIGITE O VALOR DO SAQUE: ").strip())
        if subtract > atual_balance:
            print(f"SALDO INSULFICIENTE!\n")
        if subtract > 500:
            print(f"LIMITE DE R$ 500,00 POR SAQUE!\n")
            return None
        else:
            print(f"SAQUE: R$ {subtract:.2f}\n")
            balance.append(("S", subtract))
            return subtract

def get_addition(): # Executa um depósito
    addition = float(input("DIGITE O VALOR DO DEPÓSITO: ").strip())
    print(f"DEPÓSITO: R$ {addition:.2f}\n")
    balance.append(("A", addition))
    return addition

def get_extract(balance): # Exibe o extrato
    DATE = "DATA"
    TIME = f"{' ' * 9}HORA"
    BALANCE = f"{' ' * 7}MOVIMENTAÇÃO"
    print(f"{DATE}{TIME}{BALANCE}")
    now = datetime.now().strftime("%Y-%m-%d   %H:%M:%S")
    atual_balance = 0
    for type, balance_item in balance:
        if type == "S":
            moviment = "-"
            moviment_type = "(S)"
            atual_balance -= balance_item
        elif type == "A":
            moviment = "+"
            moviment_type = "(D)"
            atual_balance += balance_item
        print(f"{now}{' ' * 2} {moviment}R$ {atual_balance:.2f} {moviment_type}")
    print(f"\nSALDO {'#' * 17} R$ {atual_balance:.2f}\n")
    
print("BEM VINDO AO BANCO DIO!\n")
while True:
    for item_menu in menu:
        print(item_menu)
    operation = get_menu("ESCOLHA UMA OPÇÃO: ")
    print()

    if operation == 1:
        if subtract_number >= 3:
            print("VOCÊ ATINGIU O LIMITE DIÁRIO DE SAQUE. MUITO OBRIGADO!")
            break
        else:
            subtract = get_subtract()
            if subtract == None:
                pass
            else:
                subtract_number += 1
        
    elif operation == 2:
        addition = get_addition()

    elif operation == 3:
        get_extract(balance)

    elif operation == 0:
        print("MUITO OBRIGADO!")
        break
