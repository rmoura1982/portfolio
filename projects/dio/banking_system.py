from bank_menu import get_menu, menu
from transactions import get_subtract, get_addition, get_extract, balance, subtract_number


print("BEM VINDO AO BANCO DIO!\n")
operations = []
operation_number = 0

while True:
    if operation_number >= 11:
        print("VOCÊ EXCEDEU O LIMITE MÁXIMO DE 10 OPERAÇÕES!\n")
        break

    for item_menu in menu:
        print(item_menu)
    operation = get_menu("ESCOLHA UMA OPÇÃO: ")
    print()

    if operation == 1:
        if subtract_number >= 3:
            print("VOCÊ ATINGIU O LIMITE DIÁRIO DE SAQUE. MUITO OBRIGADO!\n")
            continue  # volta ao menu principal
        subtract = get_subtract(balance)
        if subtract is not None:
            subtract_number += 1
            operations.append(("S", subtract))
            operation_number += 1

    elif operation == 2:
        addition = get_addition(balance)
        operations.append(("D", addition))
        operation_number += 1

    elif operation == 3:
        get_extract(balance)

    elif operation == 0:
        print("MUITO OBRIGADO!")
        break

