def validar_dados_cadastro(dados):
    erros = []

    if not dados["tipo_conta"]:
        erros.append("Selecione um tipo de conta.")

    if not dados["nome"].strip():
        erros.append("Preencha o nome.")

    if not dados["cpf"].isdigit() or len(dados["cpf"]) != 11:
        erros.append("CPF inválido.")

    if not dados["telefone"].isdigit() or len(dados["telefone"]) < 10:
        erros.append("Telefone inválido.")

    if not dados["data_nascimento"] or len(dados["data_nascimento"]) != 10:
        erros.append("Data de nascimento inválida.")

    cep = numero = ""
    if "," not in dados["endereco"]:
        erros.append("Endereço deve conter CEP e número separados por vírgula.")
    else:
        endereco_split = dados["endereco"].split(",")
        cep = endereco_split[0].strip()
        numero = endereco_split[1].strip()

    if "@" not in dados["email"] or "." not in dados["email"]:
        erros.append("Email inválido.")

    if len(dados["senha"]) < 9:
        erros.append("Senha muito curta.")

    return erros, cep, numero

# app/validadores.py

def validar_dados_pagamento(dados):
    erros = []

    cpf = dados.get("cpf_destino", "").strip()
    valor_str = dados.get("valor", "").strip()
    conta_origem = dados.get("conta_origem")

    if not cpf.isdigit() or len(cpf) != 11:
        erros.append("CPF inválido.")

    try:
        valor = float(valor_str)
        if valor <= 0:
            erros.append("Valor deve ser positivo.")
    except ValueError:
        erros.append("Valor inválido.")

    if not conta_origem or not conta_origem.ativa:
        erros.append("Conta de origem inválida.")

    return erros
