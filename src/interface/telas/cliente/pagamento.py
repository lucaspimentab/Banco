import flet as ft
from interface.componentes.notificador import Notificador
from app.servicos.servico_pagamento import ServicoPagamento

class TelaPagamento:
    def __init__(self, cliente):
        self.cliente = cliente
        self.servico = ServicoPagamento(cliente)
        self.notificador = Notificador()

        # Referências de campos
        self.cpf_ref = ft.Ref[ft.TextField]()
        self.valor_ref = ft.Ref[ft.TextField]()
        self.desc_ref = ft.Ref[ft.TextField]()

        self.view = self.criar_view()

    def criar_view(self):
        return ft.Column(
            controls=[
                ft.Text("💸 Realizar Pagamento", size=22, weight=ft.FontWeight.BOLD),
                ft.TextField(label="CPF do destinatário", ref=self.cpf_ref, hint_text="Somente números"),
                ft.TextField(label="Valor (R$)", ref=self.valor_ref, keyboard_type=ft.KeyboardType.NUMBER),
                ft.TextField(label="Descrição (opcional)", ref=self.desc_ref),
                ft.ElevatedButton("Pagar", on_click=self.realizar_pagamento),
                self.notificador.get_snackbar()
            ],
            spacing=15
        )

    def realizar_pagamento(self, e):
        dados = {
            "cpf_destino": self.cpf_ref.current.value,
            "valor": self.valor_ref.current.value,
            "descricao": self.desc_ref.current.value
        }

        resultado = self.servico.efetuar_pagamento(dados)

        if resultado["sucesso"]:
            self.notificador.sucesso(e.page, "✅ Pagamento realizado com sucesso!")
        else:
            self.notificador.erro(e.page, "\n".join(resultado["erros"]))
