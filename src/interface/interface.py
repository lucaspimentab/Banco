import flet as ft
from interface.telas.login import TelaLogin
from interface.telas.cadastro import TelaCadastro

def main(page: ft.Page):
    def ir_para_login(e=None):
        page.controls.clear()
        page.add(tela_login.view)

    def ir_para_cadastro(e=None):
        page.controls.clear()
        page.add(tela_cadastro.view)

    def login_realizado(usuario, senha):
        print("Login com:", usuario, senha) # Remover isso depois
        # Colocar ir_para_principal(), por exemplo

    def cadastro_realizado(dados):
        print("Cadastrado:", dados)
        # Chamar a função de salvar no banco de dados
        ir_para_login()

    # Cria as telas e passa os callbacks certos
    tela_login = TelaLogin(
        on_login_callback = login_realizado,
        on_ir_cadastro = ir_para_cadastro
    )

    tela_cadastro = TelaCadastro(
        on_cadastro_callback = cadastro_realizado,
        on_voltar_login = ir_para_login
    )

    page.title = "Sistema Bancário"
    page.bgcolor = ft.Colors.WHITE
    page.add(tela_login.view)  # Começa com login
