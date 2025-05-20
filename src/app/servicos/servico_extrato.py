class ServicoExtrato:
    def __init__(self, cliente):
        """
        Serviço responsável por fornecer saldo e extrato da conta do cliente.
        """
        self.cliente = cliente

    def obter_saldo(self, conta):
        """
        Retorna o saldo da conta do cliente.
        """
        return conta.saldo if conta else 0.0

    def obter_transacoes(self, conta, limite=10):
        """
        Retorna as últimas transações da conta do cliente.
        """
        if conta:
            return conta.transacoes[-limite:]  # 🔧 corrigido: .transacoes é @property protegida
        return []
