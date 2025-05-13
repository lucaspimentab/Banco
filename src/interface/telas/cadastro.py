import flet as ft
from interface.componentes.campo_com_icone import CampoComIcone

class TelaCadastro:
    def __init__(self, on_cadastro_callback=None, on_voltar_login=None):
        self.on_cadastro_callback = on_cadastro_callback
        self.on_voltar_login = on_voltar_login

        # Referências
        self.nome_ref       = ft.Ref[str]()
        self.cpf_ref        = ft.Ref[str]()
        self.tel_ref        = ft.Ref[str]()
        self.nasc_ref       = ft.Ref[str]()
        self.end_ref        = ft.Ref[str]()
        self.email_ref      = ft.Ref[str]()
        self.senha_ref      = ft.Ref[str]()
        self.tipo_conta_ref = ft.Ref[str]()

        self.snackbar = ft.SnackBar(ft.Text(""))
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

        campos = ft.Column(
            [
                CampoComIcone("person", "Nome", ref_obj=self.nome_ref, hint_text="Nome completo"),
                CampoComIcone("badge", "CPF", ref_obj=self.cpf_ref, hint_text="Somente números, sem pontos ou traços"),
                CampoComIcone("cake", "Data de Nascimento (aaaa-mm-dd)", ref_obj=self.nasc_ref, hint_text="Ex: 2005-08-15"),
                CampoComIcone("phone", "Telefone (DDD + número)", ref_obj=self.tel_ref, hint_text="Ex: 31991234567"),
                CampoComIcone("home", "CEP + número da casa", ref_obj=self.end_ref, hint_text="Ex: 30130-010, 123"),
                CampoComIcone("mail", "Email", ref_obj=self.email_ref, hint_text="Ex: nome@email.com"),
                CampoComIcone("lock", "Senha", ref_obj=self.senha_ref, senha=True, hint_text="Mínimo 9 caracteres com número, letra e símbolo"),
            ],
            spacing=10
        )

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
                    self.snackbar
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
            expand=True
        )

    def mostrar_erro(self, page, mensagem):
        self.snackbar.content.value = mensagem
        self.snackbar.bgcolor = ft.Colors.RED_600
        self.snackbar.open = True
        page.snack_bar = self.snackbar
        page.update()

    def mostrar_sucesso(self, page, mensagem):
        self.snackbar.content.value = mensagem
        self.snackbar.bgcolor = ft.Colors.GREEN_600
        self.snackbar.open = True
        page.snack_bar = self.snackbar
        page.update()

    def on_cadastrar_click(self, e):
        page = e.page
        dados = {
            "tipo_conta": self.tipo_conta_ref.current.value,
            "nome": self.nome_ref.current.value,
            "cpf": self.cpf_ref.current.value,
            "telefone": self.tel_ref.current.value,
            "data_nascimento": self.nasc_ref.current.value,
            "endereco": self.end_ref.current.value,
            "email": self.email_ref.current.value,
            "senha": self.senha_ref.current.value,
        }
        print("Cadastro:", dados)

        erros = []

        if not dados["tipo_conta"]:
            erros.append("Selecione um tipo de conta.")
        if not dados["nome"].strip():
            erros.append("Preencha o nome.")
        if not dados["cpf"].isdigit() or len(dados["cpf"]) != 11:
            erros.append("CPF inválido. Digite apenas 11 dígitos.")
        if not dados["telefone"].isdigit() or len(dados["telefone"]) < 10:
            erros.append("Telefone inválido. Ex: 31991234567.")
        if not dados["data_nascimento"] or len(dados["data_nascimento"]) != 10:
            erros.append("Informe a data de nascimento no formato aaaa-mm-dd.")
        if "," not in dados["endereco"]:
            erros.append("Endereço incompleto. Use CEP + número da casa, separado por vírgula.")
        if "@" not in dados["email"] or "." not in dados["email"]:
            erros.append("Email inválido.")
        if len(dados["senha"]) < 9:
            erros.append("Senha muito curta. Mínimo de 9 caracteres.")

        if erros:
            self.mostrar_erro(page, "\n".join(erros))
            return

        if self.on_cadastro_callback:
            self.on_cadastro_callback(dados)