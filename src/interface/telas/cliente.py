import flet as ft

class TelaCliente:
    def __init__(self, cliente, on_voltar):
        self.cliente = cliente
        self.on_voltar = on_voltar
        self.view = self.criar_view()

    def criar_view(self):
        titulo = ft.Text(f"Bem-vindo(a), {self.cliente.nome}", size=22, weight=ft.FontWeight.BOLD)

        dados = ft.Text(
            f"CPF: {self.cliente.cpf}\n"
            f"Email: {self.cliente.email}\n"
            f"Telefone: {self.cliente.telefone}\n"
            f"Contas: {len(self.cliente.contas)} conta(s) ativa(s)",
            size=16
        )

        botao_voltar = ft.ElevatedButton(
            text="Sair",
            on_click=self.on_voltar
        )

        return ft.Container(
            content=ft.Column(
                controls=[titulo, dados, botao_voltar],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            alignment=ft.alignment.center,
            expand=True
        )
