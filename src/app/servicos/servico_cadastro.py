class ServicoCadastro:
    def __init__(self, banco):
        """
        Serviço responsável por realizar o cadastro de novos clientes e abertura de contas.
        
        Parâmetro:
        - banco: Instância do banco que gerencia os clientes e contas.
        """
        self.banco = banco

    def realizar_cadastro(self, dados):
        """
        Valida os dados e solicita abertura de conta, caso todas as verificações sejam bem-sucedidas.

        Parâmetro:
        - dados (dict): Dicionário contendo os dados do formulário de cadastro.

        Retorna:
        - dict: {"sucesso": bool, "erros" ou "mensagens": list}
        """
        erros = []

        # Validação básica de campos
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

        # Validação do endereço (espera CEP, número separados por vírgula)
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

        # Verificação de cliente já existente
        cliente_existente = self.banco.buscar_cliente_por_cpf(dados["cpf"])
        if cliente_existente:
            if cliente_existente.nome.strip() != dados["nome"].strip():
                erros.append("Nome não confere com o já cadastrado.")
            
            if cliente_existente.email.strip() != dados["email"].strip():
                erros.append("Email não confere com o já cadastrado.")
            
            if cliente_existente.telefone.strip() != dados["telefone"].strip():
                erros.append("Telefone não confere com o já cadastrado.")
            
            if cliente_existente.senha.strip() != dados["senha"].strip():
                erros.append("Senha não confere com o já cadastrado.")
            
            if cliente_existente.data_nascimento.strip() != dados["data_nascimento"].strip():
                erros.append("Data de nascimento não confere com o já cadastrado.")

        if erros:
            return {"sucesso": False, "erros": erros}

        # Chama o banco para criação da conta
        resultado = self.banco.abrir_conta(
            tipo_conta      = dados["tipo_conta"],
            nome            = dados["nome"],
            cpf             = dados["cpf"],
            telefone        = dados["telefone"],
            email           = dados["email"],
            cep             = cep,
            num_end = numero,
            senha           = dados["senha"],
            data_nascimento = dados["data_nascimento"]
        )

        if resultado and resultado.get("sucesso"):
            return {"sucesso": True}
        else:
            return {
                "sucesso": False,
                "erros": resultado.get("mensagens", ["Erro desconhecido ao criar conta."])
            }
