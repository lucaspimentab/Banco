from datetime import datetime

class Transacao:
    def __init__(self, tipo, valor, descricao=""):
        self.tipo = tipo
        self.valor = valor
        self.descricao = descricao
        self.data = datetime.now()

    def __str__(self):
        return f"[{self.data.strftime('%Y-%m-%d %H:%M:%S')}] {self.tipo.title()}: R$ {self.valor:.2f} - {self.descricao}"
