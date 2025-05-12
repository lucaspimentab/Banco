import flet as ft
from interface.componentes.login import TelaLogin
from interface.componentes.cadastro import TelaCadastro

def main(page: ft.Page):
    page.title = "Sistema Bancário"
    page.bgcolor = ft.Colors.WHITE
    tela_login = TelaLogin()
    tela_cadastro = TelaCadastro()

    #page.add(tela_login.view)
    page.add(tela_cadastro.view)

if __name__ == "__main__":
    ft.app(target=main)