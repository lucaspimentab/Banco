from abc import ABC, abstractmethod 
import datetime

class Conta(ABC):
    contador_conta = 1000  # Contador para gerar números únicos de conta

    def __init__(self, cliente, tipo, saldo_inicial=0.0):
        """
        Inicializa uma nova conta associada a um cliente.
        Gera número de conta automaticamente e registra data de criação.
        """
        if cliente is None:
            raise ValueError("Cliente inválido")
        self.cliente = cliente
        self.numero_conta = Conta.contador_conta
        Conta.contador_conta += 1
        self.ativa = True
        self.tipo = tipo
        self.saldo = saldo_inicial
        self.data_criacao = datetime.datetime.now()
        self.data_ultima_movimentacao = self.data_criacao
        self.transacoes = []
        cliente.adicionar_conta(self)

    def desativar_conta(self):
        """
        Desativa a conta se ela estiver ativa.
        Retorna mensagem de sucesso ou erro.
        """
        if not self.ativa:
            return {"sucesso": False, "mensagem": "Conta já está desativada."}
        self.ativa = False
        
        return {"sucesso": True, "mensagem": "Conta desativada com sucesso."}

    def reativar_conta(self):
        """
        Reativa a conta se ela estiver desativada.
        Retorna mensagem de sucesso ou erro.
        """
        if self.ativa:
            return {"sucesso": False, "mensagem": "Conta já está ativa."}
        self.ativa = True    
        
        return {"sucesso": True, "mensagem": "Conta reativada com sucesso."}

    def depositar(self, valor):
        """
        Realiza um depósito na conta se estiver ativa e valor for válido.
        Atualiza data da última movimentação e registra transação.
        """
        try:
            valor_dec = float(valor)
        except ValueError:
            return {"sucesso": False, "mensagem": "Valor de depósito inválido."}

        if not self.ativa:
            return {"sucesso": False, "mensagem": "Conta desativada."}

        if valor_dec <= 0:
            return {"sucesso": False, "mensagem": "Valor de depósito deve ser maior que zero."}

        self.saldo += valor_dec
        self.data_ultima_movimentacao = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transacoes.append(f"Depósito: R$ {valor_dec:.2f}")
        
        return {
            "sucesso": True, 
            "mensagem": f"Depósito de R$ {valor_dec:.2f} realizado.", 
            "novo_saldo": self.saldo
        }

    def sacar(self, valor):
        """
        Realiza um saque se a conta estiver ativa, valor for válido
        e saldo suficiente. Registra a movimentação.
        """
        try:
            valor_dec = float(valor)
        except ValueError:
            return {"sucesso": False, "mensagem": "Valor de saque inválido."}

        if not self.ativa:
            return {"sucesso": False, "mensagem": "Conta desativada."}

        if valor_dec <= 0:
            return {"sucesso": False, "mensagem": "Valor de saque deve ser maior que zero."}

        if valor_dec > self.saldo:
            return {"sucesso": False, "mensagem": "Saldo insuficiente."}

        self.saldo -= valor_dec
        self.data_ultima_movimentacao = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transacoes.append(f"Saque: R$ {valor_dec:.2f}")
        
        return {
            "sucesso": True, 
            "mensagem": f"Saque de R$ {valor_dec:.2f} realizado.", 
            "novo_saldo": self.saldo
        }

    def transferir(self, outra_conta, valor):
        """
        Realiza transferência entre contas ativas, se houver saldo suficiente
        e o valor for válido. Atualiza a movimentação nas duas contas.
        """
        try:
            valor_dec = float(valor)
        except ValueError:
            return {"sucesso": False, "mensagem": "Valor de transferência inválido."}

        if not self.ativa or not outra_conta.ativa:
            return {"sucesso": False, "mensagem": "Uma das contas está desativada."}

        if valor_dec <= 0:
            return {"sucesso": False, "mensagem": "Valor de transferência deve ser maior que zero."}

        if valor_dec > self.saldo:
            return {"sucesso": False, "mensagem": "Saldo insuficiente."}

        self.saldo -= valor_dec
        outra_conta.saldo += valor_dec
        agora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.data_ultima_movimentacao = agora
        outra_conta.data_ultima_movimentacao = agora
        self.transacoes.append(f"Transferido R$ {valor_dec:.2f} para conta {outra_conta.numero_conta}")
        outra_conta.transacoes.append(f"Recebido R$ {valor_dec:.2f} da conta {self.numero_conta}")
        
        return {
            "sucesso": True, 
            "mensagem": f"Transferência de R$ {valor_dec:.2f} realizada.", 
            "novo_saldo": self.saldo
        }

    def get_resumo(self):
        """
        Retorna um dicionário com os dados resumidos da conta,
        incluindo saldo, status, datas e transações.
        """
        return {
            "numero_conta": self.numero_conta,
            "tipo": self.tipo,
            "saldo": self.saldo,
            "ativa": self.ativa,
            "data_criacao": self.data_criacao.strftime("%Y-%m-%d %H:%M:%S"),
            "ultima_movimentacao": self.data_ultima_movimentacao,
            "transacoes": self.transacoes
        }

    def verificar_operacao_segura(self, cliente_id, senha=None):
        """
        Verifica se a operação é segura comparando o ID do cliente
        e, se fornecida, valida também a senha.
        """
        if self.cliente.id != cliente_id:
            return False

        if senha is not None:
            if not self.cliente.verificar_senha(senha):
                return False
        
        return True

    @abstractmethod
    def limite_saque(self):
        """
        Método abstrato para retornar o limite de saque da conta.
        """
        pass

    @abstractmethod
    def pode_emitir_cheque_especial(self):
        """
        Método abstrato para indicar se a conta permite cheque especial.
        """
        pass

    @abstractmethod
    def calcular_rendimento_mensal(self):
        """
        Método abstrato para calcular rendimento mensal da conta.
        """
        pass

    @abstractmethod
    def aplicar_taxas(self):
        """
        Método abstrato para aplicar taxas mensais à conta.
        """
        pass

    @abstractmethod
    def aplicar_juros(self):
        """
        Método abstrato para aplicar juros mensais à conta.
        """
        pass
