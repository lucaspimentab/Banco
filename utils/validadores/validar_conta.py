from utils.constantes import TAMANHO_MIN_NUMERO_CONTA

class ValidarConta:
    """
    Classe utilitária responsável pela validação de atributos relacionados a contas bancárias.
    Cada método lança exceções apropriadas em caso de entrada inválida.
    """

    @staticmethod
    def todos_campos(numero_conta: str, saldo: float, historico: list, estado: bool) -> list[str]:
        """
        Valida todos os campos comuns de uma conta bancária.

        Args:
            numero_conta (str): Número da conta.
            saldo (float): Saldo inicial da conta.
            historico (list): Histórico da conta.
            estado (bool): Estado da conta (ativa/inativa).

        Returns:
            erros (list[str]): Lista de mensagens de erro (vazia se não houver erros).
        """
        erros = []

        try:
            ValidarConta._numero_conta(numero_conta)
        except (ValueError, TypeError) as e:
            erros.append(str(e))

        try:
            ValidarConta.saldo_livre(saldo)
        except (ValueError, TypeError) as e:
            erros.append(str(e))

        try:
            ValidarConta._historico(historico)
        except (ValueError, TypeError) as e:
            erros.append(str(e))

        try:
            ValidarConta.estado_da_conta(estado)
        except (ValueError, TypeError) as e:
            erros.append(str(e))

        return erros

    @staticmethod
    def _numero_conta(numero_conta) -> None:
        """
        Valida o número da conta.

        Aceita string (com apenas dígitos) ou int (positivo). Converte string para int se necessário.

        Raises:
            TypeError: Se o tipo for inválido.
            ValueError: Se o número estiver vazio, for negativo, ou não for composto por dígitos.
        """
        if isinstance(numero_conta, int):
            if numero_conta < 0:
                raise ValueError("Número da conta não pode ser negativo.")
            if len(str(numero_conta)) < TAMANHO_MIN_NUMERO_CONTA:
                raise ValueError("Número da conta muito curto.")
            return

        if isinstance(numero_conta, str):
            if numero_conta.strip() == "":
                raise ValueError("Número da conta não pode ser vazio.")
            if not numero_conta.isdigit():
                raise ValueError("Número da conta deve conter apenas dígitos.")
            if len(numero_conta) < TAMANHO_MIN_NUMERO_CONTA:
                raise ValueError("Número da conta muito curto.")
            return

        raise TypeError("Número da conta deve ser um número inteiro ou string com dígitos.")


    @staticmethod
    def _verificacoes_basicas_saldo(saldo: float) -> None:
        """
        Verifica se o saldo é um número real válido e finito.

        Args:
            saldo (float): Valor a ser validado.

        Raises:
            TypeError: Se o saldo não for um número.
            ValueError: Se o saldo for NaN (não é um número) ou infinito.
        """
        if not isinstance(saldo, (int, float)):
            raise TypeError("O saldo deve ser um número.")
        if not (saldo == saldo and saldo != float("inf") and saldo != float("-inf")):
            raise ValueError("O saldo não pode ser NaN ou infinito.")

    @staticmethod
    def saldo_positivo_ou_zero(saldo: float) -> None:
        """
        Valida que o saldo é numérico, finito e não-negativo.

        Essa validação é usada em operações que não permitem saldo negativo,
        como transferências bancárias.

        Args:
            saldo (float): Valor a ser validado.

        Raises:
            TypeError: Se o saldo não for um número.
            ValueError: Se o saldo for NaN ou infinito.
            ValueError: Se o saldo for negativo.
        """
        ValidarConta._verificacoes_basicas_saldo(saldo)
        if saldo < 0:
            raise ValueError("O saldo não pode ser negativo.")

    @staticmethod
    def saldo_livre(saldo: float) -> None:
        """
        Valida que o saldo é numérico e finito, permitindo valores negativos.

        Essa validação é usada em situações onde saldos negativos são aceitáveis,
        como atualizações mensais de cobrança.

        Args:
            saldo (float): Valor a ser validado.

        Raises:
            TypeError: Se o saldo não for um número.
            ValueError: Se o saldo for NaN ou infinito.
        """
        ValidarConta._verificacoes_basicas_saldo(saldo)

    @staticmethod
    def _historico(historico: list) -> None:
        """
        Valida se o histórico da conta é uma lista de strings.

        Args:
            historico (list): Lista que representa o histórico a ser validado.

        Raises:
            TypeError: Se o histórico não for uma lista.
            TypeError: Se algum item da lista não for uma string.
        """
        if not isinstance(historico, list):
            raise TypeError("Histórico da conta deve ser uma lista.")
        for item in historico:
            if not isinstance(item, str):
                raise TypeError("Cada item do histórico da conta deve ser uma string.")

    @staticmethod
    def estado_da_conta(estado: bool) -> None:
        """
        Valida se o estado da conta é um valor booleano.

        Args:
            estado (bool): Valor booleano que representa o estado da conta.

        Raises:
            TypeError: Se o estado informado não for do tipo booleano.
        """
        if not isinstance(estado, bool):
            raise TypeError("O estado da conta deve ser um valor booleano.")
