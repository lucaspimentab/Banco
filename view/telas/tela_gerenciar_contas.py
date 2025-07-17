import flet as ft
import uuid
from controller.conta_controller import ContaController
from view.components.mensagens import Notificador
from view.components.identidade_visual import CORES, ESTILOS_TEXTO


class TelaGerenciarContas:
    """
    Tela para gerenciamento das contas do cliente,
    permitindo ativar, reativar ou encerrar contas existentes.
    """

    def __init__(self, cliente):
        self.cliente = cliente
        self.notificador = Notificador()

        self.conta_dropdown = ft.Ref[ft.Dropdown]()
        self.senha_field = ft.Ref[ft.TextField]()
        self.botao_acao = ft.Ref[ft.ElevatedButton]()
        self.dropdown_control = None

        self.view = self.criar_view()
        self.recarregar_lista_contas()

    def criar_view(self) -> ft.Container:
        """Cria o layout completo da tela para gerenciamento de contas."""
        self.dropdown_control = ft.Dropdown(
            ref=self.conta_dropdown,
            key=str(uuid.uuid4()),
            label="Selecione uma conta",
            width=400,
            on_change=self.alternar_botao_acao
        )

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
                        ft.Icon(name=ft.Icons.MANAGE_ACCOUNTS, size=28, color=CORES["primaria"]),
                        ft.Text("Gerenciar Contas", style=ESTILOS_TEXTO["titulo"])
                    ], alignment=ft.MainAxisAlignment.CENTER),

                    self.dropdown_control,
                    ft.TextField(ref=self.senha_field, label="Confirme sua senha", password=True),
                    ft.ElevatedButton(
                        "Ativar / Reativar",
                        ref=self.botao_acao,
                        on_click=self.executar_acao,
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

    def recarregar_lista_contas(self):
        """Recarrega as contas disponíveis para seleção no dropdown."""
        contas = ContaController.listar_contas(self.cliente.numero_documento)

        if not contas:
            self.dropdown_control.options = []
            self.dropdown_control.label = "Nenhuma conta encontrada"
            return

        opcoes = []
        for conta in contas:
            estado = "Ativa" if conta.get_estado_da_conta() else "Inativa"
            opcoes.append(
                ft.dropdown.Option(
                    key=str(conta.get_numero_conta()),
                    text=f"{conta.__class__.__name__} - Nº {conta.get_numero_conta()} - {estado}"
                )
            )

        self.dropdown_control.options = opcoes
        self.dropdown_control.value = None

        if self.senha_field.current:
            self.senha_field.current.value = ""

    def alternar_botao_acao(self, e):
        """Alterna texto e cor do botão com base no estado atual da conta selecionada."""
        numero = self.conta_dropdown.current.value
        conta = self._buscar_conta(numero)

        if not conta or not self.botao_acao.current:
            return

        if conta.get_estado_da_conta():
            self.botao_acao.current.text = "Encerrar conta"
            self.botao_acao.current.bgcolor = CORES["erro"]
        else:
            self.botao_acao.current.text = "Reativar conta"
            self.botao_acao.current.bgcolor = CORES["sucesso"]

        e.page.update()

    def executar_acao(self, e):
        """Executa ativação, reativação ou encerramento da conta selecionada após validação da senha."""
        numero = self.conta_dropdown.current.value
        senha = self.senha_field.current.value

        if not numero or not senha:
            self.notificador.erro(e.page, "Selecione uma conta e digite a senha.")
            return

        conta = self._buscar_conta(numero)
        if not conta:
            self.notificador.erro(e.page, "Conta não encontrada.")
            return

        if not self.cliente.verificar_senha(senha):
            self.notificador.erro(e.page, "Senha incorreta.")
            return

        if conta.get_estado_da_conta():
            resultado = ContaController.excluir_conta(self.cliente.numero_documento, numero, senha)
        else:
            resultado = ContaController.reativar_conta(self.cliente.numero_documento, numero, senha)

        if resultado["sucesso"]:
            self.notificador.sucesso(e.page, resultado["mensagem"])
            self.recarregar_lista_contas()
        else:
            self.notificador.erro(e.page, resultado["mensagem"])

        # Reset visual do dropdown após ação executada
        self.dropdown_control.key = str(uuid.uuid4())
        self.dropdown_control.value = None
        self.dropdown_control.update()

        # Reset visual do botão e campo senha
        self.botao_acao.current.text = "Ativar / Reativar"
        self.botao_acao.current.bgcolor = CORES["primaria"]

        if self.senha_field.current:
            self.senha_field.current.value = ""

        e.page.update()

    def _buscar_conta(self, numero: str):
        """Busca e retorna a conta correspondente ao número fornecido."""
        contas = ContaController.listar_contas(self.cliente.numero_documento)
        for conta in contas:
            if str(conta.get_numero_conta()) == str(numero):
                return conta
        return None