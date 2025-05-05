from abc import ABC, abstractmethod 
import datetime
class Conta(ABC):
    contador_conta= 1000

    def __init__(self,cliente,tipo, saldo_inicial=0.0):
        if cliente is None:
            raise ValueError("Cliente inválido")
        self.cliente=cliente
        self.numero_conta= Conta.contador_conta
        Conta.contador_conta+=1
        self.ativa= True
        self.tipo= tipo
        self.saldo= saldo_inicial
        self.data_criacao = datetime.datetime.now()
        self.data_ultima_movimentacao = self.data_criacao
        self.transacoes = []
        cliente.adicionar_conta(self)


    def desativar_conta(self):
        if not self.ativa:
            return {"sucesso": False, "mensagem":"Conta já está desativada."}
        self.ativa = False
        return {"sucesso": True, "mensagem":"Conta desativada com sucesso."}
        return True

    def reativar_conta(self):
        if self.ativa:
            return {"sucesso": False, "mensagem":"Conta já está ativa."}
        self.ativa = True    
        return {"sucesso": True, "mensagem":"Conta reativada com sucesso."}
        
     
 
    def depositar(self,valor):
        try:
            valor_dec = float(valor)
        except ValueError:
            return {"sucesso": False, "mensagem": "Valor de deposito inválido."}
         
        if not self.ativa:
            return {"sucesso": False, "mensagem": "Conta desativada."}
        
        if valor_dec<=0:
            return {"sucesso": False, "mensagem": "Valor de depósito deve ser maior que zero."}
        
        self.saldo+=valor_dec
        self.data_ultima_movimentacao = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transacoes.append(f"Depósito: R$ {valor_dec:.2f}")
        return {"sucesso": True, "mensagem": f"Depósito de R$ {valor_dec:.2f} realizado.", "novo_saldo": self.saldo}

    def sacar(self,valor):
        try:
            valor_dec = float(valor)
        except ValueError:
            return {"sucesso": False, "mensagem": "Valor de saque inválido."}
        
        if not self.ativa:
            return {"sucesso": False, "mensagem": "Conta desativada."}
        
        if valor_dec<=0:
            return {"sucesso": False, "mensagem": "Valor de saque deve ser maior que zero."}
        
        if valor_dec>self.saldo:
            return {"sucesso": False, "mensagem": "Saldo insuficiente."}
        self.saldo -= valor_dec
        self.data_ultima_movimentacao = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transacoes.append(f"Saque: R$ {valor_dec:.2f}")
        return {"sucesso": True, "mensagem": f"Saque de R$ {valor_dec:.2f} realizado.", "novo_saldo": self.saldo}

    def transferir(self, outra_conta, valor):

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
        return {"sucesso": True, "mensagem": f"Transferência de R$ {valor_dec:.2f} realizada.", "novo_saldo": self.saldo}    

    def get_resumo(self):

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

        if self.cliente.id != cliente_id:
            return False
        
        if senha is not None:
            if not self.cliente.verificar_senha(senha):
                return False
        return True
    

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