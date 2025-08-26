def encontrar_usuario(cpf):
    for usuario in usuarios:
        if usuario['cpf'] == cpf:
            return usuario
    return None

def criar_usuario():
    cpf = input("CPF (formato xxx.xxx.xxx-xx): ")
    if not validar_cpf(cpf):
        print("[ALERTA] CPF inválido! Use o formato xxx.xxx.xxx-xx.")
        return
    if encontrar_usuario(cpf):
        print("Usuário já cadastrado!")
        return
    nome = input("Nome completo: ")
    nascimento = input("Data de nascimento (dd/mm/aaaa): ")
    if not validar_data(nascimento):
        print("[ALERTA] Data inválida! Use o formato dd/mm/aaaa.")
        return
    endereco = input("Endereço (logradouro, nro - bairro - cidade/UF): ")
    if not validar_endereco(endereco):
        print("[ALERTA] Endereço inválido! Use o formato correto.")
        return
    usuarios.append({"cpf": cpf, "nome": nome, "nascimento": nascimento, "endereco": endereco})
    print("Usuário cadastrado com sucesso!")

def criar_conta():
    cpf = input("CPF do titular: ")
    usuario = encontrar_usuario(cpf)
    if not usuario:
        print("Usuário não encontrado!")
        return
    numero = len(contas) + 1
    contas.append({"agencia": "0001", "numero": numero, "usuario": usuario})
    transacoes[numero] = {"saldo": 0, "extrato": [], "saques": 0}
    print(f"Conta {numero} criada para {usuario['nome']}.")


# Sistema Bancário Avançado
import re

def validar_cpf(cpf):
    return bool(re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', cpf))

def validar_data(data):
    import datetime
    if not re.match(r'^\d{2}/\d{2}/\d{4}$', data):
        return False
    dia, mes, ano = map(int, data.split('/'))
    try:
        datetime.datetime(ano, mes, dia)
        return True
    except ValueError:
        return False

def validar_endereco(endereco):
    return bool(re.match(r'^.+,\s*\d+\s*-\s*.+\s*-\s*.+/.{2}$', endereco))

menu = """
[u] Novo Usuário
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """


usuarios = []
contas = []
transacoes = {}
LIMITE_SAQUES = 3
LIMITE_VALOR_SAQUE = 500


def depositar():
    numero_str = input("Número da conta: ")
    if not numero_str.isdigit():
        print("Número da conta inválido! Digite apenas números.")
        return
    numero = int(numero_str)
    valor_str = input("Valor do depósito: ").replace(',', '.')
    try:
        valor = float(valor_str)
    except ValueError:
        print("Valor inválido! Use apenas números.")
        return
    if valor <= 0:
        print("Valor inválido!")
        return
    if numero not in transacoes:
        print("Conta não encontrada!")
        return
    transacoes[numero]["saldo"] += valor
    transacoes[numero]["extrato"].append(f"Depósito: R$ {valor:.2f}")
    print("Depósito realizado!")

def sacar():
    numero_str = input("Número da conta: ")
    if not numero_str.isdigit():
        print("Número da conta inválido! Digite apenas números.")
        return
    numero = int(numero_str)
    valor_str = input("Valor do saque: ").replace(',', '.')
    try:
        valor = float(valor_str)
    except ValueError:
        print("Valor inválido! Use apenas números.")
        return
    if numero not in transacoes:
        print("Conta não encontrada!")
        return
    saldo = transacoes[numero]["saldo"]
    saques = transacoes[numero]["saques"]
    if valor > saldo:
        print("Saldo insuficiente!")
    elif valor > LIMITE_VALOR_SAQUE:
        print("Valor excede o limite por saque!")
    elif saques >= LIMITE_SAQUES:
        print("Limite de saques diários atingido!")
    elif valor <= 0:
        print("Valor inválido!")
    else:
        transacoes[numero]["saldo"] -= valor
        transacoes[numero]["extrato"].append(f"Saque: R$ {valor:.2f}")
        transacoes[numero]["saques"] += 1
        print("Saque realizado!")

def extrato():
    numero_str = input("Número da conta: ")
    if not numero_str.isdigit():
        print("Número da conta inválido! Digite apenas números.")
        return
    numero = int(numero_str)
    if numero not in transacoes:
        print("Conta não encontrada!")
        return
    print("\n===== EXTRATO =====")
    if not transacoes[numero]["extrato"]:
        print("Não foram realizadas movimentações.")
    else:
        for mov in transacoes[numero]["extrato"]:
            print(mov)
    print(f"Saldo: R$ {transacoes[numero]['saldo']:.2f}")
    print("===================\n")

def listar_contas():
    print("\n--- CONTAS CADASTRADAS ---")
    for conta in contas:
        print(f"Agência: {conta['agencia']} | Conta: {conta['numero']} | Titular: {conta['usuario']['nome']} | CPF: {conta['usuario']['cpf']}")
    print("--------------------------\n")

def menu_principal():
    print("""
    [u] Usuário
    [c] Contas
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [l] Listar Contas
    [q] Sair
    """)
    return input("=> ").lower()

def main():
    while True:
        opcao = menu_principal()
        if opcao == "u":
            criar_usuario()
        elif opcao == "c":
            criar_conta()
        elif opcao == "d":
            depositar()
        elif opcao == "s":
            sacar()
        elif opcao == "e":
            extrato()
        elif opcao == "l":
            listar_contas()
        elif opcao == "q":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()

