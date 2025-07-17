from model.pessoa import Pessoa
from utils.validadores.validar_pessoa_juridica import ValidarPessoaJuridica as Validar


class PessoaJuridica(Pessoa):
    """
    Representa uma pessoa jurídica, com CNPJ e nome fantasia.
    Herda os atributos e comportamentos da classe abstrata Pessoa.
    """

    def __init__(
        self,
        nome: str,
        email: str,
        numero_documento: str,
        cep: str,
        numero_endereco: str,
        endereco: str,
        telefone: str,
        nome_fantasia: str = ""
    ):
        """
        Inicializa a pessoa jurídica com os dados obrigatórios e nome fantasia opcional.

        Raises:
            ValueError: Se houver erro na validação dos dados.
        """
        erros = Validar.todos_campos(
            nome, email, numero_documento, cep, numero_endereco, telefone, nome_fantasia
        )
        if erros:
            raise ValueError("\n".join(erros))

        super().__init__(nome, email, numero_documento, cep, numero_endereco, telefone, endereco)
        self._nome_fantasia = nome_fantasia

    def __str__(self) -> str:
        """
        Representação textual da pessoa jurídica (nome fantasia + CNPJ).
        """
        nome_exibicao = self._nome_fantasia.strip() or "Empresa sem nome fantasia"
        return f"{nome_exibicao} (CNPJ: {self._numero_documento})"

    def get_nome_fantasia(self) -> str:
        """
        Retorna o nome fantasia da empresa.
        """
        return self._nome_fantasia or ""

    def get_tipo(self) -> str:
        """
        Retorna o tipo da pessoa para fins de serialização.
        """
        return "juridica"