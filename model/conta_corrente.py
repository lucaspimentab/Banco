from model.conta import Conta
from model.exceptions import ContaInativaError
from utils.constantes import TAXA_MANUTENCAO_CCORRENTE


class ContaCorrente(Conta):
    """
    Representa uma conta corrente, com limite de transferência superior e taxa mensal de manutenção.
    Não possui rendimento automático.
    """

    def atualizacao_mensal(self) -> None:
        """
        Aplica a taxa de manutenção mensal ao saldo da conta.

        Nota:
            O saldo pode ficar negativo, se necessário.

        Raises:
            ContaInativaError: Se a conta estiver inativa.
        """
        if not self.get_estado_da_conta():
            raise ContaInativaError(self.get_numero_conta())

        novo_saldo = self._saldo - TAXA_MANUTENCAO_CCORRENTE
        self._set_saldo(novo_saldo, permitir_negativo=True)
        self._registrar_operacao(
            f"Atualização mensal: taxa de manutenção de R$ {TAXA_MANUTENCAO_CCORRENTE:.2f} cobrada."
        )