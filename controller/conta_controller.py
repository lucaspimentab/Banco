from dao.cliente_dao import ClienteDAO
from dao.conta_dao import ContaDAO
from model.conta_corrente import ContaCorrente
from model.conta_poupanca import ContaPoupanca
from utils.constantes import TIPO_CCORRENTE, TIPO_CPOUPANCA


class ContaController:
    """
    Controlador central para operações sobre contas bancárias:
    criação, reativação, encerramento, extrato, listagem e identificação de destinatários.
    """

    _cache_cliente_por_conta = {}

    @staticmethod
    def obter_extrato(numero_conta: int):
        """
        Retorna o saldo e objeto da conta, se ativa.

        Returns:
            tuple: (saldo, conta), None se houver erro.
        """
        conta = ContaDAO().buscar_por_id(numero_conta)
        if not conta:
            return None, "Conta não encontrada."
        if not conta.get_estado_da_conta():
            return None, "Conta inativa."
        return (conta.get_saldo(), conta), None

    @staticmethod
    def criar_conta(usuario_id: str, tipo_conta: str) -> dict:
        """
        Cria uma nova conta do tipo informado para o cliente especificado.

        Args:
            usuario_id (str): Documento do cliente.
            tipo_conta (str): Tipo da conta (corrente ou poupança).

        Returns:
            dict: Resultado da operação.
        """
        cliente_dao = ClienteDAO()
        conta_dao = ContaDAO()
        cliente = cliente_dao.buscar_por_id(usuario_id)
        if not cliente:
            return {"sucesso": False, "mensagem": "Cliente não encontrado."}

        for conta in cliente.contas:
            if (tipo_conta == TIPO_CCORRENTE and isinstance(conta, ContaCorrente)) or \
               (tipo_conta == TIPO_CPOUPANCA and isinstance(conta, ContaPoupanca)):
                return {"sucesso": False, "mensagem": f"Você já possui uma conta do tipo {tipo_conta}."}

        existentes = [int(c.get_numero_conta()) for c in conta_dao.listar_todos_objetos()]
        novo_numero = str(max(existentes, default=1000) + 1)

        nova_conta = (
            ContaCorrente(novo_numero) if tipo_conta == TIPO_CCORRENTE else
            ContaPoupanca(novo_numero) if tipo_conta == TIPO_CPOUPANCA else None
        )
        if not nova_conta:
            return {"sucesso": False, "mensagem": "Tipo de conta inválido."}

        conta_dao.salvar_objeto(nova_conta)

        cliente_atualizado = cliente_dao.buscar_por_id(usuario_id)
        if not cliente_atualizado:
            return {"sucesso": False, "mensagem": "Erro ao recarregar cliente."}

        cliente_atualizado.contas.append(nova_conta)
        cliente_dao.atualizar_objeto(cliente_atualizado)

        return {"sucesso": True, "mensagem": f"Conta {novo_numero} criada com sucesso!"}

    @staticmethod
    def listar_contas(usuario_id: str):
        """
        Lista todas as contas associadas ao cliente.

        Args:
            usuario_id (str): Documento do cliente.

        Returns:
            list: Contas atreladas ao cliente.
        """
        cliente = ClienteDAO().buscar_por_id(usuario_id)
        return cliente.contas if cliente else []

    @staticmethod
    def excluir_conta(usuario_id: str, numero_conta: str, senha: str) -> dict:
        """
        Encerra uma conta ativa do cliente.

        Returns:
            dict: Resultado com sucesso ou erro.
        """
        cliente_dao = ClienteDAO()
        conta_dao = ContaDAO()

        cliente = cliente_dao.buscar_por_id(usuario_id)
        if not cliente:
            return {"sucesso": False, "mensagem": "Cliente não encontrado."}
        if not cliente.verificar_senha(senha):
            return {"sucesso": False, "mensagem": "Senha incorreta."}

        conta = next((c for c in cliente.contas if str(c.get_numero_conta()) == str(numero_conta)), None)
        if not conta or not conta.get_estado_da_conta():
            return {"sucesso": False, "mensagem": "Conta não encontrada ou já está inativa."}

        conta.encerrar_conta()
        conta_dao.atualizar_objeto(conta)
        cliente_dao.atualizar_objeto(cliente)

        return {"sucesso": True, "mensagem": f"Conta {numero_conta} encerrada com sucesso."}

    @staticmethod
    def reativar_conta(usuario_id: str, numero_conta: str, senha: str) -> dict:
        """
        Reativa uma conta previamente encerrada.

        Returns:
            dict: Resultado com sucesso ou erro.
        """
        cliente_dao = ClienteDAO()
        conta_dao = ContaDAO()
        cliente = cliente_dao.buscar_por_id(usuario_id)

        if not cliente:
            return {"sucesso": False, "mensagem": "Cliente não encontrado."}
        if not cliente.verificar_senha(senha):
            return {"sucesso": False, "mensagem": "Senha incorreta."}

        conta = next((c for c in cliente.contas if str(c.get_numero_conta()) == str(numero_conta)), None)
        if not conta:
            return {"sucesso": False, "mensagem": "Conta não encontrada."}
        if conta.get_estado_da_conta():
            return {"sucesso": False, "mensagem": "A conta já está ativa."}

        conta._ativa = True
        conta_dao.atualizar_objeto(conta)
        cliente_dao.atualizar_objeto(cliente)

        return {"sucesso": True, "mensagem": f"Conta {numero_conta} reativada com sucesso."}


    @staticmethod
    def contas_ativas_para_dropdown(cliente):
        cliente_atualizado = ClienteDAO().buscar_por_id(cliente.pessoa.get_numero_documento())
        return [
            str(conta.get_numero_conta())
            for conta in cliente_atualizado.contas if conta.get_estado_da_conta()
        ]


    @staticmethod
    def obter_info_destinatario(numero_conta: int) -> str:
        """
        Retorna uma string com os dados do destinatário de uma conta.

        Args:
            numero_conta (int): Número da conta destino.

        Returns:
            str: Informações de nome, documento e número da conta.
        """
        if numero_conta in ContaController._cache_cliente_por_conta:
            cliente = ContaController._cache_cliente_por_conta[numero_conta]
        else:
            cliente = ClienteDAO().buscar_cliente_por_numero_conta(numero_conta)
            if cliente:
                ContaController._cache_cliente_por_conta[numero_conta] = cliente

        if not cliente:
            return f"Conta {numero_conta} (cliente não encontrado)"

        nome = cliente.pessoa.get_nome()
        doc = cliente.pessoa.get_numero_documento()
        return f"Destinatário: {nome} | Documento: {doc} | Conta: {numero_conta}"