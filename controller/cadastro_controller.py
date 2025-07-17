from utils.logger import logger
from dao.pessoa_dao import PessoaDAO
from dao.cliente_dao import ClienteDAO
from model.cliente import Cliente


class CadastroController:
    """
    Controlador responsável pelo fluxo de cadastro de clientes no sistema.
    Garante que CPF/CNPJ e e-mail sejam únicos e cria Pessoa + Cliente.
    """

    @staticmethod
    def cadastrar_cliente(dados: dict) -> dict:
        """
        Processa o cadastro de um novo cliente com base nos dados fornecidos.

        Args:
            dados (dict): Dicionário com dados da pessoa e senha.

        Returns:
            dict: Resultado do processo com status ('sucesso' ou 'erro') e mensagem.
        """
        numero_documento = dados.get("numero_documento")
        email = dados.get("email")

        logger.info(f"Iniciando cadastro de cliente com documento: {numero_documento}")

        cliente_dao = ClienteDAO()
        pessoa_dao = PessoaDAO()

        # Verifica se já existe cliente com mesmo documento
        if cliente_dao.buscar_por_id(numero_documento):
            return {
                "status": "erro",
                "mensagem": f"Já existe um cliente cadastrado com o documento {numero_documento}."
            }

        # Verifica duplicidade de e-mail (evita instanciar Pessoa antes da verificação)
        if any(p.get("email") == email for p in pessoa_dao._ler_dados_do_json()):
            return {
                "status": "erro",
                "mensagem": f"Já existe um cliente cadastrado com o e-mail {email}."
            }

        # Tenta criar pessoa e cliente
        try:
            CadastroController._criar_pessoa(dados)
            CadastroController._criar_cliente(numero_documento, dados["senha"])
            return {
                "status": "sucesso",
                "mensagem": "Cadastro realizado com sucesso"
            }

        # Tratamento de exceções específicas
        except ValueError as e:
            logger.warning(f"Erro de validação: {e}")
            return {"status": "erro", "mensagem": str(e)}

        except TypeError as e:
            logger.warning(f"Erro de tipagem: {e}")
            return {"status": "erro", "mensagem": str(e)}

        except Exception as e:
            logger.error(f"Erro inesperado no cadastro: {e}")
            return {"status": "erro", "mensagem": "Erro inesperado ao cadastrar cliente."}

    # === MÉTODOS AUXILIARES ===

    @staticmethod
    def _criar_pessoa(dados: dict) -> None:
        """
        Cria e persiste um objeto Pessoa (física ou jurídica) com base no dicionário recebido.
        """
        from copy import deepcopy
        pessoa_dao = PessoaDAO()
        dados_pessoa = deepcopy(dados)

        # Garante existência de campo opcional
        dados_pessoa["nome_fantasia"] = dados_pessoa.get("nome_fantasia", "").strip()

        pessoa = pessoa_dao.criar_objeto(dados_pessoa)
        pessoa_dao.salvar_objeto(pessoa)

    @staticmethod
    def _criar_cliente(numero_documento: str, senha: str) -> None:
        """
        Cria um cliente a partir do documento e senha informados, associando a uma Pessoa já criada.
        """
        pessoa = PessoaDAO().buscar_por_id(numero_documento)
        if not pessoa:
            raise ValueError(f"Pessoa não encontrada para o documento {numero_documento}.")

        cliente = Cliente(pessoa=pessoa, senha=senha)
        ClienteDAO().salvar_objeto(cliente)
