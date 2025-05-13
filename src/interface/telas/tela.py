import flet as ft

class Tela:
    def __init__(self):
        # Cria a view padrão ao instanciar a tela
        self.view = ft.Container(expand=True, alignment=ft.alignment.center)

    def criar_view(self, page):
        # Pode customizar a view conforme necessário
        return self.view

    def add_componentes(self, components):
        # Adiciona componentes organizados verticalmente na view
        self.view.content = ft.Column(
            controls=components,
            alignment=ft.MainAxisAlignment.CENTER
        )
