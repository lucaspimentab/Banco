from utils.validadores.validar_pessoa import ValidarPessoa as Validar

class ValidarPessoaJuridica(Validar):
    """
    Validações específicas para Pessoa Jurídica.
    """

    @staticmethod
    def todos_campos(nome, email, cnpj, cep, numero_endereco, telefone, nome_fantasia) -> list[str]:
        erros = Validar._campos_comuns(nome, email, cep, numero_endereco, telefone)

        try:
            ValidarPessoaJuridica.cnpj(cnpj)
        except ValueError as e:
            erros.append(str(e))

        return erros

    @staticmethod
    def cnpj(cnpj: str) -> None:
        cnpj_limpo = Validar._limpar_numeros(cnpj)
        if not cnpj_limpo or len(cnpj_limpo) != 14:
            raise ValueError("CNPJ inválido. Deve conter 14 dígitos numéricos.")