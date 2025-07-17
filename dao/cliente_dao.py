from typing import Optional, List
from model.cliente import Cliente
from dao.dao import DAO
from dao.pessoa_dao import PessoaDAO
from dao.conta_dao import ContaDAO
from utils.constantes import ARQUIVO_CLIENTES


class ClienteDAO(DAO):
    """
    DAO responsável pela persistência de objetos Cliente, vinculando
    Pessoa, senha e lista de contas associadas.
    """

    def __init__(self):
        """
        Inicializa o DAO de clientes, bem como os DAOs auxiliares para Pessoa e Conta.
        """
        super().__init__(ARQUIVO_CLIENTES)
        self._pessoa_dao = PessoaDAO()
        self._conta_dao = ContaDAO()
        self._cache_clientes_objetos = None

    def criar_objeto(self, dados: dict) -> Cliente:
        """
        Constrói um objeto Cliente a partir dos dados do JSON, incluindo as contas vinculadas.
        """
        pessoa = self._pessoa_dao.buscar_por_id(dados["numero_documento"])
        todas_contas = {c.get_numero_conta(): c for c in self._conta_dao.listar_todos_objetos()}

        contas = []
        for n in dados.get("contas", []):
            try:
                numero = int(n)
                if numero in todas_contas:
                    contas.append(todas_contas[numero])
            except ValueError:
                continue

        return Cliente(pessoa=pessoa, senha=dados["senha"], contas=contas)

    def extrair_dados_do_objeto(self, obj: Cliente) -> dict:
        """
        Converte um objeto Cliente em dicionário para persistência no JSON.
        """
        return {
            "numero_documento": obj.pessoa.get_numero_documento(),
            "senha": obj._senha,
            "contas": [str(c.get_numero_conta()) for c in obj.contas],
        }

    def tipo_de_id(self) -> str:
        """
        Define o campo identificador único do cliente no JSON.
        """
        return "numero_documento"

    def listar_todos_objetos(self) -> List[Cliente]:
        """
        Retorna todos os clientes armazenados, com suporte a cache.
        """
        if self._cache_clientes_objetos is not None:
            return self._cache_clientes_objetos

        dados_raw = self._ler_dados_do_json()
        self._cache_clientes_objetos = [self.criar_objeto(d) for d in dados_raw]
        return self._cache_clientes_objetos

    def buscar_por_id(self, id_valor: str) -> Optional[Cliente]:
        """
        Retorna o cliente com o documento informado.
        """
        return super().buscar_por_id(id_valor)

    def salvar_objeto(self, obj: Cliente) -> None:
        """
        Salva um novo cliente e limpa o cache.
        """
        super().salvar_objeto(obj)
        self._cache_clientes_objetos = None

    def atualizar_objeto(self, obj: Cliente) -> bool:
        """
        Atualiza um cliente existente e limpa o cache.
        """
        resultado = super().atualizar_objeto(obj)
        self._cache_clientes_objetos = None
        return resultado

    def deletar_objeto(self, id_valor: str) -> bool:
        """
        Remove um cliente com base no número do documento e limpa o cache.
        """
        resultado = super().deletar_objeto(id_valor)
        self._cache_clientes_objetos = None
        return resultado

    def buscar_cliente_por_numero_conta(self, numero_conta: int) -> Optional[Cliente]:
        """
        Retorna o cliente associado à conta informada.
        """
        for cliente in self.listar_todos_objetos():
            if any(str(c.get_numero_conta()) == str(numero_conta) for c in cliente.contas):
                return cliente
        return None