import flet as ft


class BotaoPrimario(ft.ElevatedButton):
    """
    Botão com estilo primário padrão do sistema.

    Usado para ações principais (como "Confirmar", "Salvar", "Entrar").
    """

    def __init__(self, texto: str, on_click: callable):
        """
        Inicializa um botão elevado com cor de fundo azul e texto branco.

        Args:
            texto (str): Texto exibido no botão.
            on_click (callable): Função a ser chamada ao clicar.
        """
        super().__init__(
            text=texto,
            on_click=on_click,
            bgcolor=ft.Colors.BLUE_600,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=6))
        )


class BotaoSecundario(ft.TextButton):
    """
    Botão com estilo secundário do sistema.

    Usado para ações secundárias ou de navegação (como "Voltar", "Cancelar").
    """

    def __init__(self, texto: str, on_click: callable):
        """
        Inicializa um botão de texto simples com cor azul escura.

        Args:
            texto (str): Texto exibido no botão.
            on_click (callable): Função a ser chamada ao clicar.
        """
        super().__init__(
            text=texto,
            on_click=on_click,
            style=ft.ButtonStyle(color=ft.Colors.BLUE_800)
        )
