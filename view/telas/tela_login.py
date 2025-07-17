import flet as ft
import asyncio

from view.components.campos import CampoCPF, CampoCNPJ, CampoSenha
from view.components.botoes import BotaoPrimario, BotaoSecundario
from view.components.mensagens import Notificador
from controller.auth_controller import AuthController
from view.components.identidade_visual import CORES, ESTILOS_TEXTO


class TelaLogin:
    """
    Classe responsável pela tela de login do sistema bancário, permitindo
    acesso ao usuário com CPF ou CNPJ e senha.
    """

    def __init__(self, on_login_sucesso=None, on_ir_cadastro=None):
        self.on_login_sucesso = on_login_sucesso
        self.on_ir_cadastro = on_ir_cadastro
        self.notificador = Notificador()

        self.tipo_ref = ft.Ref[ft.RadioGroup]()
        self.documento_container = ft.Ref[ft.Container]()

        self.campo_documento = CampoCPF()
        self.campo_senha = CampoSenha()

    def criar_view(self, page: ft.Page) -> ft.Container:
        """Cria a visualização completa da tela de login."""

        grupo_tipo = ft.RadioGroup(
            ref=self.tipo_ref,
            value="cpf",
            on_change=self.trocar_campo_documento,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Radio(label="CPF", value="cpf"),
                    ft.Radio(label="CNPJ", value="cnpj"),
                ]
            )
        )

        layout = ft.Container(
            width=420,
            padding=30,
            bgcolor=CORES["fundo"],
            border_radius=16,
            shadow=ft.BoxShadow(
                blur_radius=20,
                color="#00000022",
                spread_radius=2,
                offset=ft.Offset(3, 3)
            ),
            content=ft.Column(
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Row([
                        ft.Icon(name=ft.Icons.LOCK_OUTLINE, size=32, color=CORES["primaria"]),
                        ft.Text("Acesso ao sistema bancário", style=ESTILOS_TEXTO["titulo"])
                    ], alignment=ft.MainAxisAlignment.CENTER),

                    ft.Text("Tipo de documento", style=ESTILOS_TEXTO["subtitulo"]),
                    grupo_tipo,
                    ft.Container(ref=self.documento_container, content=self.campo_documento),
                    self.campo_senha,

                    ft.Row([
                        BotaoPrimario("Entrar", on_click=lambda e: page.run_task(self.on_login_click, e)),
                        BotaoSecundario("Criar conta", on_click=lambda e: self.on_ir_cadastro())
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                    self.notificador.get_snackbar()
                ]
            )
        )

        return ft.Container(
            alignment=ft.alignment.center,
            expand=True,
            bgcolor=CORES["secundaria"],
            content=layout
        )

    def trocar_campo_documento(self, e):
        """Alterna o campo de documento entre CPF e CNPJ conforme seleção."""
        tipo = self.tipo_ref.current.value
        self.campo_documento = CampoCPF() if tipo == "cpf" else CampoCNPJ()
        self.documento_container.current.content = self.campo_documento
        e.page.update()

    async def on_login_click(self, e):
        """Realiza autenticação e redireciona o usuário ao painel após login."""
        e.control.disabled = True
        e.page.update()

        spinner = ft.ProgressRing()
        e.page.overlay.append(spinner)
        e.page.update()

        documento = self.campo_documento.value.strip()
        senha = self.campo_senha.value.strip()

        resultado = AuthController.login(documento, senha)

        e.page.overlay.clear()
        e.page.update()

        if resultado["status"] != "sucesso":
            self.notificador.erro(e.page, resultado["mensagem"])
            e.control.disabled = False
            e.page.update()
            return

        await asyncio.sleep(0.2)

        if self.on_login_sucesso:
            self.on_login_sucesso(resultado["usuario_id"])