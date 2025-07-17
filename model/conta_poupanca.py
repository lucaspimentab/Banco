from model.conta import Conta
from model.exceptions import ContaInativaError
from utils.constantes import (
    LIMITE_TRANSFERENCIA_CPOUPANCA,
    RENDIMENTO_MENSAL_CPOUPANCA
)


class ContaPoupanca(Conta):
    """
    Representa uma conta poupança, com rendimento mensal e limite de transferência reduzido.
    Herda os comportamentos padrão da classe Conta.
    """

    @property
    def limite_transferencia(self) -> float:
        """
        Limite específico de transferência para contas poupança.
        """
        return LIMITE_TRANSFERENCIA_CPOUPANCA

    def atualizacao_mensal(self) -> None:
        """
        Aplica o rendimento mensal sobre o saldo da conta.

        Raises:
            ContaInativaError: Se a conta estiver inativa.
        """
        if not self.get_estado_da_conta():
            raise ContaInativaError(self.get_numero_conta())

        rendimento = self._saldo * RENDIMENTO_MENSAL_CPOUPANCA
        self._set_saldo(self._saldo + rendimento)
        self._registrar_operacao(f"Atualização mensal: rendimento de R$ {rendimento:.2f} aplicado.")