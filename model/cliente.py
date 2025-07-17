from typing import List
from model.pessoa import Pessoa
from model.conta import Conta
from utils.validadores.validar_cliente import ValidarCliente as Validar


class Cliente:
    """
    Representa um cliente do sistema bancário.

    Um cliente possui:
        - Um objeto Pessoa com os dados pessoais (física ou jurídica).
        - Uma senha de acesso ao sistema.
        - Uma ou mais contas bancárias associadas (opcional).
    """

    def __init__(self, pessoa: Pessoa, senha: str, contas: List[Conta] = None) -> None:
        """
        Inicializa um novo cliente com pessoa, senha e lista opcional de contas.

        Raises:
            TypeError: Se os tipos de pessoa ou contas forem inválidos.
        """
        if not isinstance(pessoa, Pessoa):
            raise TypeError("O parâmetro 'pessoa' deve ser um objeto da classe Pessoa.")

        if contas is None:
            contas = []
        elif not all(isinstance(c, Conta) for c in contas):
            raise TypeError("Todos os itens em 'contas' devem ser objetos da classe Conta.")

        self._pessoa = pessoa
        self._senha = senha
        self._contas = contas

    @property
    def pessoa(self) -> Pessoa:
        """
        Retorna o objeto Pessoa associado ao cliente.
        """
        return self._pessoa

    @property
    def contas(self) -> List[Conta]:
        """
        Retorna a lista de contas associadas ao cliente.
        """
        return self._contas

    @contas.setter
    def contas(self, nova_lista: List[Conta]):
        self._contas = nova_lista

    @property
    def numero_documento(self) -> str:
        """
        Retorna o número do documento da pessoa associada.
        """
        return self._pessoa.get_numero_documento()

    def verificar_senha(self, senha_digitada: str) -> bool:
        """
        Verifica se a senha informada está correta.
        """
        return self._senha == senha_digitada

    def alterar_senha(self, senha_atual: str, nova_senha: str) -> None:
        """
        Altera a senha do cliente após validação.

        Raises:
            ValueError: Se a senha atual estiver incorreta ou a nova senha for inválida.
        """
        if not self.verificar_senha(senha_atual):
            raise ValueError("Senha atual incorreta.")
        Validar.senha(nova_senha)
        self._senha = nova_senha

    def possui_conta(self) -> bool:
        """
        Verifica se o cliente possui pelo menos uma conta cadastrada.
        """
        return bool(self._contas)