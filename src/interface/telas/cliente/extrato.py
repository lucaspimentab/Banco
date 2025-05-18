import flet as ft
from interface.componentes.notificador import Notificador
from app.servicos.servico_extrato import ServicoExtrato

class TelaExtrato:
    def __init__(self, cliente):
        """
        Tela que exibe o extrato e saldo de uma conta específica do cliente.

        Parâmetro:
        - cliente: Instância do Cliente logado.
        """
        self.cliente = cliente
        self.servico = ServicoExtrato(cliente)
        self.notificador = Notificador()

        self.dropdown_ref = ft.Ref[ft.Dropdown]()
        self.saldo_text = ft.Text()
        self.lista_extrato = ft.Column([], spacing=8, scroll=ft.ScrollMode.AUTO)

        self.view = self.criar_view()

    def criar_view(self):
        """
        Cria a interface da tela com dropdown para escolha de conta, saldo e extrato.

        Retorna:
        - ft.Container: Interface da tela.
        """
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("💰 Saldo e Extrato", size=22, weight=ft.FontWeight.BOLD),

                    # Dropdown para escolha da conta
                    ft.Dropdown(
                        label="Escolha uma conta",
                        ref=self.dropdown_ref,
                        options=[
                            ft.dropdown.Option(str(conta.numero_conta))
                            for conta in self.cliente.contas if conta.ativa
                        ],
                        on_change=self.atualizar_extrato,
                    ),

                    # Texto com o saldo da conta selecionada
                    self.saldo_text,
                    ft.Divider(),

                    # Lista com transações
                    ft.Text("📄 Extrato recente:", size=16),
                    self.lista_extrato,

                    # Notificações
                    self.notificador.get_snackbar()
                ],
                spacing=15
            ),
            padding=20
        )

    def atualizar_extrato(self, e):
        """
        Atualiza a exibição do saldo e do extrato da conta selecionada.

        Parâmetro:
        - e: Evento de mudança do dropdown.
        """
        valor = self.dropdown_ref.current.value
        if not valor:
            self.notificador.erro(e.page, "Selecione uma conta.")
            return

        numero = int(valor)
        conta = self.cliente.buscar_conta(numero)

        if not conta or not conta.ativa:
            self.notificador.erro(e.page, "Conta inválida ou inativa.")
            return

        saldo = self.servico.obter_saldo(conta)
        self.saldo_text.value = f"💰 Saldo: R$ {saldo:.2f}"

        transacoes = self.servico.obter_transacoes(conta)

        self.lista_extrato.controls.clear()
        if not transacoes:
            self.lista_extrato.controls.append(
                ft.Text("Nenhuma transação encontrada.", italic=True)
            )
        else:
            for t in transacoes:
                self.lista_extrato.controls.append(ft.Text(str(t), size=15))

        e.page.update()
