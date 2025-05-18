import flet as ft
from interface.componentes.notificador import Notificador
from app.servicos.servico_pagamento import ServicoPagamento

class TelaPagamento:
    def __init__(self, banco, cliente):
        self.cliente = cliente
        self.servico = ServicoPagamento(banco, cliente)
        self.notificador = Notificador()

        # Referências de campos
        self.conta_ref = ft.Ref[ft.Dropdown]()
        self.cpf_ref = ft.Ref[ft.TextField]()
        self.valor_ref = ft.Ref[ft.TextField]()
        self.desc_ref = ft.Ref[ft.TextField]()

        self.view = self.criar_view()

    def criar_view(self):
        # Gera opções de contas ativas
        opcoes_contas = [
            ft.dropdown.Option(str(conta.numero_conta)) for conta in self.cliente.contas if conta.ativa
        ]

        return ft.Column(
            controls=[
                ft.Text("💸 Realizar Pagamento", size=22, weight=ft.FontWeight.BOLD),
                ft.Dropdown(
                    label="Escolha a conta de origem",
                    ref=self.conta_ref,
                    options=opcoes_contas,
                    hint_text="Selecione a conta",
                    width=250
                ),
                ft.TextField(label="CPF do destinatário", ref=self.cpf_ref, hint_text="Somente números"),
                ft.TextField(label="Valor (R$)", ref=self.valor_ref, keyboard_type=ft.KeyboardType.NUMBER),
                ft.TextField(label="Descrição (opcional)", ref=self.desc_ref),
                ft.ElevatedButton("Pagar", on_click=self.realizar_pagamento),
                self.notificador.get_snackbar()
            ],
            spacing=15
        )

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
            self.notificador.sucesso(e.page, resultado["mensagem"])
        else:
            self.notificador.erro(e.page, "\n".join(resultado["erros"]))
