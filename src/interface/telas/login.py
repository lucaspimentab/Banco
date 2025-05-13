import flet as ft
from interface.componentes.campo_com_icone import CampoComIcone

class TelaLogin:
    def __init__(self, on_login_callback=None, on_ir_cadastro=None):
        self.on_login_callback = on_login_callback
        self.on_ir_cadastro = on_ir_cadastro

        self.cpf_ref = ft.Ref[str]()
        self.senha_ref = ft.Ref[str]()
        self.snackbar = ft.SnackBar(ft.Text(""))

    def criar_view(self, page):
        msg = page.session.get("mensagem_sucesso")
        if msg:
            self.snackbar = ft.SnackBar(
                content=ft.Text(msg),
                bgcolor=ft.Colors.GREEN_600,
                show_close_icon=True,
                duration=3000
            )
            page.snack_bar = self.snackbar
            self.snackbar.open = True
            page.session.set("mensagem_sucesso", "")
            page.update()

        titulo = ft.Text("Login", size=24, weight=ft.FontWeight.BOLD)

        cpf_row = CampoComIcone(
            "badge",
            "CPF",
            ref_obj=self.cpf_ref,
            hint_text="Digite seu CPF (somente números)"
        )

        senha_row = CampoComIcone(
            "lock",
            "Senha",
            senha=True,
            ref_obj=self.senha_ref
        )

        login_button = ft.ElevatedButton("Entrar", on_click=self.on_login_click)

        register_link = ft.TextButton(
            "Não tem uma conta? Cadastre-se",
            style=ft.ButtonStyle(color=ft.Colors.BLUE_500),
            on_click=self.on_ir_cadastro
        )

        return ft.Container(
            content=ft.Column(
                controls=[
                    titulo,
                    cpf_row,
                    senha_row,
                    login_button,
                    register_link,
                    self.snackbar
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
            expand=True
        )

    def mostrar_erro(self, page, mensagem):
        self.snackbar.content.value = mensagem
        self.snackbar.bgcolor = ft.Colors.RED_600
        self.snackbar.open = True
        page.snack_bar = self.snackbar
        page.update()

    def on_login_click(self, e):
        page = e.page
        cpf = self.cpf_ref.current.value.strip()
        senha = self.senha_ref.current.value.strip()

        if not cpf or not cpf.isdigit() or len(cpf) != 11:
            self.mostrar_erro(page, "CPF inválido. Digite exatamente 11 números.")
            return

        if not senha:
            self.mostrar_erro(page, "Digite a senha.")
            return

        if self.on_login_callback:
            self.on_login_callback(cpf, senha)