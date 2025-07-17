from abc import ABC, abstractmethod
import json
import os
from typing import List, Optional, TypeVar, Generic

T = TypeVar("T")  # Tipo genérico para entidades manipuladas pelo DAO


class DAO(ABC, Generic[T]):
    """
    Classe abstrata genérica para DAOs com persistência em arquivos JSON.
    Define a estrutura comum para salvar, buscar, atualizar e deletar entidades.
    """

    def __init__(self, arquivo_json: str):
        """
        Inicializa o DAO com o caminho do arquivo JSON de armazenamento.
        """
        self.arquivo_json = os.path.join("database", arquivo_json)
        self._cache_local = None  # Cache opcional de leitura

    @abstractmethod
    def criar_objeto(self, data: dict) -> T:
        """
        Converte um dicionário do JSON em uma instância da entidade.
        """
        pass

    @abstractmethod
    def extrair_dados_do_objeto(self, obj: T) -> dict:
        """
        Converte uma entidade em dicionário para persistência.
        """
        pass

    @abstractmethod
    def tipo_de_id(self) -> str:
        """
        Retorna o nome do campo usado como identificador único.
        """
        pass

    def _ler_dados_do_json(self) -> List[dict]:
        """
        Lê o conteúdo do JSON, retornando uma lista de dicionários.
        Retorna lista vazia se o arquivo não existir ou estiver corrompido.
        """
        try:
            with open(self.arquivo_json, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _salvar_no_arquivo_json(self, dados: List[dict]) -> None:
        """
        Salva uma lista de dicionários no arquivo JSON.
        """
        with open(self.arquivo_json, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4)

    def listar_todos_objetos(self) -> List[T]:
        """
        Retorna todas as entidades salvas no JSON.
        """
        dados = self._ler_dados_do_json()
        return [self.criar_objeto(item) for item in dados]

    def buscar_por_id(self, id_valor) -> Optional[T]:
        """
        Retorna a entidade correspondente ao identificador fornecido.
        """
        for item in self._ler_dados_do_json():
            if str(item.get(self.tipo_de_id())) == str(id_valor):
                return self.criar_objeto(item)
        return None

    def salvar_objeto(self, obj: T) -> None:
        """
        Salva um novo objeto no JSON, desde que não haja duplicação de ID.
        """
        dados = self._ler_dados_do_json()
        novo = self.extrair_dados_do_objeto(obj)
        chave = self.tipo_de_id()

        if any(item.get(chave) == novo[chave] for item in dados):
            raise ValueError(f"Objeto com {chave} = '{novo[chave]}' já existe.")

        dados.append(novo)
        self._salvar_no_arquivo_json(dados)

    def atualizar_objeto(self, obj: T) -> bool:
        """
        Atualiza um objeto existente com base em seu identificador.
        Retorna True se atualizado com sucesso, False se não encontrado.
        """
        dados = self._ler_dados_do_json()
        id_chave = self.tipo_de_id()
        novo_dado = self.extrair_dados_do_objeto(obj)
        id_valor = novo_dado[id_chave]

        for i, item in enumerate(dados):
            if item.get(id_chave) == id_valor:
                dados[i] = novo_dado
                self._salvar_no_arquivo_json(dados)
                return True

        return False

    def deletar_objeto(self, id_valor) -> bool:
        """
        Remove um objeto com o ID fornecido.
        Retorna True se a exclusão for bem-sucedida, False se não encontrado.
        """
        dados = self._ler_dados_do_json()
        novo_dados = [item for item in dados if item.get(self.tipo_de_id()) != id_valor]

        if len(novo_dados) == len(dados):
            return False

        self._salvar_no_arquivo_json(novo_dados)
        return True
