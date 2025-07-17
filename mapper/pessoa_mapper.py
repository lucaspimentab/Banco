from model.pessoa_fisica import PessoaFisica
from model.pessoa_juridica import PessoaJuridica
from utils.constantes import TIPO_PFISICA, TIPO_PJURIDICA


class PessoaMapper:
    """
    Classe responsável por converter objetos Pessoa (física ou jurídica)
    para dicionários e vice-versa, com suporte a validação de tipo.
    """

    @staticmethod
    def from_dict(dados: dict):
        """
        Constrói uma instância de PessoaFisica ou PessoaJuridica a partir de um dicionário.

        Raises:
            ValueError: Se o tipo for desconhecido ou os dados forem inválidos.
        """
        tipo = dados.get("tipo", "").strip().lower()

        if tipo == TIPO_PFISICA.lower():
            return PessoaFisica(
                nome=dados["nome"],
                email=dados["email"],
                numero_documento=dados["numero_documento"],
                cep=dados["cep"],
                numero_endereco=dados["numero_endereco"],
                endereco=dados.get("endereco", ""),
                telefone=dados["telefone"],
                data_nascimento=dados["data_nascimento"]
            )

        if tipo == TIPO_PJURIDICA.lower():
            return PessoaJuridica(
                nome=dados["nome"],
                email=dados["email"],
                numero_documento=dados["numero_documento"],
                cep=dados["cep"],
                numero_endereco=dados["numero_endereco"],
                endereco=dados["endereco"],
                telefone=dados["telefone"],
                nome_fantasia=dados.get("nome_fantasia", "")
            )

        raise ValueError(f"Tipo de pessoa desconhecido: {tipo}")

    @staticmethod
    def to_dict(pessoa):
        """
        Converte uma instância de Pessoa em dicionário serializável.
        """
        dados = {
            "nome": pessoa.get_nome(),
            "email": pessoa.get_email(),
            "numero_documento": pessoa.get_numero_documento(),
            "cep": pessoa.get_cep(),
            "numero_endereco": pessoa.get_numero_endereco(),
            "endereco": pessoa.get_endereco(),
            "telefone": pessoa.get_telefone(),
            "tipo": pessoa.get_tipo()
        }

        if pessoa.get_tipo() == TIPO_PFISICA:
            dados["data_nascimento"] = pessoa.get_data_nascimento().strftime("%d/%m/%Y")

        elif pessoa.get_tipo() == TIPO_PJURIDICA:
            nome_fantasia = pessoa.get_nome_fantasia()
            if nome_fantasia.strip():
                dados["nome_fantasia"] = nome_fantasia

        return dados