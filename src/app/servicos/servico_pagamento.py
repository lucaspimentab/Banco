class ServicoPagamento:
    def __init__(self, cliente):
        self.cliente = cliente
        self.banco = cliente.banco  # Supondo que cada cliente tem acesso ao banco

    def efetuar_pagamento(self, dados):
        erros = []

        cpf_destino = dados.get("cpf_destino", "").strip()
        valor_str = dados.get("valor", "").strip()
        descricao = dados.get("descricao", "").strip()

        if not cpf_destino.isdigit() or len(cpf_destino) != 11:
            erros.append("CPF inválido.")

        try:
            valor = float(valor_str)
            if valor <= 0:
                erros.append("O valor deve ser maior que zero.")
        except ValueError:
            erros.append("Valor inválido.")

        if cpf_destino == self.cliente.cpf:
            erros.append("Não é possível transferir para si mesmo.")

        cliente_destino = self.banco.buscar_cliente_por_cpf(cpf_destino)
        if not cliente_destino:
            erros.append("Destinatário não encontrado.")

        if self.cliente.conta.saldo < valor:
            erros.append("Saldo insuficiente.")

        if erros:
            return {"sucesso": False, "erros": erros}

        # Simulação de transferência
        self.cliente.conta.sacar(valor)
        cliente_destino.conta.depositar(valor)

        transacao = {
            "tipo": "Pagamento",
            "valor": valor,
            "para": cpf_destino,
            "descricao": descricao
        }

        self.cliente.conta.historico.append(transacao)

        return {"sucesso": True}
