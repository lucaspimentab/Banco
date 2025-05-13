import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import flet as ft
from interface.telas.cadastro import TelaCadastro
from interface.telas.login import TelaLogin
from interface.telas.cliente import TelaCliente
from app.banco import Banco

banco = Banco()
banco.carregar_dados("data/contas.json")

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
        if not cliente:
            tela_login.snackbar.content.value = "CPF não encontrado. Verifique os dados."
            tela_login.snackbar.bgcolor = ft.Colors.RED_600
            tela_login.snackbar.open = True
            page.snack_bar = tela_login.snackbar
            page.update()
            return

        if not cliente.verificar_senha(senha):
            tela_login.snackbar.content.value = "Senha incorreta. Tente novamente."
            tela_login.snackbar.bgcolor = ft.Colors.RED_600
            tela_login.snackbar.open = True
            page.snack_bar = tela_login.snackbar
            page.update()
            return

        # Login bem-sucedido → mostrar tela do cliente
        tela_cliente = TelaCliente(cliente, on_voltar_cliente)
        page.controls.clear()
        page.add(tela_cliente.view)

    def cadastro_realizado(dados):
        endereco_split = dados["endereco"].split(",")
        if len(endereco_split) < 2:
            tela_cadastro.mostrar_erro(page, "Endereço deve conter CEP e número separados por vírgula.")
            return

        cep = endereco_split[0].strip()
        numero = endereco_split[1].strip()

        cliente_existente = banco.buscar_cliente_por_cpf(dados["cpf"])
        mensagens = []

        if cliente_existente:
            if cliente_existente.nome.strip() != dados["nome"].strip():
                mensagens.append("Nome não confere com o já cadastrado.")
            if cliente_existente.email.strip() != dados["email"].strip():
                mensagens.append("Email não confere com o já cadastrado.")
            if cliente_existente.telefone.strip() != dados["telefone"].strip():
                mensagens.append("Telefone não confere com o já cadastrado.")
            if cliente_existente.senha.strip() != dados["senha"].strip():
                mensagens.append("Senha não confere com o já cadastrado.")
            if cliente_existente.data_nascimento.strip() != dados["data_nascimento"].strip():
                mensagens.append("Data de nascimento não confere com o já cadastrado.")

        if mensagens:
            tela_cadastro.mostrar_erro(page, "\n".join(mensagens))
            return

        resp = banco.abrir_conta(
            tipo_conta=dados["tipo_conta"],
            nome=dados["nome"],
            cpf=dados["cpf"],
            telefone=dados["telefone"],
            email=dados["email"],
            cep=cep,
            numero_endereco=numero,
            senha=dados["senha"],
            data_nascimento=dados["data_nascimento"]
        )

        if resp and resp["sucesso"]:
            banco.salvar_dados("data/contas.json")
            page.session.set("mensagem_sucesso", "✅ Conta criada com sucesso!")
            ir_para_login()
        else:
            if resp and "mensagens" in resp:
                tela_cadastro.mostrar_erro(page, "\n".join(resp["mensagens"]))

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