import flet as ft
from interface.componentes.campo_com_icone import CampoComIcone

class TelaLogin:
    def __init__(self, on_login_callback=None):
        self.on_login_callback = on_login_callback
        
        # Referências
        self.login_ref = ft.Ref[str]()
        self.senha_ref = ft.Ref[str]()

        self.view = self.criar_view()

    def criar_view(self):

        # Subitens da tela de login:
        titulo = ft.Text("Login", size=24, weight=ft.FontWeight.BOLD)
        login_row = CampoComIcone("person", "Usuário", ref_obj=self.login_ref)
        password_row = CampoComIcone("lock", "Senha", senha=True, ref_obj=self.senha_ref)
        login_button = ft.ElevatedButton("Entrar", on_click=self.on_login_click)
        register_link = ft.Text("Não tem uma conta? Cadastre-se", color=ft.Colors.BLUE_500)
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    titulo,
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
        print("Senha:", self.senha_input.value)
        if self.on_login_callback:
            self.on_login_callback(self.login_input.value, self.senha_input.value)
