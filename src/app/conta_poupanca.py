from app.conta import Conta

class ContaPoupanca(Conta):
    def __init__(self, cliente, saldo_inicial=0.0, taxa_juros=0.005):
        super().__init__(cliente, "Poupanca", saldo_inicial)
        self._taxa_juros = taxa_juros  # 🔒 protegido

    @property
    def taxa_juros(self):
        return self._taxa_juros

    def limite_saque(self):
        return self.saldo  # sem cheque especial

    def pode_emitir_cheque_especial(self):
        return False

    def calcular_rendimento_mensal(self):
        return self.saldo * self._taxa_juros

    def aplicar_taxas(self):
        # Pode implementar tarifa futura, se necessário
        pass

    def aplicar_juros(self):
        # Exemplo: aplicar rendimento ao saldo
        rendimento = self.calcular_rendimento_mensal()
        if rendimento > 0:
            self._saldo += rendimento
            self.registrar_transacao(
                tipo="Rendimento",
                valor=rendimento,
                descricao="Rendimento mensal aplicado"
            )
