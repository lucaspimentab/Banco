from abc import ABC, abstractmethod
from datetime import datetime
from app.transacao import Transacao

class Conta(ABC):
    contador_conta = 1000  # Contador para gerar números únicos de conta

    def __init__(self, cliente, tipo, saldo_inicial=0.0):
        if cliente is None:
            raise ValueError("Cliente inválido")

        self._cliente = cliente
        self.numero_conta = Conta.contador_conta
        Conta.contador_conta += 1

        self._ativa = True
        self.tipo = tipo
        self._saldo = saldo_inicial
        self.data_criacao = datetime.now()
        self.data_ultima_movimentacao = self.data_criacao
        self._transacoes = []

        cliente.adicionar_conta(self)

    @property
    def saldo(self):
        return self._saldo

    @property
    def ativa(self):
        return self._ativa

    @ativa.setter
    def ativa(self, valor):
        self._ativa = valor

    @property
    def transacoes(self):
        return self._transacoes.copy()

    def desativar_conta(self):
        if not self._ativa:
            return {"sucesso": False, "mensagem": "Conta já está desativada."}
        self._ativa = False
        return {"sucesso": True, "mensagem": "Conta desativada com sucesso."}

    def reativar_conta(self):
        if self._ativa:
            return {"sucesso": False, "mensagem": "Conta já está ativa."}
        self._ativa = True
        return {"sucesso": True, "mensagem": "Conta reativada com sucesso."}

    def depositar(self, valor):
        try:
            valor_dec = float(valor)
        except ValueError:
            return {"sucesso": False, "mensagem": "Valor de depósito inválido."}

        if not self._ativa:
            return {"sucesso": False, "mensagem": "Conta desativada."}

        if valor_dec <= 0:
            return {"sucesso": False, "mensagem": "Valor de depósito deve ser maior que zero."}

        self._saldo += valor_dec
        self.data_ultima_movimentacao = datetime.now()
        self.registrar_transacao(Transacao("Depósito", valor_dec, origem=self.numero_conta))

        return {
            "sucesso": True,
            "mensagem": f"Depósito de R$ {valor_dec:.2f} realizado.",
            "novo_saldo": self._saldo
        }

    def sacar(self, valor):
        try:
            valor_dec = float(valor)
        except ValueError:
            return {"sucesso": False, "mensagem": "Valor de saque inválido."}

        if not self._ativa:
            return {"sucesso": False, "mensagem": "Conta desativada."}

        if valor_dec <= 0:
            return {"sucesso": False, "mensagem": "Valor de saque deve ser maior que zero."}

        if valor_dec > self._saldo:
            return {"sucesso": False, "mensagem": "Saldo insuficiente."}

        self._saldo -= valor_dec
        self.data_ultima_movimentacao = datetime.now()
        self.registrar_transacao(Transacao("Saque", valor_dec, origem=self.numero_conta))

        return {
            "sucesso": True,
            "mensagem": f"Saque de R$ {valor_dec:.2f} realizado.",
            "novo_saldo": self._saldo
        }

    def transferir(self, outra_conta, valor):
        try:
            valor_dec = float(valor)
        except ValueError:
            return {"sucesso": False, "mensagem": "Valor de transferência inválido."}

        if not self._ativa or not outra_conta.ativa:
            return {"sucesso": False, "mensagem": "Uma das contas está desativada."}

        if valor_dec <= 0:
            return {"sucesso": False, "mensagem": "Valor de transferência deve ser maior que zero."}

        if valor_dec > self._saldo:
            return {"sucesso": False, "mensagem": "Saldo insuficiente."}

        self._saldo -= valor_dec
        outra_conta._saldo += valor_dec
        agora = datetime.now()
        self.data_ultima_movimentacao = agora
        outra_conta.data_ultima_movimentacao = agora

        self.registrar_transacao(Transacao("Transferência", valor_dec, origem=self.numero_conta, destino=outra_conta.numero_conta))
        outra_conta.registrar_transacao(Transacao("Recebimento", valor_dec, origem=self.numero_conta, destino=outra_conta.numero_conta))

        return {
            "sucesso": True,
            "mensagem": f"Transferência de R$ {valor_dec:.2f} realizada.",
            "novo_saldo": self._saldo
        }

    def registrar_transacao(self, transacao):
        self._transacoes.append(transacao)

    def get_resumo(self):
        return {
            "numero_conta": self.numero_conta,
            "tipo": self.tipo,
            "saldo": self._saldo,
            "ativa": self._ativa,
            "data_criacao": self.data_criacao.strftime("%Y-%m-%d %H:%M:%S"),
            "ultima_movimentacao": self.data_ultima_movimentacao.strftime("%Y-%m-%d %H:%M:%S"),
            "transacoes": [str(t) for t in self._transacoes]
        }

    def verificar_operacao_segura(self, cliente_id, senha=None):
        if self._cliente.id != cliente_id:
            return False

        if senha is not None:
            if not self._cliente.verificar_senha(senha):
                return False

        return True

    # Métodos abstratos que as subclasses devem implementar
    @abstractmethod
    def limite_saque(self):
        pass

    @abstractmethod
    def pode_emitir_cheque_especial(self):
        pass

    @abstractmethod
    def calcular_rendimento_mensal(self):
        pass

    @abstractmethod
    def aplicar_taxas(self):
        pass

    @abstractmethod
    def aplicar_juros(self):
        pass