from app.conta import Conta

class ContaCorrente(Conta):
    def __init__(self, cliente, saldo_inicial=0.0, limite=500.0):
        super().__init__(cliente, "Corrente", saldo_inicial)
        self.limite = limite

    def limite_saque(self):
        return self.saldo + self.limite

    def pode_emitir_cheque_especial(self):
        return True

    def calcular_rendimento_mensal(self):
        return 0.0

    def aplicar_taxas(self):
        pass

    def aplicar_juros(self):
        pass