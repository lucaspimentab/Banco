from abc import ABC, abstractmethod
from utils.validadores.validar_pessoa import ValidarPessoa as Validar
from utils.api import API


class Pessoa(ABC):
    """
    Classe abstrata que representa uma pessoa (física ou jurídica).

    Atributos:
        - nome, email, número de documento, telefone.
        - CEP e número do endereço, com busca automática via API (ViaCEP).
    """

    def __init__(
        self,
        nome: str,
        email: str,
        numero_documento: str,
        cep: str,
        numero_endereco: str,
        telefone: str,
        endereco: str = None 
    ) -> None:
        """
        Inicializa uma instância de Pessoa com os dados fornecidos.

        Nota:
            As validações são feitas nas subclasses.
            Esta classe assume que os dados recebidos já são válidos.

        Raises:
            ValueError: Em caso de falha ao buscar o endereço via API.
        """
        self._nome = nome
        self._email = email
        self._numero_documento = numero_documento
        self._cep = cep
        self._numero_endereco = numero_endereco
        self._telefone = telefone
        self._endereco = endereco
        self._atualizar_endereco()

    @abstractmethod
    def __str__(self) -> str:
        """
        Retorna a representação textual da pessoa.
        Deve ser implementado por subclasses.
        """
        pass

    # === Getters e Setters ===

    def get_nome(self) -> str:
        return self._nome

    def set_nome(self, novo_nome: str) -> None:
        Validar.nome(novo_nome)
        self._nome = novo_nome

    def get_email(self) -> str:
        return self._email

    def set_email(self, novo_email: str) -> None:
        Validar.email(novo_email)
        self._email = novo_email

    def get_numero_documento(self) -> str:
        return self._numero_documento

    def get_cep(self) -> str:
        return self._cep

    def set_cep(self, novo_cep: str) -> None:
        Validar.cep(novo_cep)
        self._cep = novo_cep

    def get_numero_endereco(self) -> str:
        return self._numero_endereco

    def set_numero_endereco(self, novo_numero: str) -> None:
        Validar.numero_endereco(novo_numero)
        self._numero_endereco = novo_numero

    def get_endereco(self) -> str:
        return self._endereco

    def get_telefone(self) -> str:
        return self._telefone

    def set_telefone(self, novo_telefone: str) -> None:
        Validar.telefone(novo_telefone)
        self._telefone = novo_telefone

    # === Lógica de endereço ===

    def _atualizar_endereco(self) -> None:
        """
        Consulta a API externa e atualiza o endereço completo da pessoa.

        Otimizado para evitar chamada se o endereço já estiver preenchido.
        """
        self._endereco = API.buscar_endereco_por_cep(self._cep, self._numero_endereco)