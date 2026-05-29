
pedidos = {}
entregadores = {}


def menu_principal():

    while True:

        print("""

 ==================SISTEMA PRINCIPAL====================


1 - Cadastrar Pedido
2 - Cadastrar Entregador
3 - Operações
4 - Consultas
5 - Relatórios
0 - Finalizar Sistema
""")

        opcao = input("Escolha uma opção: ")

        match opcao:

            case "1":
                cadastrar_pedido()

            case "2":
                cadastrar_entregador()

            case "3":
                menu_operacoes()

            case "4":
                menu_consultas()

            case "5":
                relatorios()

            case "0":
                print("\nSistema encerrado.")
                break

            case _:
                print("Opção inválida.")

def menu_operacoes():
    check=0
    while check == 0:

        print("""
============= OPERAÇÕES =============

1 - Associar Pedido ao Entregador
2 - Remover Associação
3 - Atualizar Pedido
0 - Voltar
""")

        op = input("Escolha: ")

        match op:

            case "1":
                associar()

            case "2":
                remover_associacao()

            case "3":
                atualizar()

            case "0":
                check = 1

            case _:
                print("Opção inválida.")


def menu_consultas():
    check = 0

    while check == 0:

        print("""
================ CONSULTAS ================

1 - Pedidos Pendentes
2 - Pedidos Entregues
3 - Buscar Pedido por ID
4 - Entregadores Disponíveis
5 - Entregas por Entregador
0 - Voltar
""")

        op = input("Escolha: ")

        match op:

            case "1":
                pedidos_pendentes()

            case "2":
                pedidos_entregues()

            case "3":
                buscar()

            case "4":
                entregadores_disponiveis()

            case "5":
                entregas_por_entregador()

            case "0":
                check = 1

            case _:
                print("Opção inválida.")


def validar_id_pedido(id_pedido):

    return (
        len(id_pedido) == 5 and
        id_pedido[0].isalpha() and
        id_pedido[1:].isdigit()
    )


def validar_id_entregador(id_ent):

    return (
        len(id_ent) == 4 and
        id_ent.isdigit()
    )


def capacidade_maxima(veiculo):

    match veiculo:

        case "moto":
            return 1

        case "carro":
            return 2

        case "van":
            return 3

        case _:
            return 0


def cadastrar_pedido():

    print("\n=========== CADASTRO DE PEDIDO ===========")

    id_pedido = input("ID do pedido: ").upper()

    if not validar_id_pedido(id_pedido):
        print("ID inválido.")
        return

    if id_pedido in pedidos:
        print("Pedido já cadastrado.")
        return

    cliente = input("Nome do cliente: ")

    endereco = input("Endereço: ")

    prioridade = input("Prioridade (Alta/Normal): ").capitalize()

    if prioridade != "Alta" and prioridade != "Normal":
        print("Prioridade inválida.")
        return

    descricao = input("Descrição do pedido: ")

    pedidos[id_pedido] = {
        "cliente": cliente,
        "endereco": endereco,
        "prioridade": prioridade,
        "descricao": descricao,
        "status": "Pendente",
        "entregador": None,
    }

    print("Pedido cadastrado com sucesso.")


def cadastrar_entregador():

    print("\n========= CADASTRO DE ENTREGADOR =========")

    id_ent = input("ID do entregador: ")

    if not validar_id_entregador(id_ent):
        print("ID inválido.")
        return

    if id_ent in entregadores:
        print("Entregador já cadastrado.")
        return

    nome = input("Nome do entregador: ")

    veiculo = input("Veículo (moto/carro/van): ").lower()

    match veiculo:

        case "moto" | "carro" | "van":

            entregadores[id_ent] = {
                "nome": nome,
                "veiculo": veiculo,
                "pedidos": [],
                "disponivel": True
            }

            print("Entregador cadastrado com sucesso.")

        case _:
            print("Veículo inválido.")


def associar():

    print("\n=========== ASSOCIAR PEDIDO ===========")

    id_pedido = input("ID do pedido: ").upper()

    id_ent = input("ID do entregador: ")

    if id_pedido not in pedidos:
        print("Pedido não encontrado.")
        return

    if id_ent not in entregadores:
        print("Entregador não encontrado.")
        return

    pedido = pedidos[id_pedido]

    entregador = entregadores[id_ent]

    if pedido["entregador"] is not None:
        print("Pedido já possui entregador.")
        return

    limite = capacidade_maxima(entregador["veiculo"])

    if len(entregador["pedidos"]) >= limite:
        print("Capacidade máxima atingida.")
        return

    pedido["entregador"] = id_ent

    pedido["status"] = "Em Rota"

    entregador["pedidos"].append(id_pedido)

    if len(entregador["pedidos"]) >= limite:
        entregador["disponivel"] = False

    print("Pedido associado com sucesso.")


def remover_associacao():

    print("\n========== REMOVER ASSOCIAÇÃO ==========")

    id_pedido = input("ID do pedido: ").upper()

    if id_pedido not in pedidos:
        print("Pedido não encontrado.")
        return

    pedido = pedidos[id_pedido]

    if pedido["entregador"] is None:
        print("Pedido não possui entregador.")
        return

    id_ent = pedido["entregador"]

    entregador = entregadores[id_ent]

    entregador["pedidos"].remove(id_pedido)

    entregador["disponivel"] = True

    pedido["entregador"] = None

    pedido["status"] = "Pendente"

    print("Associação removida.")


def atualizar():

    print("\n=========== ATUALIZAR PEDIDO ===========")

    id_pedido = input("ID do pedido: ").upper()

    if id_pedido not in pedidos:
        print("Pedido não encontrado.")
        return

    pedido = pedidos[id_pedido]

    print("""
1 - Alterar status
2 - Cancelar pedido
""")

    opcao = input("Escolha: ")

    match opcao:

        case "1":

            print("""
1 - Pendente
2 - Em Rota
3 - Entregue
""")

            status = input("Escolha: ")

            match status:

                case "1":
                    pedido["status"] = "Pendente"

                case "2":
                    pedido["status"] = "Em Rota"

                case "3":

                    pedido["status"] = "Entregue"

                    if pedido["entregador"] is not None:

                        entregador = entregadores[pedido["entregador"]]

                        if id_pedido in entregador["pedidos"]:
                            entregador["pedidos"].remove(id_pedido)

                        entregador["disponivel"] = True

                case _:
                    print("Opção inválida.")
                    return

            print("Status atualizado.")

        case "2":

            if pedido["entregador"] is not None :

                entregador = entregadores[pedido["entregador"]]

                if id_pedido in entregador["pedidos"]:
                    entregador["pedidos"].remove(id_pedido)

                entregador["disponivel"] = True

            del pedidos[id_pedido]

            print("Pedido cancelado e removido do sistema.")

        case _:
            print("Opção inválida.")


def mostrar(id_pedido, pedido):

    print("\n--------------------------------")

    print("ID:", id_pedido)
    print("Cliente:", pedido["cliente"])
    print("Endereço:", pedido["endereco"])
    print("Prioridade:", pedido["prioridade"])
    print("Descrição:", pedido["descricao"])
    print("Status:", pedido["status"])
    print("Entregador:", pedido["entregador"])

    print("--------------------------------")


def pedidos_pendentes():

    print("\n========== PEDIDOS PENDENTES ==========")

    encontrou = False

    for id_pedido in pedidos:

        pedido = pedidos[id_pedido]

        if pedido["status"] == "Pendente":

            mostrar(id_pedido, pedido)

            encontrou = True

    if not encontrou:
        print("Nenhum pedido pendente.")


def pedidos_entregues():

    print("\n========== PEDIDOS ENTREGUES ==========")

    encontrou = False

    for id_pedido in pedidos:

        pedido = pedidos[id_pedido]

        if pedido["status"] == "Entregue":

            mostrar(id_pedido, pedido)

            encontrou = True

    if not encontrou:
        print("Nenhum pedido entregue.")


def buscar():

    print("\n============ BUSCAR PEDIDO ============")

    id_pedido = input("Digite o ID: ").upper()

    if id_pedido in pedidos:
        mostrar(id_pedido, pedidos[id_pedido])

    else:
        print("Pedido não encontrado.")


def entregadores_disponiveis():

    print("\n====== ENTREGADORES DISPONÍVEIS ======")

    encontrou = False

    for id_ent in entregadores:

        ent = entregadores[id_ent]

        if ent["disponivel"]:

            print("\n--------------------------------")
            print("ID:", id_ent)
            print("Nome:", ent["nome"])
            print("Veículo:", ent["veiculo"])
            print("Pedidos:", ent["pedidos"])
            print("--------------------------------")

            encontrou = True

    if not encontrou:
        print("Nenhum entregador disponível.")


def entregas_por_entregador():

    print("\n====== ENTREGAS POR ENTREGADOR ======")

    id_ent = input("ID do entregador: ")

    encontrou = False

    for id_pedido in pedidos:

        pedido = pedidos[id_pedido]

        if (
            pedido["entregador"] == id_ent and
            pedido["status"] == "Entregue"
        ):

            mostrar(id_pedido, pedido)

            encontrou = True

    if not encontrou:
        print("Nenhuma entrega encontrada.")


def relatorios():

    print("\n============= RELATÓRIOS =============")

    total = len(pedidos)

    pendente = 0
    rota = 0
    entregue = 0

    for id_pedido in pedidos:

        pedido = pedidos[id_pedido]

        match pedido["status"]:

            case "Pendente":
                pendente += 1

            case "Em Rota":
                rota += 1

            case "Entregue":
                entregue += 1


    print("\nTotal de pedidos:", total)

    print("\nQuantidade por status:")
    print("Pendente:", pendente)
    print("Em rota:", rota)
    print("Entregue:", entregue)

    print("\n====== PEDIDOS PRIORIDADE ALTA ======")

    encontrou = False

    for id_pedido in pedidos:

        pedido = pedidos[id_pedido]

        if pedido["prioridade"] == "Alta":

            print(id_pedido, "-", pedido["cliente"])

            encontrou = True

    if not encontrou:
        print("Nenhum pedido prioritário.")

    maior = 0
    melhor_entregador = None

    for id_ent in entregadores:

        qtd = 0

        for id_pedido in pedidos:

            pedido = pedidos[id_pedido]

            if (
                pedido["entregador"] == id_ent and
                pedido["status"] == "Entregue"
            ):
                qtd += 1

        if qtd > maior:
            maior = qtd
            melhor_entregador = id_ent

    print("\n=== ENTREGADOR COM MAIS ENTREGAS ===")

    if melhor_entregador is not None:

        ent = entregadores[melhor_entregador]

        print("Nome:", ent["nome"])
        print("ID:", melhor_entregador)
        print("Quantidade:", maior)

    else:
        print("Nenhuma entrega realizada.")


menu_principal()
