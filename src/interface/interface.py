import flet as ft
from interface.componentes.login import TelaLogin

def main(page: ft.Page):
    page.title = "Sistema Bancário"
    page.bgcolor = ft.Colors.WHITE
    tela_login = TelaLogin()
    page.add(tela_login.view)

if __name__ == "__main__":
    ft.app(target=main)