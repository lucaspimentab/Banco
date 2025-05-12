import flet as ft

class TelaLogin:
    def __init__(self, on_login_callback=None):
        self.on_login_callback = on_login_callback
        self.view = self.criar_view()

    def criar_view(self):
        login_text = ft.Text("Login", size=24, weight=ft.FontWeight.BOLD)

        login_row = ft.Row(
            controls=[
                ft.Icon(ft.Icons.PERSON),
                ft.TextField(label="Usuário", autofocus=True, ref=ft.Ref[str]())
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

        password_row = ft.Row(
            controls=[
                ft.Icon(ft.Icons.LOCK),
                ft.TextField(label="Senha", password=True, can_reveal_password=True, ref=ft.Ref[str]())
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

        login_button = ft.ElevatedButton("Entrar", on_click=self.on_login_click)
        register_link = ft.Text("Não tem uma conta? Cadastre-se", color=ft.Colors.BLUE_500)

        self.login_input = login_row.controls[1]
        self.password_input = password_row.controls[1]

        return ft.Container(
            content=ft.Column(
                controls=[
                    login_text,
                    login_row,
                    password_row,
                    login_button,
                    register_link,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
            expand=True
        )

    def on_login_click(self, e):
        print("Usuário:", self.login_input.value)
        print("Senha:", self.password_input.value)
        if self.on_login_callback:
            self.on_login_callback(self.login_input.value, self.password_input.value)
