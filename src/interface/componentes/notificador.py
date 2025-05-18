import flet as ft

class Notificador:
    def __init__(self):
        self._snackbar = ft.SnackBar(
            content=ft.Text(""),
            duration=3500,
            show_close_icon=True,
        )

    def erro(self, page, mensagem):
        self._mostrar(page, mensagem, ft.Colors.RED_700)

    def sucesso(self, page, mensagem):
        self._mostrar(page, mensagem, ft.Colors.GREEN_700)

    def info(self, page, mensagem):
        self._mostrar(page, mensagem, ft.Colors.BLUE_700)

    def _mostrar(self, page, mensagem, cor):
        self._snackbar.content.value = mensagem
        self._snackbar.bgcolor = cor
        page.snack_bar = self._snackbar
        self._snackbar.open = True
        page.update()

    def get_snackbar(self):
        return self._snackbar
