from datetime import datetime

class Transacao:
    def __init__(self, tipo, valor, descricao="", origem=None, destino=None):
        """
        Representa uma transação bancária entre contas.

        Parâmetros:
        - tipo (str): Tipo da transação (ex: "PIX", "Pagamento", "Depósito").
        - valor (float): Valor da transação.
        - descricao (str, opcional): Texto descritivo da transação.
        - origem (str/int, opcional): Identificador da origem (CPF ou conta).
        - destino (str/int, opcional): Identificador do destino (CPF ou conta).
        """
        self.tipo = tipo
        self.valor = valor
        self.descricao = descricao
        self.origem = origem
        self.destino = destino
        self.data = datetime.now()

    def __str__(self):
        """
        Retorna uma representação legível da transação.

        Exemplo:
        [2025-05-17 14:25:36] Pagamento: R$ 150.00 - Conta de luz
        """
        info = f"[{self.data.strftime('%Y-%m-%d %H:%M:%S')}] {self.tipo.title()}: R$ {self.valor:.2f}"
        if self.descricao:
            info += f" - {self.descricao}"
        return info
