import flet as ft
from interface.componentes.campo_com_icone import CampoComIcone

class TelaLogin:
    def __init__(self, on_login_callback=None, on_ir_cadastro=None):
        self.on_login_callback = on_login_callback
        self.on_ir_cadastro = on_ir_cadastro
        
        # Referências
        self.login_ref = ft.Ref[str]()
        self.senha_ref = ft.Ref[str]()

        self.view = self.criar_view()

    def criar_view(self):

        #1
        titulo = ft.Text(
            "Login", 
            size=24, 
            weight=ft.FontWeight.BOLD
        )

        #2
        login_row = CampoComIcone(
            "person", 
            "Usuário", 
            ref_obj=self.login_ref
        )

        #3
        password_row = CampoComIcone(
            "lock", 
            "Senha", 
            senha=True, 
            ref_obj=self.senha_ref
        )
        
        #4
        login_button = ft.ElevatedButton(
            "Entrar", 
            on_click=self.on_login_click
        )
        
        #5
        register_link = ft.TextButton(
            "Não tem uma conta? Cadastre-se", 
            style=ft.ButtonStyle(color=ft.Colors.BLUE_500),
            on_click=self.on_ir_cadastro
        )
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    titulo,        #1
                    login_row,     #2
                    password_row,  #3
                    login_button,  #4
                    register_link, #5
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
