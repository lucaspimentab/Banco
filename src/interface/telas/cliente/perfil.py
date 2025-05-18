import flet as ft
from interface.componentes.notificador import Notificador

class TelaPerfil:
    def __init__(self, cliente):
        """
        Tela de exibição de informações do perfil do cliente.
        
        Parâmetro:
        - cliente: Instância do Cliente com os dados pessoais e contas.
        """
        self.cliente = cliente
        self.notificador = Notificador()
        self.view = self.criar_view()

    def criar_view(self):
        """
        Cria a interface visual do perfil com dados pessoais, endereço e contas.

        Retorna:
        - ft.Container: Componente visual da tela.
        """
        # Título da tela
        titulo = ft.Text("👤 Meu Perfil", size=22, weight=ft.FontWeight.BOLD)

        # Informações pessoais do cliente
        dados_pessoais = ft.Column([
            ft.Text(f"Nome: {self.cliente.nome}", size=16),
            ft.Text(f"CPF: {self.cliente.cpf}", size=16),
            ft.Text(f"Email: {self.cliente.email}", size=16),
            ft.Text(f"Telefone: {self.cliente.telefone}", size=16),
            ft.Text(f"Data de Nascimento: {self.cliente.data_nascimento}", size=16),
        ], spacing=5)

        # Endereço
        endereco = ft.Text(
            f"Endereço: {self.cliente.endereco.cep}, {self.cliente.endereco.numero}",
            size=16
        )

        # Lista de contas do cliente
        contas = ft.Column(
            controls=[
                ft.Text("Contas:", size=18, weight=ft.FontWeight.W_600)
            ] + [
                ft.Text(
                    f"- {conta.tipo.title()} | Número: {conta.numero} | Saldo: R$ {conta.saldo:.2f}",
                    size=15
                ) for conta in self.cliente.contas
            ],
            spacing=4
        )

        # Container geral da tela
        return ft.Container(
            content=ft.Column(
                controls=[
                    titulo,
                    dados_pessoais,
                    endereco,
                    ft.Divider(),
                    contas,
                    self.notificador.get_snackbar()
                ],
                spacing=15
            ),
            padding=20
        )
