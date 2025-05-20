from datetime import datetime

class Transacao:
    def __init__(self, tipo, valor, descricao="", origem=None, destino=None, data_hora=None):
        """
        Representa uma transação bancária entre contas.
        """
        self._tipo = tipo
        self._valor = float(valor)
        self._descricao = descricao
        self._origem = origem
        self._destino = destino
        self._data_hora = data_hora or datetime.now()

    @property
    def tipo(self):
        return self._tipo

    @property
    def valor(self):
        return self._valor

    @property
    def descricao(self):
        return self._descricao

    @property
    def origem(self):
        return self._origem

    @property
    def destino(self):
        return self._destino

    @property
    def data_hora(self):
        return self._data_hora

    def __str__(self):
        """
        Retorna uma representação legível da transação.
        Exemplo:
        [2025-05-17 14:25:36] Pagamento: R$ 150.00 - Conta de luz
        """
        info = f"[{self._data_hora.strftime('%Y-%m-%d %H:%M:%S')}] {self._tipo.title()}: R$ {self._valor:.2f}"
        if self._descricao:
            info += f" - {self._descricao}"
        return info