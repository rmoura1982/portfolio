from datetime import datetime


balance = []
subtract_number = 0

def get_subtract(balance):  # Executa um saque
    atual_balance = 0
    for type, balance_item in balance:
        if type == "S":
            atual_balance -= balance_item
        elif type == "A":
            atual_balance += balance_item
    if atual_balance <= 0:
        print("SALDO INSUFICIENTE!\n")
        return None
    else:
        print(f"SALDO: R$ {atual_balance:.2f}")
        try:
            subtract = float(input("DIGITE O VALOR DO SAQUE: ").strip())
            if subtract <= 0:
                print("DIGITE UM VALOR MAIOR QUE ZERO!\n")
                return None
            if subtract > atual_balance:
                print("SALDO INSUFICIENTE!\n")
                return None
            if subtract > 500:
                print("LIMITE DE R$ 500,00 POR SAQUE!\n")
                return None
            print(f"SAQUE: R$ {subtract:.2f}\n")
            balance.append(("S", subtract))
            return subtract
        except ValueError:
            print("ENTRADA INVÁLIDA! DIGITE UM NÚMERO VÁLIDO.\n")
            return None

def get_addition(balance):  # Executa um depósito
    while True:
        try:
            addition = float(input("DIGITE O VALOR DO DEPÓSITO: ").strip())
            if addition > 0:
                print(f"DEPÓSITO: R$ {addition:.2f}\n")
                balance.append(("A", addition))
                return addition
            else:
                print("DIGITE UM VALOR MAIOR QUE ZERO!\n")
        except ValueError:
            print("ENTRADA INVÁLIDA! DIGITE UM NÚMERO VÁLIDO.\n")

def get_extract(balance):  # Exibe o extrato
    DATE = "DATA"
    TIME = f"{' ' * 9}HORA"
    BALANCE = f"{' ' * 7}MOVIMENTAÇÃO"
    print(f"{DATE}{TIME}{BALANCE}")
    now = datetime.now().strftime("%Y-%m-%d   %H:%M:%S")
    atual_balance = 0
    for item in balance:
        try:
            type, balance_item = item
            if type == "S":
                moviment = "-"
                moviment_type = "(S)"
                atual_balance -= float(balance_item)
            elif type == "A":
                moviment = "+"
                moviment_type = "(D)"
                atual_balance += float(balance_item)
            else:
                continue  # ignora tipos desconhecidos
            print(f"{now}{' ' * 2} {moviment}R$ {atual_balance:.2f} {moviment_type}")
        except (ValueError, TypeError):
            print("ERRO AO PROCESSAR UMA MOVIMENTAÇÃO. VERIFIQUE OS DADOS.\n")
            continue
    print(f"\nSALDO {'#' * 17} R$ {atual_balance:.2f}\n")
 