import flet as ft

class CampoComIcone(ft.Row):
    def __init__(
        self,
        icone: str,               # Nome do ícone. Ex: "LOCK", "PERSON", ...
        label: str,               # Nome do campo
        senha: bool = False,      # Dados privados? sim/não
        ref_obj: ft.Ref = None,   # Referência do valor caso necessário
        hint_text: str = ""       # Texto de dica
    ):
        icone_ft = getattr(ft.Icons, icone.upper(), ft.Icons.HELP)  # Fallback: ícone de ajuda se não existir

        self.campo = ft.TextField(
            label=label,
            hint_text=hint_text,
            password=senha,
            can_reveal_password=senha,
            ref=ref_obj
        )

        super().__init__(
            controls=[
                ft.Icon(icone_ft),
                self.campo
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )