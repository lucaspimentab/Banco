import flet as ft

class Tela:
    def __init__(self):
        self.view = self.criar_view()

    def criar_view(self):
        # Pode ser um container genérico para as telas
        return ft.Container(expand=True, alignment=ft.alignment.center)

    def add_componentes(self, components):
        # Método para adicionar componentes específicos
        self.view.content = ft.Column(controls=components, alignment=ft.MainAxisAlignment.CENTER)