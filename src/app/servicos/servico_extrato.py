class ServicoExtrato:
    def __init__(self, cliente):
        """
        Serviço responsável por fornecer saldo e extrato da conta do cliente.

        Parâmetro:
        - cliente: Instância do Cliente.
        """
        self.cliente = cliente

    def obter_saldo(self, conta):
        """
        Retorna o saldo da conta do cliente.

        Retorna:
        - float: Saldo da conta ou 0.0 se não houver conta.
        """
        return conta.saldo if conta else 0.0

    def obter_transacoes(self, conta, limite=10):
        """
        Retorna as últimas transações da conta do cliente.

        Parâmetros:
        - limite (int): Número máximo de transações a retornar (padrão: 10).

        Retorna:
        - list: Lista de transações recentes ou vazia se não houver conta.
        """
        if conta:
            return conta.historico[-limite:]
        return []
