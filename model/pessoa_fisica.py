from datetime import datetime
from model.pessoa import Pessoa
from utils.validadores.validar_pessoa_fisica import ValidarPessoaFisica as Validar


class PessoaFisica(Pessoa):
    """
    Representa uma pessoa física, com CPF e data de nascimento.
    Herda atributos e comportamentos comuns da classe Pessoa.
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
        data_nascimento: str | datetime
    ):
        """
        Inicializa uma Pessoa Física com os dados pessoais fornecidos.

        Raises:
            ValueError: Em caso de erro na validação dos dados.
        """
        erros = Validar.todos_campos(
            nome, email, numero_documento, cep, numero_endereco, telefone, data_nascimento
        )
        if erros:
            raise ValueError("\n".join(erros))

        super().__init__(nome, email, numero_documento, cep, numero_endereco, telefone, endereco)

        self._data_nascimento = (
            datetime.strptime(data_nascimento, "%d/%m/%Y")
            if isinstance(data_nascimento, str)
            else data_nascimento
        )

    def __str__(self) -> str:
        """
        Representação textual da pessoa física (nome + CPF).
        """
        return f"{self._nome} (CPF: {self._numero_documento})"

    def get_data_nascimento(self) -> datetime:
        """
        Retorna a data de nascimento como objeto datetime.
        """
        return self._data_nascimento

    def get_tipo(self) -> str:
        """
        Retorna o tipo da pessoa ('fisica') para fins de serialização.
        """
        return "fisica"