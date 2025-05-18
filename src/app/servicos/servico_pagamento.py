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
        - dados (dict): Deve conter as chaves "cpf_destino", "valor" e "descricao".

        Retorna:
        - dict com status da operação, erros (se houver) ou confirmação de sucesso.
        """
        erros = []

        # Extração e validação de dados
        cpf_destino = dados.get("cpf_destino", "").strip()
        valor_str = dados.get("valor", "").strip()
        descricao = dados.get("descricao", "").strip()

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

        # Verifica se o cliente de destino existe
        cliente_destino = self.banco.buscar_cliente_por_cpf(cpf_destino)
        if not cliente_destino:
            erros.append("Destinatário não encontrado.")

        # Busca contas padrão
        conta_origem = self.cliente.buscar_conta_padrao()
        conta_destino = cliente_destino.buscar_conta_padrao()

        # Validação de saldo
        if conta_origem and conta_origem.saldo < valor:
            erros.append("Saldo insuficiente.")

        # Retorno em caso de erro
        if erros:
            return {"sucesso": False, "erros": erros}

        # Efetua a transferência
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

        return {"sucesso": True}
