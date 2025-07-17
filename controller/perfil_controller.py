from dao.cliente_dao import ClienteDAO
from dao.pessoa_dao import PessoaDAO 
from model.pessoa_fisica import PessoaFisica
from model.cliente import Cliente
from utils.logger import logger
from typing import Optional


class PerfilController:
    """
    Controlador responsável por intermediar o acesso e atualização de dados de perfil de clientes.
    """

    @staticmethod
    def buscar_cliente_por_documento(doc: str) -> Optional[Cliente]:
        """
        Busca um cliente pelo número do documento (CPF ou CNPJ).
        """
        logger.info(f"Buscando cliente pelo documento: {doc}")
        return ClienteDAO().buscar_por_id(doc)

    @staticmethod
    def buscar_cliente_por_conta(numero_conta: int) -> Optional[Cliente]:
        """
        Busca um cliente associado a uma conta específica.
        """
        logger.info(f"Buscando cliente pela conta: {numero_conta}")
        return ClienteDAO().buscar_cliente_por_numero_conta(numero_conta)

    @staticmethod
    def atualizar_cliente(cliente: Cliente):
        """
        Atualiza os dados persistidos de um cliente.
        """
        ClienteDAO().atualizar_objeto(cliente)
        PessoaDAO().atualizar_objeto(cliente.pessoa)

    @staticmethod
    def obter_dados_perfil(documento: str) -> dict:
        """
        Retorna um dicionário com os dados públicos e financeiros do cliente.

        Returns:
            dict: Contendo chaves "status", "dados" ou "mensagem" em caso de erro.
        """
        logger.info(f"Buscando dados de perfil para documento: {documento}")
        try:
            cliente = ClienteDAO().buscar_por_id(documento)
            if cliente is None:
                return {"status": "erro", "mensagem": "Cliente não encontrado."}

            pessoa = cliente.pessoa
            tipo_doc = "CPF" if pessoa.get_tipo() == "fisica" else "CNPJ"

            dados = {
                "nome": pessoa.get_nome(),
                "documento_formatado": f"{tipo_doc}: {pessoa.get_numero_documento()}",
                "email": pessoa.get_email(),
                "cep": pessoa.get_cep(),
                "numero_endereco": pessoa.get_numero_endereco(),
                "telefone": pessoa.get_telefone(),
                "endereco": pessoa.get_endereco(),
                "contas": cliente.contas,
                "data_nascimento": (
                    pessoa.get_data_nascimento().strftime("%d/%m/%Y")
                    if isinstance(pessoa, PessoaFisica) else None
                )
            }

            return {"status": "sucesso", "dados": dados}

        except Exception as e:
            logger.error(f"Erro ao obter dados do perfil: {e}")
            return {"status": "erro", "mensagem": "Erro ao obter dados do perfil."}