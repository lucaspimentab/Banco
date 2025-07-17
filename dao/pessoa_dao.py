from dao.dao import DAO
from model.pessoa import Pessoa
from mapper.pessoa_mapper import PessoaMapper
from utils.constantes import ARQUIVO_PESSOAS


class PessoaDAO(DAO):
    """
    DAO responsável pela persistência de objetos Pessoa (ou suas subclasses)
    no arquivo JSON correspondente.
    """

    def __init__(self):
        """
        Inicializa o DAO de pessoas com cache opcional em memória.
        """
        super().__init__(ARQUIVO_PESSOAS)
        self._cache_pessoas = None

    def criar_objeto(self, dados: dict) -> Pessoa:
        """
        Constrói um objeto Pessoa (ou subclasse) a partir de um dicionário.
        """
        return PessoaMapper.from_dict(dados)

    def extrair_dados_do_objeto(self, pessoa: Pessoa) -> dict:
        """
        Converte um objeto Pessoa para dicionário serializável.
        """
        return PessoaMapper.to_dict(pessoa)

    def tipo_de_id(self) -> str:
        """
        Define o campo de identificação único no JSON.
        """
        return "numero_documento"

    def listar_todos_objetos(self) -> list[Pessoa]:
        """
        Retorna todas as pessoas cadastradas, com uso de cache.
        """
        if self._cache_pessoas is not None:
            return self._cache_pessoas

        dados = self._ler_dados_do_json()
        self._cache_pessoas = [self.criar_objeto(d) for d in dados]
        return self._cache_pessoas

    def buscar_por_id(self, id_valor: str) -> Pessoa | None:
        """
        Retorna a pessoa com o documento informado, usando cache.
        """
        return next(
            (p for p in self.listar_todos_objetos() if str(p.get_numero_documento()) == str(id_valor)),
            None
        )

    def salvar_objeto(self, pessoa: Pessoa) -> None:
        """
        Salva uma nova pessoa e invalida o cache.
        """
        super().salvar_objeto(pessoa)
        self._cache_pessoas = None

    def atualizar_objeto(self, pessoa: Pessoa) -> bool:
        """
        Atualiza uma pessoa existente e invalida o cache.
        """
        atualizado = super().atualizar_objeto(pessoa)
        self._cache_pessoas = None
        return atualizado

    def deletar_objeto(self, id_valor: str) -> bool:
        """
        Remove uma pessoa pelo documento e invalida o cache.
        """
        deletado = super().deletar_objeto(id_valor)
        self._cache_pessoas = None
        return deletado