from app.transacao import Transacao

class ServicoPagamento:
    def __init__(self, banco, cliente):
        """
        Serviço responsável por realizar pagamentos entre contas de clientes.

        Parâmetros:
        - banco: Instância do Banco contendo os clientes e contas.
        - cliente: Cliente que está efetuando o pagamento.
        """
        self.banco = banco
        self.cliente = cliente

    def efetuar_pagamento(self, dados):
        """
        Realiza a transferência de valor da conta do cliente logado para o CPF de destino.

        Parâmetros:
        - dados (dict): Deve conter as chaves:
            - "cpf_destino": CPF do destinatário
            - "valor": Valor a ser transferido
            - "descricao": Descrição da transação
            - "conta_origem": Número da conta do cliente que está pagando

        Retorna:
        - dict com status da operação, erros (se houver) ou confirmação de sucesso.
        """
        erros = []

        cpf_destino = dados.get("cpf_destino", "").strip()
        valor_str = dados.get("valor", "").strip()
        descricao = dados.get("descricao", "").strip()
        conta_origem = dados.get("conta_origem")

        # Validações iniciais
        if not cpf_destino.isdigit() or len(cpf_destino) != 11:
            erros.append("CPF inválido.")

        try:
            valor = float(valor_str)
            if valor <= 0:
                erros.append("Valor deve ser positivo.")
        except ValueError:
            erros.append("Valor inválido.")

        if cpf_destino == self.cliente.cpf:
            erros.append("Não é possível transferir para si mesmo.")

        if not conta_origem or not conta_origem.ativa:
            erros.append("Conta de origem inválida.")

        # Verifica destinatário
        cliente_destino = self.banco.buscar_cliente_por_cpf(cpf_destino)
        if not cliente_destino:
            erros.append("Destinatário não encontrado.")

        # Envia pagamento para 1a conta ativa do destinatário
        contas_ativas = [conta for conta in cliente_destino.contas if conta.ativa]
        conta_destino = contas_ativas[0] if contas_ativas else None
        
        # Demais validações
        if conta_origem and conta_origem.saldo < valor:
            erros.append("Saldo insuficiente.")

        if not conta_destino:
            erros.append("Conta de destino não encontrada.")

        # Retorna erros, se houver
        if erros:
            return {"sucesso": False, "erros": erros}

        # Realiza transferência
        conta_origem.sacar(valor)
        conta_destino.depositar(valor)

        # Registra a transação
        transacao = Transacao(
            tipo = "Pagamento",
            valor = valor,
            origem = self.cliente.cpf,
            destino = cpf_destino,
            descricao = descricao
        )
        conta_origem.registrar_transacao(transacao)

        return {
            "sucesso": True,
            "mensagem": f"Pagamento de R$ {valor:.2f} realizado com sucesso para {cpf_destino}."
        }
