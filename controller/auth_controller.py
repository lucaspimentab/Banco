from dao.cliente_dao import ClienteDAO
from utils.logger import logger

class AuthController:
    """
    Controlador responsável por autenticação de usuários:
    login e logout.

    Mantém uma sessão simples em memória através de um dicionário que associa
    identificadores de usuário a objetos Cliente autenticados.
    """

    sessao_ativa = {}
    _cache_clientes = {}

    @staticmethod
    def login(numero_documento: str, senha: str) -> dict:
        """
        Realiza login de um cliente com base no documento e senha.
        """
        logger.info(f"Tentando login com documento: {numero_documento}")

        try:
            # Verifica cache antes de acessar o DAO
            if numero_documento in AuthController._cache_clientes:
                cliente = AuthController._cache_clientes[numero_documento]
            else:
                cliente = ClienteDAO().buscar_por_id(numero_documento)
                if cliente:
                    AuthController._cache_clientes[numero_documento] = cliente

            if cliente is None:
                logger.warning(f"Cliente não encontrado: {numero_documento}")
                return {
                    "status"   : "erro",
                    "mensagem" : "Cliente não encontrado."
                }

            if not cliente.verificar_senha(senha):
                logger.warning("Senha incorreta para cliente.")
                return {
                    "status"   : "erro",
                    "mensagem" : "Senha incorreta."
                }

            # Armazena na sessão o cliente logado
            AuthController.sessao_ativa[numero_documento] = cliente

            logger.info("Login realizado com sucesso.")
            return {
                "status"     : "sucesso",
                "mensagem"   : "Login realizado com sucesso.",
                "usuario_id" : numero_documento
            }

        except Exception as e:
            logger.warning(f"Erro durante login: {e}")
            return {
                "status"   : "erro",
                "mensagem" : "Erro inesperado ao tentar login."
            }

    @staticmethod
    def logout(usuario_id: str) -> dict:
        """
        Realiza logout de um cliente.
        """
        logger.info(f"Logout solicitado para ID: {usuario_id}")

        if usuario_id in AuthController.sessao_ativa:
            del AuthController.sessao_ativa[usuario_id]
            logger.info("Logout bem-sucedido.")
            return {
                "status"   : "sucesso",
                "mensagem" : "Logout realizado com sucesso."
            }
        else:
            logger.warning("Tentativa de logout para sessão inexistente.")
            return {
                "status"   : "erro",
                "mensagem" : "Usuário não está logado."
            }