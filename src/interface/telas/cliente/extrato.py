import flet as ft
from interface.componentes.notificador import Notificador
from app.servicos.servico_extrato import ServicoExtrato

class TelaExtrato:
    def __init__(self, cliente):
        """
        Tela que exibe o saldo e o extrato da conta padrão de um cliente.

        Parâmetro:
        - cliente: Instância do Cliente logado.
        """
        self.cliente = cliente
        self.servico = ServicoExtrato(cliente)
        self.notificador = Notificador()
        self.view = self.criar_view()

    def criar_view(self):
        """
        Monta a interface gráfica da tela com título, saldo, informações da conta
        e histórico de transações.

        Retorna:
        - ft.Container: Container com os elementos da view.
        """
        titulo = ft.Text("💰 Saldo e Extrato", size=22, weight=ft.FontWeight.BOLD)

        saldo = self.servico.obter_saldo()
        conta_padrao = self.cliente.buscar_conta_padrao()
        numero_conta = conta_padrao.numero if conta_padrao else "N/A"
        tipo_conta = conta_padrao.tipo.title() if conta_padrao else "Indefinido"

        info_conta = ft.Column([
            ft.Text(f"Conta: {tipo_conta} ({numero_conta})", size=16),
            ft.Text(f"Saldo atual: R$ {saldo:.2f}", size=18, weight=ft.FontWeight.W_600),
        ], spacing=5)

        # Lista de transações (extrato)
        self.lista_extrato = ft.Column([], spacing=8, scroll=ft.ScrollMode.AUTO)

        # Carrega transações ao criar a view
        self.carregar_extrato()

        return ft.Container(
            content=ft.Column(
                controls=[
                    titulo,
                    info_conta,
                    ft.Divider(),
                    ft.Text("📄 Extrato recente:", size=16),
                    self.lista_extrato,
                    self.notificador.get_snackbar()
                ],
                spacing=15
            ),
            padding=20
        )

    def carregar_extrato(self):
        """
        Carrega e exibe as transações da conta padrão do cliente.
        """
        transacoes = self.servico.obter_transacoes()
        self.lista_extrato.controls.clear()

        if not transacoes:
            self.lista_extrato.controls.append(
                ft.Text("Nenhuma transação encontrada.", italic=True)
            )
        else:
            for t in transacoes:
                self.lista_extrato.controls.append(
                    ft.Text(str(t), size=15)
                )
