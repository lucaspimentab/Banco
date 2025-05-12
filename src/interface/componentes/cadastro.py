import flet as ft
from interface.componentes.campo_com_icone import CampoComIcone

class TelaCadastro:
    def __init__(self, on_cadastro_callback=None, on_voltar_login=None):
        self.on_cadastro_callback = on_cadastro_callback
        self.on_voltar_login = on_voltar_login

        # Referências
        self.nome_ref = ft.Ref[str]()
        self.cpf_ref = ft.Ref[str]()
        self.tel_ref = ft.Ref[str]()
        self.end_ref = ft.Ref[str]()
        self.email_ref = ft.Ref[str]()
        self.tipo_conta_ref = ft.Ref[str]()

        self.view = self.criar_view()

    def criar_view(self):
        titulo = ft.Text("CADASTRO DE CONTA", size=24, weight=ft.FontWeight.BOLD)

        tipo_conta_texto = ft.Text("Qual tipo de conta deseja criar?", size=16)

        tipo_conta_grupo = ft.RadioGroup(
            content=ft.Row(
                controls=[
                    ft.Radio(value="poupanca", label="Poupança"),
                    ft.Radio(value="corrente", label="Corrente"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ref=self.tipo_conta_ref
        )

        campos = ft.Column([
            CampoComIcone("person", "Nome", ref_obj=self.nome_ref),
            CampoComIcone("badge", "CPF", ref_obj=self.cpf_ref),
            CampoComIcone("phone", "Telefone", ref_obj=self.tel_ref),
            CampoComIcone("home", "Endereço", ref_obj=self.end_ref),
            CampoComIcone("mail", "Email", ref_obj=self.email_ref),
        ], spacing=10)

        botao_cadastro = ft.ElevatedButton("Fazer cadastro", on_click=self.on_cadastrar_click)

        link_login = ft.TextButton("Já tem uma conta? Fazer login", on_click=self.on_voltar_login)

        return ft.Container(
            content=ft.Column(
                controls=[
                    titulo,
                    tipo_conta_texto,
                    tipo_conta_grupo,
                    campos,
                    botao_cadastro,
                    link_login,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
            expand=True
        )

    def on_cadastrar_click(self, e):
        dados = {
            "tipo_conta": self.tipo_conta_ref.value,
            "nome": self.nome_ref.value,
            "cpf": self.cpf_ref.value,
            "telefone": self.tel_ref.value,
            "endereco": self.end_ref.value,
            "email": self.email_ref.value,
        }
        print("Cadastro:", dados)

        if self.on_cadastro_callback:
            self.on_cadastro_callback(dados)
