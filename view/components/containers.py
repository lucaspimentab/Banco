import flet as ft
from controller.conta_controller import ContaController


class CartaoResumo(ft.Container):
    """
    Cartão visual para exibir informações agrupadas como título e conteúdo.
    Usado para agrupar dados como saldo, extrato, perfil, etc.
    """

    def __init__(
        self,
        titulo: str,
        conteudo: list[ft.Control],
        cor_fundo: str = ft.Colors.WHITE,
        expand: bool = False,
        padding: int = 20,
        sombra: bool = True
    ):
        super().__init__(
            bgcolor=cor_fundo,
            padding=padding,
            border_radius=10,
            expand=expand,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=4,
                color=ft.Colors.GREY_400,
                offset=ft.Offset(2, 2),
            ) if sombra else None,
            content=ft.Column(
                controls=[ft.Text(titulo, size=16, weight=ft.FontWeight.BOLD)] + conteudo,
                spacing=8,
                expand=True  # permite o conteúdo crescer dentro do cartão
            )
        )


class LinhaSeparadora(ft.Divider):
    """
    Linha horizontal discreta para dividir seções visuais.
    """

    def __init__(self):
        super().__init__(height=1, thickness=1, color=ft.Colors.GREY_300)


class CartaoTransacao(ft.Container):
    """
    Cartão visual para exibir uma transação bancária no extrato.
    Mostra descrição, e abaixo o nome, documento e número da conta envolvida.
    """

    def __init__(self, texto_transacao: str):
        super().__init__()

        self.padding = 10
        self.bgcolor = self._cor_fundo(texto_transacao)
        self.border_radius = 8

        numero_encontrado = self._extrair_numero_conta(texto_transacao)
        cliente_info = ContaController.obter_info_destinatario(numero_encontrado) if numero_encontrado else "Conta não identificada"

        self.content = ft.Column([
            ft.Text(texto_transacao, size=13),
            ft.Text(cliente_info, size=12, italic=True, color=ft.Colors.GREY)
        ])

    def _extrair_numero_conta(self, texto: str) -> str:
        """
        Extrai o número da conta que aparece após 'conta ' no texto.
        """
        import re
        match = re.search(r"conta (\d+)", texto)
        return match.group(1) if match else None

    def _cor_fundo(self, texto: str) -> str:
        """
        Retorna a cor de fundo baseada no conteúdo textual da transação.
        Verde para recebimento, vermelho para envio, cinza padrão.
        """
        texto = texto.lower()
        if "recebida" in texto or "recebido" in texto or "entrada" in texto:
            return ft.Colors.GREEN_100
        if "enviada" in texto or "saída" in texto or "enviado" in texto or "transferência de" in texto:
            return ft.Colors.RED_100
        return ft.Colors.GREY_100
