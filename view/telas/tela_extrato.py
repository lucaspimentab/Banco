import flet as ft
from controller.conta_controller import ContaController
from view.components.mensagens import Notificador
from view.components.containers import CartaoResumo, CartaoTransacao
from view.components.identidade_visual import CORES, ESTILOS_TEXTO


class TelaExtrato:
    """
    Tela responsável por exibir o extrato das contas ativas do cliente.
    """

    def __init__(self, cliente):
        self.cliente = cliente
        self.notificador = Notificador()

        self.dropdown_ref = ft.Ref[ft.Dropdown]()
        self.lista_extrato = ft.Column(
            [],
            spacing=8,
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )

        self.view = self.criar_view()
        
    def criar_view(self) -> ft.Container:
        """Cria a interface completa da tela de extrato."""
        opcoes_contas = [
            ft.dropdown.Option(num)
            for num in ContaController.contas_ativas_para_dropdown(self.cliente)
        ]

        dropdown_conta = ft.Dropdown(
            label="Selecione uma conta",
            ref=self.dropdown_ref,
            width=300,
            options=opcoes_contas,
            on_change=self.atualizar_extrato,
        )

        conteudo = ft.Container(
            width=520,
            padding=25,
            bgcolor=CORES["fundo"],
            border_radius=16,
            shadow=ft.BoxShadow(blur_radius=20, color="#00000022", offset=ft.Offset(3, 3)),
            content=ft.Column(
                spacing=20,
                controls=[
                    ft.Row([
                        ft.Icon(
                            name=ft.Icons.RECEIPT_LONG,
                            size=28,
                            color=CORES["primaria"]
                        ),
                        ft.Text(
                            "Consulta de Extrato",
                            style=ESTILOS_TEXTO["titulo"]
                        )
                    ], alignment=ft.MainAxisAlignment.CENTER),

                    ft.Row([dropdown_conta], alignment=ft.MainAxisAlignment.CENTER),

                    ft.Container(
                        expand=True,
                        alignment=ft.alignment.center,
                        content=CartaoResumo(
                            titulo="Últimas transações",
                            conteudo=[
                                ft.Container(
                                    content=self.lista_extrato,
                                    expand=True
                                )
                            ],
                            expand=True,
                            padding=0,
                            sombra=False
                        )
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
            content=conteudo
        )


    def atualizar_extrato(self, e):
        """Atualiza o extrato da conta selecionada."""
        numero = self.dropdown_ref.current.value

        if not numero:
            self.notificador.erro(e.page, "Selecione uma conta.")
            return

        resultado, erro = ContaController.obter_extrato(numero)

        if erro:
            self.notificador.erro(e.page, erro)
            return

        _, conta = resultado
        historico = conta.get_historico()

        self.lista_extrato.controls.clear()

        transacoes_validas = [
            item for item in historico
            if "Recebido" in item or "Transferência de" in item
        ]

        if not transacoes_validas:
            self.lista_extrato.controls.append(
                ft.Text(
                    "Nenhuma transação encontrada.",
                    italic=True,
                    style=ESTILOS_TEXTO["normal"]
                )
            )
        else:
            for item in reversed(transacoes_validas[-10:]):
                self.lista_extrato.controls.append(CartaoTransacao(item))

        e.page.update()