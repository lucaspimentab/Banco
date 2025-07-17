import requests
from utils.validadores.validar_pessoa import ValidarPessoa as Validar

class API():
    """
    Classe utilitária responsável por consultar e compor endereços a partir de CEPs,
    utilizando a API pública ViaCEP, com cache local para evitar múltiplas requisições.
    """

    _cache_cep = {}  # Cache em memória por execução

    @staticmethod
    def buscar_endereco_por_cep(cep: str, numero: str) -> str:
        """
        Consulta o endereço completo a partir de um CEP e número do imóvel,
        utilizando a API pública ViaCEP. Usa cache local para evitar múltiplas chamadas repetidas.
        """
        Validar.cep(cep)
        Validar.numero_endereco(numero)

        cep_numerico = ''.join(filter(str.isdigit, cep))  # Apenas os dígitos

        if cep_numerico in API._cache_cep:
            data = API._cache_cep[cep_numerico]
        else:
            url = f"https://viacep.com.br/ws/{cep_numerico}/json/"
            response = requests.get(url)

            if response.status_code != 200:
                raise ValueError("Erro ao buscar o endereço. Tente novamente mais tarde.")

            data = response.json()
            if "erro" in data:
                raise ValueError("CEP não encontrado. Verifique se está digitado corretamente.")

            API._cache_cep[cep_numerico] = data  # Armazena no cache

        logradouro = data["logradouro"]
        bairro     = data["bairro"]
        localidade = data["localidade"]
        uf         = data["uf"]

        return f"{logradouro}, {numero} - {bairro}, {localidade} - {uf}, {cep_numerico}"
