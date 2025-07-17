from dao.cliente_dao import ClienteDAO
from dao.conta_dao import ContaDAO
from model.exceptions import ContaInativaError


class PagamentoController:
    """
    Controlador responsável por processar transferências entre contas de clientes.
    """

    @staticmethod
    def processar_pagamento(
        conta_origem_num: int,
        doc_destino: str,
        valor: float,
        descricao: str,
        senha: str,
        conta_destino_numero: int
    ) -> dict:
        """
        Processa uma transferência entre contas, validando origem, destino, saldo e limites.

        Returns:
            dict: Resultado com chaves 'sucesso' e 'mensagem' ou 'erros'.
        """
        # Validação inicial
        if not all([doc_destino, valor, conta_origem_num, senha, conta_destino_numero]):
            return {"sucesso": False, "erros": ["Preencha todos os campos obrigatórios."]}

        try:
            conta_origem_num = int(conta_origem_num)
            conta_destino_numero = int(conta_destino_numero)
        except ValueError:
            return {"sucesso": False, "erros": ["Número de conta inválido."]}

        if valor <= 0:
            return {"sucesso": False, "erros": ["O valor da transferência deve ser maior que zero."]}

        cliente_dao = ClienteDAO()
        conta_dao = ContaDAO()

        # Busca cliente e conta de origem
        cliente_origem = cliente_dao.buscar_cliente_por_numero_conta(conta_origem_num)
        if not cliente_origem:
            return {"sucesso": False, "erros": ["Cliente de origem não encontrado."]}

        if not cliente_origem.verificar_senha(senha):
            return {"sucesso": False, "erros": ["Senha incorreta."]}

        conta_origem = conta_dao.buscar_por_id(conta_origem_num)
        if not conta_origem or not conta_origem.get_estado_da_conta():
            return {"sucesso": False, "erros": ["A conta de origem está inativa ou não encontrada."]}

        # Busca cliente e conta de destino
        cliente_destino = cliente_dao.buscar_por_id(doc_destino)
        if not cliente_destino:
            return {"sucesso": False, "erros": [f"Destinatário com documento {doc_destino} não encontrado."]}

        conta_destino = next(
            (c for c in cliente_destino.contas if int(c.get_numero_conta()) == conta_destino_numero),
            None
        )
        if not conta_destino or not conta_destino.get_estado_da_conta():
            return {"sucesso": False, "erros": ["Conta de destino não encontrada ou está inativa."]}

        if conta_origem.get_numero_conta() == conta_destino.get_numero_conta():
            return {"sucesso": False, "erros": ["Você não pode transferir para a mesma conta."]}

        if valor > conta_origem.get_saldo():
            return {"sucesso": False, "erros": ["Saldo insuficiente para realizar a transferência."]}

        if valor > conta_origem.limite_transferencia:
            return {
                "sucesso": False,
                "erros": [f"Valor excede o limite de transferência da conta (R$ {conta_origem.limite_transferencia:.2f})."]
            }

        # Efetiva a transferência
        try:
            conta_origem.transferir(conta_destino, valor)
        except (ContaInativaError, ValueError) as e:
            return {"sucesso": False, "erros": [str(e)]}

        conta_dao.atualizar_objeto(conta_origem)
        conta_dao.atualizar_objeto(conta_destino)

        return {
            "sucesso": True,
            "mensagem": f"Transferência de R$ {valor:.2f} realizada com sucesso para {cliente_destino.pessoa.get_nome()} (conta {conta_destino_numero})."
        }