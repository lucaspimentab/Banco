import flet as ft
from interface.componentes.notificador import Notificador
from app.servicos.servico_pagamento import ServicoPagamento
from config.caminhos import CAMINHO_DADOS_JSON

class TelaPagamento:
    def realizar_pagamento(self, e):
        numero_conta = self.conta_ref.current.value
        if not numero_conta:
            self.notificador.erro(e.page, "⚠️ Selecione uma conta de origem.")
            return

        conta_origem = self.cliente.buscar_conta(int(numero_conta))
        if not conta_origem or not conta_origem.ativa:
            self.notificador.erro(e.page, "Conta inválida ou inativa.")
            return

        # Monta o dicionário com dados
        dados = {
            "cpf_destino": self.cpf_ref.current.value,
            "valor": self.valor_ref.current.value,
            "descricao": self.desc_ref.current.value,
            "conta_origem": conta_origem
        }

        resultado = self.servico.efetuar_pagamento(dados)

        if resultado["sucesso"]:
            self.servico.banco.salvar_dados(CAMINHO_DADOS_JSON)
            self.notificador.sucesso(e.page, resultado["mensagem"])
        else:
            self.notificador.erro(e.page, "\n".join(resultado["erros"]))
