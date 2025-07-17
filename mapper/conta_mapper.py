from model.conta import Conta
from model.conta_corrente import ContaCorrente
from model.conta_poupanca import ContaPoupanca
from utils.constantes import TIPO_CCORRENTE, TIPO_CPOUPANCA


class ContaMapper:
    """
    Classe responsável por converter objetos Conta (e subclasses)
    para dicionários e vice-versa, com validação de tipo.
    """

    @staticmethod
    def from_dict(dados: dict) -> Conta:
        """
        Constrói uma instância de ContaCorrente ou ContaPoupanca a partir de um dicionário.

        Raises:
            ValueError: Se campos obrigatórios estiverem ausentes ou tipo for inválido.
        """
        campos_obrigatorios = ["tipo", "numero", "saldo", "historico", "ativa"]
        campos_faltantes = [campo for campo in campos_obrigatorios if campo not in dados]
        if campos_faltantes:
            raise ValueError(f"Campos obrigatórios ausentes: {', '.join(campos_faltantes)}")

        tipo = dados["tipo"]
        numero = int(dados["numero"])
        saldo = float(dados["saldo"])
        historico = dados["historico"]
        ativa = dados["ativa"]

        if tipo == TIPO_CCORRENTE:
            return ContaCorrente(numero, saldo, historico, ativa)
        elif tipo == TIPO_CPOUPANCA:
            return ContaPoupanca(numero, saldo, historico, ativa)
        else:
            raise ValueError(f"Tipo de conta desconhecido: {tipo}")

    @staticmethod
    def to_dict(conta: Conta) -> dict:
        """
        Converte uma instância de Conta em um dicionário serializável.
        """
        tipo = TIPO_CCORRENTE if isinstance(conta, ContaCorrente) else TIPO_CPOUPANCA

        return {
            "numero": str(conta.get_numero_conta()),
            "saldo": conta.get_saldo(),
            "historico": conta.get_historico(),
            "ativa": conta.get_estado_da_conta(),
            "tipo": tipo
        }