from abc import ABC, abstractmethod
from utils.helpers import data_hora_atual_str
from utils.validadores.validar_conta import ValidarConta as Validar
from utils.constantes import LIMITE_TRANSFERENCIA_CCORRENTE
from model.exceptions import ContaInativaError

class Conta(ABC):
    """
    Representa uma conta bancária.

    Attributes:
        _numero_conta (str): Número único da conta.
        _saldo (float): Saldo atual da conta.
        _historico (list[str]): Lista de operações realizadas.
        _ativa (bool): Indica se a conta está ativa.
    """

    def __init__(self, numero: str, saldo: float = 0.0, historico: list[str] = None, ativa: bool = True) -> None:
        """
        Inicializa uma conta bancária com os dados necessários.
        
        Todos os parâmetros são validados e em caso de valores inválidos, uma exceção será lançada
        contendo todos os erros é lançada.

        Args:
            numero (str): Número da conta.
            saldo (float, opcional): Saldo da conta (pode ser negativo). Padrão: 0.0.
            historico (list[str], opcional): Lista de transações registradas. Padrão: lista vazia.
            ativa (bool, opcional): Estado da conta (ativa ou inativa). Padrão: True.

        Raises:
            ValueError: Se um ou mais valores forem inválidos e/ou esiverem com tipo incorreto.
        """
        historico = historico or []

        erros = Validar.todos_campos(numero, saldo, historico, ativa)
        if erros:
            raise ValueError("\n".join(erros))

        self._numero_conta = numero
        self._saldo = saldo
        self._historico = historico
        self._ativa = ativa

    @abstractmethod
    def atualizacao_mensal(self) -> None:
        """
        Aplica regras específicas de atualização mensal.

        Este método deve ser implementado pelas subclasses.
        """
        pass

    @property
    def limite_transferencia(self) -> float:
        """
        Retorna o valor máximo permitido para transferência.
        Subclasses podem sobrescrever esta propriedade para impor limites específicos.

        Returns:
            float: Valor máximo que pode ser transferido.
        """
        return float(LIMITE_TRANSFERENCIA_CCORRENTE)

    def transferir(self, destino: 'Conta', valor: float) -> None:
        """
        Transfere um valor para outra conta, seguindo o fluxo:
            1. Verifica contas ativas
            2. Verifica valor positivo
            3. Verifica saldo
            4. Verifica limite específico
            5. Executa débito/crédito e registra operação

        Args:
            destino (Conta): Conta de destino.
            valor (float): Valor a ser transferido.
        
        Raises:
            ContaInativaError: Se a conta origem ou destino estiver inativa.
            ValueError: Se o valor for inválido, se o saldo for insuficiente ou se o valor exceder o limite permitido.
        """
        if not self._ativa:
            raise ContaInativaError(self.get_numero_conta())
        if not destino._ativa:
            raise ContaInativaError(destino.get_numero_conta())
        if valor <= 0:
            raise ValueError("O valor da transferência deve ser positivo.")
        if valor > self._saldo:
            raise ValueError("Saldo insuficiente para a transferência.")
        if valor > self.limite_transferencia:
            raise ValueError(
                f"O valor da transferência excede o limite de R$ {self.limite_transferencia:.2f}."
            )

        self._set_saldo(self._saldo - valor)
        destino._set_saldo(destino._saldo + valor)
        self._registrar_operacao(
            f"Transferência de R$ {valor:.2f} para conta {destino.get_numero_conta()}"
        )
        destino._registrar_operacao(
            f"Recebido R$ {valor:.2f} da conta {self.get_numero_conta()}"
        )

    def encerrar_conta(self) -> None:
        """
        Encerra a conta, tornando-a inativa.
        Faz o registro de encerramento e adiciona no histórico.
        """
        self._ativa = False
        self._registrar_operacao("Conta encerrada")

    def get_estado_da_conta(self) -> bool:
        """
        Retorna o estado atual da conta, ativo (True) ou inativo (False).

        Returns:
            bool: Estado da conta.
        """
        return self._ativa

    def get_saldo(self) -> float:
        """
        Retorna o saldo atual da conta.

        Returns:
            float: Saldo da conta.
        """
        return self._saldo

    def _set_saldo(self, novo_saldo: float, permitir_negativo: bool = False) -> None:
        """
        Define o saldo da conta, após validação.
        O método é utilizado apenas internamente e não deve ser usado fora da classe.

        Obs: A operação não é registrada!

        Args:
            novo_saldo (float): Novo valor de saldo.
            permitir_negativo (bool): Se True, permite saldos negativos (default: False)
            
        Raises:
            ValueError: Se o saldo for inválido.
            TypeError: Se o tipo for incorreto.
        """
        if permitir_negativo:
            Validar.saldo_livre(novo_saldo)
        else:
            Validar.saldo_positivo_ou_zero(novo_saldo)
        self._saldo = novo_saldo

    def get_historico(self) -> list[str]:
        """
        Retorna o histórico de transações da conta.

        Returns:
            list[str]: Lista de descrições de transações.
        """
        return self._historico.copy()

    def get_numero_conta(self) -> str:
        """
        Retorna o número da conta.

        Returns:
            str: Número da conta.
        """
        return self._numero_conta

    def _registrar_operacao(self, descricao: str) -> None:
        """
        Adiciona um registro da operação no histórico da conta, com data e hora.

        Args:
            descricao (str): Descrição da operação.
        """
        registro = f"[{data_hora_atual_str()}] {descricao}"
        self._historico.append(registro)

    def __str__(self) -> str:
        """
        Retorna uma representação textual da conta.

        Returns:
            str: Representação da conta.
        """
        return f"Conta {self.get_numero_conta()} | Saldo: R$ {self.get_saldo():.2f}"

    @property
    def numero_documento(self) -> str:
        return self._pessoa.get_numero_documento()
