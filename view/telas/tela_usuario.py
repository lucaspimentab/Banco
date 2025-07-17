import flet as ft
from controller.auth_controller import AuthController
from view.telas.tela_perfil import TelaPerfil
from view.telas.tela_pagamento import TelaPagamento
from view.telas.tela_extrato import TelaExtrato


class TelaUsuario:
    """
    Classe responsável por criar e gerenciar a interface principal do usuário após login.
    Permite acesso às funcionalidades: perfil, pagamentos, extrato, criação e gerenciamento de contas e edição de dados pessoais.
    """

    def __init__(self, banco, cliente, on_logout, subrota: str = None, resetar: bool = False):
        self.banco = banco
        self.cliente = cliente
        self.on_logout = on_logout
        self.subrota = subrota or "perfil"
        self.resetar = resetar
        self.conteudo_ref = ft.Ref[ft.Container]()
        self.view = self.criar_view()

        # Inicializa com a tela padrão (ou passada na subrota)
        self.carregar_tela(self.subrota)

    def criar_view(self) -> ft.Container:
        """Cria o container principal que inclui a barra lateral e a área de conteúdo."""
        return ft.Container(
            alignment=ft.alignment.center,
            expand=True,
            content=ft.Row(
                expand=True,
                controls=[
                    self.criar_sidebar(),
                    ft.Container(
                        ref=self.conteudo_ref,
                        expand=True,
                        padding=30,
                        content=ft.Text("Bem-vindo ao sistema bancário", size=20)
                    )
                ]
            )
        )

    def criar_sidebar(self) -> ft.Container:
        """Cria a barra lateral com botões para navegação entre funcionalidades."""
        return ft.Container(
            width=240,
            bgcolor=ft.Colors.GREY_100,
            padding=20,
            content=ft.Column(
                spacing=15,
                controls=[
                    ft.Text(self.cliente.pessoa.get_nome(), size=18, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    ft.TextButton("Perfil", icon=ft.Icons.PERSON, on_click=lambda e: self.carregar_tela("perfil", e)),
                    ft.TextButton("Pagamentos", icon=ft.Icons.PAYMENTS, on_click=lambda e: self.carregar_tela("pagamento", e)),
                    ft.TextButton("Extrato", icon=ft.Icons.RECEIPT_LONG, on_click=lambda e: self.carregar_tela("extrato", e)),
                    ft.TextButton("Criar conta", icon=ft.Icons.ACCOUNT_BALANCE, on_click=lambda e: self.carregar_tela("criar_conta", e)),
                    ft.TextButton("Gerenciar contas", icon=ft.Icons.MANAGE_ACCOUNTS, on_click=lambda e: self.carregar_tela("gerenciar_contas", e)),
                    ft.TextButton("Alterar dados", icon=ft.Icons.EDIT, on_click=lambda e: self.carregar_tela("editar", e)),
                    ft.TextButton("Sair", icon=ft.Icons.LOGOUT, on_click=self.on_logout),
                ]
            )
        )

    def carregar_tela(self, rota: str, e=None):
        """
        Atualiza dinamicamente o conteúdo principal da tela baseado na rota selecionada.

        Args:
            rota (str): Nome da funcionalidade/tela para exibir.
            e (Event): Evento do Flet que acionou essa troca, opcional para atualização visual.
        """
        # Usa sempre cliente mais recente da sessão para evitar consultas desnecessárias
        cliente_sessao = AuthController.sessao_ativa.get(self.cliente.numero_documento)
        if cliente_sessao:
            self.cliente = cliente_sessao

        # Seleciona qual tela carregar com base na rota passada
        match rota:
            case "perfil":
                tela = TelaPerfil(self.cliente)

            case "pagamento":
                tela = TelaPagamento(self.banco, self.cliente)

            case "extrato":
                tela = TelaExtrato(self.cliente)

            case "criar_conta":
                from view.telas.tela_criar_conta import TelaCriarConta
                tela = TelaCriarConta(self.cliente)

            case "gerenciar_contas":
                from view.telas.tela_gerenciar_contas import TelaGerenciarContas
                tela = TelaGerenciarContas(self.cliente)

            case "editar":
                from view.telas.tela_editar_cliente import TelaEditarCliente
                tela = TelaEditarCliente(self.cliente)

            case _:
                tela = None

        # Define a nova tela ou uma mensagem padrão caso não exista
        self.conteudo_ref.current.content = tela.view if tela else ft.Text("Tela não encontrada.")

        if e and e.page:
            e.page.update()