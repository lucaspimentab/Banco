import flet as ft
from view.roteador import navegar

def main(page: ft.Page):
    """
    Função principal que inicializa a aplicação, configura aspectos visuais
    e define o comportamento de navegação entre telas.
    """
    # Configurações iniciais do aplicativo
    page.title = "Sistema Bancário"
    page.bgcolor = ft.Colors.WHITE
    page.window_width = 1000
    page.window_height = 700
    page.theme_mode = ft.ThemeMode.LIGHT

    # Ativa o roteador ao alterar a rota da página
    page.on_route_change = lambda e: navegar(page, page.route)

    page.go("/login")

if __name__ == "__main__":
    ft.app(target=main)