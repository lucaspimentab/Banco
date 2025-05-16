import flet as ft
from interface.telas.cliente.perfil import TelaPerfil
from interface.telas.cliente.pagamento import TelaPagamento
from interface.telas.cliente.extrato import TelaExtrato

class TelaCliente:
    def __init__(self, cliente, on_logout):
        self.cliente = cliente
        self.on_logout = on_logout

        # Referência da área de conteúdo central
        self.conteudo_ref = ft.Ref[ft.Container]()
        self.view = self.criar_view()

    def criar_view(self):
        sidebar = ft.Container(
            width=250,
            bgcolor=ft.colors.GREY_200,
            padding=20,
            content=ft.Column(
                controls=[
                    ft.Text(f"👤 {self.cliente.nome}", size=18, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    ft.TextButton("📄 Perfil", on_click=self.mostrar_perfil),
                    ft.TextButton("💸 Fazer Pagamento", on_click=self.mostrar_pagamento),
                    ft.TextButton("📊 Saldo / Extrato", on_click=self.mostrar_extrato),
                    ft.TextButton("🚪 Sair", on_click=self.on_logout),
                ],
                spacing=15
            )
        )

        conteudo_inicial = ft.Container(
            ref=self.conteudo_ref,
            expand=True,
            padding=30,
            content=ft.Text("Bem-vindo ao seu painel!", size=20)
        )

        layout = ft.Row(
            controls=[sidebar, conteudo_inicial],
            expand=True
        )

        return layout

    def mostrar_perfil(self, e=None):
        self._mostrar(TelaPerfil(self.cliente), e)

    def mostrar_pagamento(self, e=None):
        self._mostrar(TelaPagamento(self.cliente), e)

    def mostrar_extrato(self, e=None):
        self._mostrar(TelaExtrato(self.cliente), e)

    def _mostrar(self, tela, e=None):
        self.conteudo_ref.current.content = tela.view
        if e: e.page.update()