import flet as ft
import re
from view.components.identidade_visual import ICONES_CAMPOS


class CampoTextoPadrao(ft.TextField):
    """
    Campo de texto base reutilizável com borda, estilo e ícone padronizados.
    Serve como base para os campos especializados.
    """
    def __init__(self, label: str, hint: str = "", icon: str = None, **kwargs):
        super().__init__(
            label=label,
            hint_text=hint,
            border_radius=6,
            border_color=ft.Colors.BLUE_300,
            focused_border_color=ft.Colors.BLUE_600,
            text_style=ft.TextStyle(size=14),
            prefix_icon=icon,
            **kwargs
        )


class CampoEmail(CampoTextoPadrao):
    """Campo para e-mail com teclado adequado e ícone padronizado."""
    def __init__(self):
        super().__init__(
            label="Email",
            hint="exemplo@email.com",
            keyboard_type="email",
            icon=ICONES_CAMPOS["email"]
        )


class CampoSenha(ft.TextField):
    """Campo de senha com revelação opcional e estilo visual definido."""
    def __init__(self, label="Senha"):
        super().__init__(
            label=label,
            password=True,
            can_reveal_password=True,
            border_radius=6,
            border_color=ft.Colors.BLUE_300,
            focused_border_color=ft.Colors.BLUE_600,
            text_style=ft.TextStyle(size=14),
            prefix_icon=ICONES_CAMPOS["senha"]
        )


class CampoCPF(CampoTextoPadrao):
    """Campo com máscara dinâmica para CPF (000.000.000-00)."""
    def __init__(self):
        super().__init__(label="CPF", hint="000.000.000-00", max_length=14, icon=ICONES_CAMPOS["cpf"])
        self.keyboard_type = "number"
        self.on_change = self._on_change

    def _on_change(self, e):
        self.value = self._formatar(self.value)
        self.update()

    def _formatar(self, texto: str) -> str:
        d = "".join(filter(str.isdigit, texto))[:11]
        return f"{d[:3]}.{d[3:6]}.{d[6:9]}-{d[9:]}" if len(d) >= 9 else \
               f"{d[:3]}.{d[3:6]}.{d[6:]}" if len(d) >= 6 else \
               f"{d[:3]}.{d[3:]}" if len(d) > 3 else d


class CampoCNPJ(CampoTextoPadrao):
    """Campo com máscara dinâmica para CNPJ (00.000.000/0000-00)."""
    def __init__(self):
        super().__init__(label="CNPJ", hint="00.000.000/0000-00", max_length=18, icon=ICONES_CAMPOS.get("cpf"))
        self.keyboard_type = "number"
        self.on_change = self._on_change

    def _on_change(self, e):
        self.value = self._formatar(self.value)
        self.update()

    def _formatar(self, texto: str) -> str:
        d = "".join(filter(str.isdigit, texto))[:14]
        return f"{d[:2]}.{d[2:5]}.{d[5:8]}/{d[8:12]}-{d[12:]}" if len(d) > 12 else \
               f"{d[:2]}.{d[2:5]}.{d[5:8]}/{d[8:]}" if len(d) > 8 else \
               f"{d[:2]}.{d[2:5]}.{d[5:]}" if len(d) > 5 else \
               f"{d[:2]}.{d[2:]}" if len(d) > 2 else d


class CampoCEP(CampoTextoPadrao):
    """Campo com máscara dinâmica para CEP (00000-000)."""
    def __init__(self):
        super().__init__(label="CEP", hint="00000-000", max_length=9, icon=ICONES_CAMPOS["cep"])
        self.keyboard_type = "number"
        self.on_change = self._on_change

    def _on_change(self, e):
        d = "".join(filter(str.isdigit, self.value))[:8]
        self.value = f"{d[:5]}-{d[5:]}" if len(d) > 5 else d
        self.update()


class CampoNome(CampoTextoPadrao):
    """Campo para nome completo com validação integrada e suporte a PF/PJ."""

    def __init__(self):
        super().__init__(
            label="Nome completo",
            hint="Digite seu nome completo",
            icon=ICONES_CAMPOS["nome"]
        )

    def validar(self) -> bool:
        texto = self.value.strip()
        if not texto or not re.match(r"^[A-Za-zÀ-ÿ\s]+$", texto):
            self._mostrar_erro("Nome inválido. Use apenas letras.")
            return False
        self._limpar_erro()
        return True

    def _mostrar_erro(self, mensagem: str):
        self.error_text = mensagem
        self.border_color = ft.Colors.RED
        self.update()

    def _limpar_erro(self):
        self.error_text = ""
        self.border_color = ft.Colors.BLUE_300
        self.update()

    def atualizar_para_empresa(self):
        self.label = "Nome da empresa"
        self.hint_text = "Digite o nome da sua empresa"
        self.prefix_icon = ft.Icons.BUSINESS
        self.update()

    def atualizar_para_pessoa_fisica(self):
        self.label = "Nome completo"
        self.hint_text = "Digite seu nome completo"
        self.prefix_icon = ICONES_CAMPOS["nome"]
        self.update()


class CampoTelefone(CampoTextoPadrao):
    """Campo com máscara e validação para número de telefone brasileiro."""
    def __init__(self):
        super().__init__(label="Telefone", hint="(31) 91234-5678", max_length=15, icon=ICONES_CAMPOS["telefone"])
        self.keyboard_type = "number"
        self.on_change = self._on_change

    def _on_change(self, e):
        self.value = self._formatar(self.value)
        self.update()

    def _formatar(self, texto: str) -> str:
        d = "".join(filter(str.isdigit, texto))[:11]
        return f"({d[:2]}) {d[2:7]}-{d[7:]}" if len(d) > 7 else \
               f"({d[:2]}) {d[2:]}" if len(d) > 2 else d

    def validar(self) -> bool:
        if len("".join(filter(str.isdigit, self.value))) not in [10, 11]:
            self._mostrar_erro("Telefone inválido.")
            return False
        self._limpar_erro()
        return True

    def _mostrar_erro(self, mensagem: str):
        self.error_text = mensagem
        self.border_color = ft.Colors.RED
        self.update()

    def _limpar_erro(self):
        self.error_text = ""
        self.border_color = ft.Colors.BLUE_300
        self.update()


class CampoValor(CampoTextoPadrao):
    """Campo para entrada de valores monetários com validação de formato."""
    def __init__(self):
        super().__init__(
            label="Valor",
            hint="Digite um valor, ex: 100.00",
            keyboard_type="number",
            icon=ICONES_CAMPOS["valor"]
        )

    def validar(self) -> bool:
        valor = self.value.strip()

        if not valor:
            self._mostrar_erro("Valor é obrigatório.")
            return False

        if "." not in valor:
            self._mostrar_erro("Formato de dinheiro inválido. Use ponto como separador decimal.")
            return False

        try:
            numero = float(valor)
            if numero <= 0:
                self._mostrar_erro("O valor deve ser maior que zero.")
                return False
        except ValueError:
            self._mostrar_erro("Valor inválido. Use apenas números com ponto.")
            return False

        self._limpar_erro()
        return True

    def get_valor(self) -> float:
        return float(self.value.strip())

    def _mostrar_erro(self, mensagem: str):
        self.error_text = mensagem
        self.border_color = ft.Colors.RED
        self.update()

    def _limpar_erro(self):
        self.error_text = ""
        self.border_color = ft.Colors.BLUE_300
        self.update()



class CampoDataNascimento(CampoTextoPadrao):
    """Campo com máscara para entrada de datas no formato dd/mm/aaaa."""
    def __init__(self):
        super().__init__(label="Data de Nascimento", hint="dd/mm/aaaa", max_length=10, icon="calendar_today")
        self.keyboard_type = "number"
        self.on_change = self._on_change

    def _on_change(self, e):
        d = "".join(filter(str.isdigit, self.value))[:8]
        self.value = (
            f"{d[:2]}/{d[2:4]}/{d[4:]}" if len(d) > 4 else
            f"{d[:2]}/{d[2:]}" if len(d) > 2 else d
        )
        self.update()