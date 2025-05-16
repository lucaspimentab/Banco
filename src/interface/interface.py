import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import flet as ft
import asyncio
from interface.telas.cadastro import TelaCadastro
from interface.telas.login import TelaLogin
from interface.telas.cliente import TelaCliente
from app.banco import Banco
from app.servicos.servico_cadastro import ServicoCadastro

banco = Banco()
banco.carregar_dados("data/contas.json")
servico_cadastro = ServicoCadastro(banco)

def main(page: ft.Page):
    def ir_para_login(e=None):
        page.controls.clear()
        page.add(tela_login.criar_view(page))

    def ir_para_cadastro(e=None):
        page.controls.clear()
        page.add(tela_cadastro.view)

    def on_voltar_cliente(e=None):
        page.controls.clear()
        page.add(tela_login.criar_view(page))

    def login_realizado(cpf, senha):
        cliente = banco.buscar_cliente_por_cpf(cpf)

        # Possíveis erros:
        if not cliente:
            tela_login.notificador.erro(page, "CPF não encontrado. Verifique os dados.")
            return

        if not cliente.verificar_senha(senha):
            tela_login.notificador.erro(page, "Senha incorreta. Tente novamente.")
            return

        # Login bem-sucedido, ir para tela do cliente:
        tela_cliente = TelaCliente(cliente, on_voltar_cliente)
        page.controls.clear()
        page.add(tela_cliente.view)

    async def cadastro_realizado(dados):
        resultado = servico_cadastro.realizar_cadastro(dados)

        if resultado["sucesso"]:
            banco.salvar_dados("data/contas.json")
            tela_cadastro.notificador.sucesso(page, "✅ Conta criada com sucesso!")
            page.update()

            await asyncio.sleep(1)
            ir_para_login()
        else:
            tela_cadastro.notificador.erro(page, "\n".join(resultado["erros"]))
            page.update()

    tela_login = TelaLogin(
        on_login_callback=login_realizado,
        on_ir_cadastro=ir_para_cadastro
    )

    tela_cadastro = TelaCadastro(
        on_cadastro_callback=cadastro_realizado,
        on_voltar_login=ir_para_login
    )

    page.title = "Sistema Bancário"
    page.bgcolor = ft.Colors.WHITE
    page.add(tela_login.criar_view(page))