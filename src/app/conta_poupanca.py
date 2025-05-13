from app.conta import Conta

class ContaPoupanca(Conta):
    def __init__(self, cliente, saldo_inicial=0.0, taxa_juros=0.005):
        super().__init__(cliente, "Poupanca", saldo_inicial)
        self.taxa_juros = taxa_juros

    def limite_saque(self):
        return self.saldo

    def pode_emitir_cheque_especial(self):
        return False

    def calcular_rendimento_mensal(self):
        return self.saldo * self.taxa_juros

    def aplicar_taxas(self):
        pass

    def aplicar_juros(self):
        pass
