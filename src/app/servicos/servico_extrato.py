class ServicoExtrato:
    def __init__(self, cliente):
        """
        Serviço responsável por fornecer saldo e extrato da conta padrão do cliente.

        Parâmetro:
        - cliente: Instância do Cliente.
        """
        self.cliente = cliente

    def obter_saldo(self):
        """
        Retorna o saldo da conta padrão do cliente.

        Retorna:
        - float: Saldo da conta ou 0.0 se não houver conta padrão.
        """
        conta = self.cliente.buscar_conta_padrao()
        return conta.saldo if conta else 0.0

    def obter_transacoes(self, limite=10):
        """
        Retorna as últimas transações da conta padrão do cliente.

        Parâmetros:
        - limite (int): Número máximo de transações a retornar (padrão: 10).

        Retorna:
        - list: Lista de transações recentes ou vazia se não houver conta.
        """
        conta = self.cliente.buscar_conta_padrao()
        if conta:
            return conta.historico[-limite:]
        return []
