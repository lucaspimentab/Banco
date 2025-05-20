from app.transacao import Transacao
from app.validadores import validar_dados_pagamento

class ServicoPagamento:
    def __init__(self, banco, cliente):
        self.banco = banco
        self.cliente = cliente

    def efetuar_pagamento(self, dados):
        erros = validar_dados_pagamento(dados)

        cpf_destino = dados.get("cpf_destino", "").strip()
        valor_str = dados.get("valor", "").strip()
        descricao = dados.get("descricao", "").strip()
        conta_origem = dados.get("conta_origem")

        # Verifica destinatário
        cliente_destino = self.banco.buscar_cliente_por_cpf(cpf_destino)
        if not cliente_destino:
            erros.append("Destinatário não encontrado.")

        contas_ativas = [c for c in cliente_destino.contas if c.ativa] if cliente_destino else []
        conta_destino = contas_ativas[0] if contas_ativas else None

        try:
            valor = float(valor_str)
        except ValueError:
            valor = 0  # já vai falhar por valor inválido acima

        if conta_origem and conta_origem.saldo < valor:
            erros.append("Saldo insuficiente.")

        if not conta_destino:
            erros.append("Conta de destino não encontrada.")

        if cpf_destino == self.cliente.cpf:
            erros.append("Não é possível transferir para si mesmo.")

        if erros:
            return {"sucesso": False, "erros": erros}

        conta_origem.sacar(valor)
        conta_destino.depositar(valor)

        transacao = Transacao(
            tipo="Pagamento",
            valor=valor,
            origem=self.cliente.cpf,
            destino=cpf_destino,
            descricao=descricao
        )
        conta_origem.registrar_transacao(transacao)

        return {
            "sucesso": True,
            "mensagem": f"Pagamento de R$ {valor:.2f} realizado com sucesso para {cpf_destino}."
        }
