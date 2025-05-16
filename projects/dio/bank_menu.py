menu = ["[0] - SAIR", "[1] - SAQUE", "[2] - DEPÓSITO", "[3] - EXTRATO"]

def get_menu(text): # Executa a interação com o menu
    operation = input(f"{text}").strip()
    if operation in ["0", "1", "2", "3"]:
        operation = int(operation)
        return operation
    else:
        print(f"'{operation.upper()}' é uma opção INVÁLIDA!")