import flet as ft
from view.components.mensagens import Notificador
from dao.cliente_dao import ClienteDAO
from dao.pessoa_dao import PessoaDAO
from view.components.identidade_visual import CORES, ESTILOS_TEXTO


class TelaEditarCliente:
    """
    Tela responsável por permitir ao cliente atualizar seu email, telefone e senha.
    Requer confirmação com a senha atual para aplicar alterações.
    """

    def __init__(self, cliente):
        self.cliente = cliente
        self.notificador = Notificador()

        self.email_field = ft.Ref[ft.TextField]()
        self.telefone_field = ft.Ref[ft.TextField]()
        self.senha_atual_field = ft.Ref[ft.TextField]()
        self.nova_senha_field = ft.Ref[ft.TextField]()

        self.view = self.criar_view()

    def criar_view(self) -> ft.Container:
        """Cria o layout da tela de edição de dados do cliente."""
        layout = ft.Container(
            width=500,
            padding=25,
            bgcolor=CORES["fundo"],
            border_radius=16,
            shadow=ft.BoxShadow(blur_radius=20, color="#00000022", offset=ft.Offset(3, 3)),
            content=ft.Column(
                spacing=20,
                controls=[
                    ft.Row([
                        ft.Icon(name=ft.Icons.EDIT, size=28, color=CORES["primaria"]),
                        ft.Text("Alterar Dados do Cliente", style=ESTILOS_TEXTO["titulo"])
                    ], alignment=ft.MainAxisAlignment.CENTER),

                    ft.TextField(
                        ref=self.email_field,
                        label="Email",
                        value=self.cliente.pessoa.get_email()
                    ),
                    ft.TextField(
                        ref=self.telefone_field,
                        label="Telefone",
                        value=self.cliente.pessoa.get_telefone()
                    ),

                    ft.Divider(),

                    ft.Text(
                        "Para confirmar as alterações, digite sua senha atual:",
                        size=12,
                        italic=True,
                        color=CORES["texto"]
                    ),
                    ft.TextField(
                        ref=self.senha_atual_field,
                        label="Senha atual",
                        password=True,
                        can_reveal_password=True
                    ),
                    ft.TextField(
                        ref=self.nova_senha_field,
                        label="Nova senha (preencha se quiser trocar)",
                        password=True,
                        can_reveal_password=True
                    ),

                    ft.ElevatedButton(
                        "Salvar alterações",
                        on_click=self.salvar_dados,
                        bgcolor=CORES["primaria"],
                        color=CORES["icone_sidebar"]
                    ),
                    self.notificador.get_snackbar()
                ]
            )
        )

        return ft.Container(
            alignment=ft.alignment.top_center,
            expand=True,
            bgcolor=CORES["secundaria"],
            padding=30,
            content=layout
        )

    def salvar_dados(self, e):
        """Valida a senha e atualiza os dados do cliente no sistema."""
        page = e.page

        email = self.email_field.current.value.strip()
        telefone = self.telefone_field.current.value.strip()
        senha_atual = self.senha_atual_field.current.value.strip()
        nova_senha = self.nova_senha_field.current.value.strip()

        if not senha_atual:
            self.notificador.erro(page, "Digite sua senha atual para confirmar as alterações.")
            return

        if not self.cliente.verificar_senha(senha_atual):
            self.notificador.erro(page, "Senha atual incorreta.")
            return

        try:
            self.cliente.pessoa.set_email(email)
            self.cliente.pessoa.set_telefone(telefone)

            if nova_senha:
                self.cliente.alterar_senha(senha_atual, nova_senha)

            ClienteDAO().atualizar_objeto(self.cliente)
            PessoaDAO().atualizar_objeto(self.cliente.pessoa)

            # Limpa os campos de senha após atualização
            self.senha_atual_field.current.value = ""
            self.nova_senha_field.current.value = ""
            page.update()

            self.notificador.sucesso(page, "Dados atualizados com sucesso!")
        except Exception as err:
            self.notificador.erro(page, str(err))