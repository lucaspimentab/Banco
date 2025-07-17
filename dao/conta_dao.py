from model.conta import Conta
from mapper.conta_mapper import ContaMapper
from dao.dao import DAO
from utils.constantes import ARQUIVO_CONTAS


class ContaDAO(DAO):
    """
    DAO responsável pela persistência de objetos do tipo Conta,
    como ContaCorrente e ContaPoupanca, no arquivo JSON de contas.
    """

    def __init__(self):
        """
        Inicializa o DAO com cache local e caminho do arquivo JSON.
        """
        super().__init__(ARQUIVO_CONTAS)
        self._cache_contas = None

    def criar_objeto(self, dados: dict) -> Conta:
        """
        Constrói uma instância de Conta a partir de um dicionário.
        """
        return ContaMapper.from_dict(dados)

    def extrair_dados_do_objeto(self, conta: Conta) -> dict:
        """
        Converte uma instância de Conta em dicionário serializável.
        """
        return ContaMapper.to_dict(conta)

    def tipo_de_id(self) -> str:
        """
        Define o campo identificador único da Conta.
        """
        return "numero"

    def listar_todos_objetos(self) -> list[Conta]:
        """
        Retorna todas as contas armazenadas, com suporte a cache local.
        """
        if self._cache_contas is not None:
            return self._cache_contas

        dados = self._ler_dados_do_json()
        self._cache_contas = [self.criar_objeto(d) for d in dados]
        return self._cache_contas

    def buscar_por_id(self, id_valor: str) -> Conta | None:
        """
        Retorna a conta correspondente ao número informado.
        """
        return next(
            (c for c in self.listar_todos_objetos() if str(c.get_numero_conta()) == str(id_valor)),
            None
        )

    def salvar_objeto(self, conta: Conta) -> None:
        """
        Salva uma nova conta e limpa o cache.
        """
        super().salvar_objeto(conta)
        self._cache_contas = None

    def atualizar_objeto(self, conta: Conta) -> bool:
        """
        Atualiza uma conta existente e limpa o cache.
        """
        atualizado = super().atualizar_objeto(conta)
        self._cache_contas = None
        return atualizado

    def deletar_objeto(self, id_valor: str) -> bool:
        """
        Remove uma conta com base no número e limpa o cache.
        """
        deletado = super().deletar_objeto(id_valor)
        self._cache_contas = None
        return deletado