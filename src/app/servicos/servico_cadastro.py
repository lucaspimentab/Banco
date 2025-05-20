from app.validadores import validar_dados_cadastro

class ServicoCadastro:
    def __init__(self, banco):
        self.banco = banco

    def realizar_cadastro(self, dados):
        erros, cep, numero = validar_dados_cadastro(dados)

        cliente_existente = self.banco.buscar_cliente_por_cpf(dados["cpf"])
        if cliente_existente:
            if cliente_existente.nome.strip() != dados["nome"].strip():
                erros.append("Nome não confere com o já cadastrado.")

            if cliente_existente.email.strip() != dados["email"].strip():
                erros.append("Email não confere com o já cadastrado.")

            if cliente_existente.telefone.strip() != dados["telefone"].strip():
                erros.append("Telefone não confere com o já cadastrado.")

            if not cliente_existente.verificar_senha(dados["senha"].strip()):
                erros.append("Senha não confere com o já cadastrado.")

            if cliente_existente.data_nascimento.strip() != dados["data_nascimento"].strip():
                erros.append("Data de nascimento não confere com o já cadastrado.")

        if erros:
            return {"sucesso": False, "erros": erros}

        resultado = self.banco.abrir_conta(
            tipo_conta=dados["tipo_conta"],
            nome=dados["nome"],
            cpf=dados["cpf"],
            telefone=dados["telefone"],
            email=dados["email"],
            cep=cep,
            num_end=numero,
            senha=dados["senha"],
            data_nascimento=dados["data_nascimento"]
        )

        if resultado and resultado.get("sucesso"):
            return {"sucesso": True}
        else:
            return {
                "sucesso": False,
                "erros": resultado.get("mensagens", ["Erro desconhecido ao criar conta."])
            }
