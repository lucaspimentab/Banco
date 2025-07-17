import flet as ft
import uuid
from view.components.campos import CampoValor, CampoTextoPadrao, CampoCPF, CampoCNPJ
from view.components.mensagens import Notificador
from controller.pagamento_controller import PagamentoController
from controller.conta_controller import ContaController
from controller.perfil_controller import PerfilController
from view.components.identidade_visual import CORES, ESTILOS_TEXTO


class TelaPagamento:
    """
    Classe responsável pela tela de pagamentos, permitindo ao cliente realizar transferências entre contas.
    """

    def __init__(self, banco, cliente):
        self.banco = banco
        self.cliente = cliente
        self.notificador = Notificador()

        self.tipo_chave = ft.Ref[ft.Dropdown]()
        self.conta_destino_ref = ft.Ref[ft.Dropdown]()
        self.campo_doc = CampoCPF()
        self.campo_doc.on_blur = self.buscar_destinatario_automatico
        self.container_chave = ft.Container(content=ft.Column([self.campo_doc]))

        self.dropdown_conta_destino = ft.Dropdown(
            ref=self.conta_destino_ref,
            label="Conta de destino",
            width=300,
            opacity=0,
            disabled=True
        )

        self.campo_valor = CampoValor()
        self.campo_desc = CampoTextoPadrao(label="Descrição", hint="Opcional")
        self.campo_senha = ft.TextField(label="Sua senha", password=True, can_reveal_password=True, width=300)
        self.nome_destinatario_text = ft.Text("", size=14, italic=True, color=CORES["texto"])

        self.conta_ref = ft.Ref[ft.Dropdown]()
        self.saldo_text = ft.Text("", size=14, italic=True)
        self.tipo_conta_text = ft.Text("", size=14)
        self.limite_text = ft.Text("", size=14)

        self.destinatario_confirmado = False
        self.view = self.criar_view()

    def criar_view(self) -> ft.Container:
        """Cria a visualização completa da tela de pagamentos."""
        opcoes_contas = [
            ft.dropdown.Option(num) for num in ContaController.contas_ativas_para_dropdown(self.cliente)
        ]

        dropdown_conta = ft.Dropdown(
            label="Conta de origem",
            ref=self.conta_ref,
            options=opcoes_contas,
            width=300,
            on_change=self.atualizar_saldo
        )

        self.dropdown_tipo = ft.Dropdown(
            ref=self.tipo_chave,
            label="Tipo de chave",
            width=300,
            options=[ft.dropdown.Option("CPF"), ft.dropdown.Option("CNPJ")],
            on_change=self.alternar_campo_chave
        )

        conteudo = ft.Container(
            width=500,
            padding=25,
            bgcolor=CORES["fundo"],
            border_radius=16,
            shadow=ft.BoxShadow(blur_radius=20, color="#00000022", offset=ft.Offset(3, 3)),
            content=ft.Column(
                spacing=18,
                controls=[
                    ft.Row([
                        ft.Icon(name=ft.Icons.PAYMENTS_OUTLINED, size=28, color=CORES["primaria"]),
                        ft.Text("Transferência entre contas", style=ESTILOS_TEXTO["titulo"])
                    ], alignment=ft.MainAxisAlignment.CENTER),

                    dropdown_conta,
                    self.saldo_text,
                    self.tipo_conta_text,
                    self.limite_text,

                    self.dropdown_tipo,
                    self.container_chave,
                    self.nome_destinatario_text,
                    self.dropdown_conta_destino,

                    self.campo_valor,
                    self.campo_desc,
                    self.campo_senha,

                    ft.ElevatedButton("Confirmar pagamento", on_click=self.realizar_pagamento),
                    self.notificador.get_snackbar()
                ]
            )
        )


        return ft.Container(
            alignment=ft.alignment.top_center,
            expand=True,
            bgcolor=CORES["secundaria"],
            padding=30,
            content=ft.Column(
                scroll=ft.ScrollMode.AUTO,
                controls=[conteudo]
            )
        )



    def alternar_campo_chave(self, e):
        """Alterna entre os campos CPF e CNPJ conforme tipo selecionado."""
        tipo = self.tipo_chave.current.value
        self.destinatario_confirmado = False
        self.nome_destinatario_text.value = ""
        self.dropdown_conta_destino.opacity = 0
        self.dropdown_conta_destino.disabled = True
        self.dropdown_conta_destino.options = []

        self.campo_doc = CampoCPF() if tipo == "CPF" else CampoCNPJ()
        self.campo_doc.on_blur = self.buscar_destinatario_automatico
        self.container_chave.content = ft.Column([self.campo_doc])
        self.container_chave.update()
        e.page.update()

    def buscar_destinatario_automatico(self, e):
        """Busca automaticamente destinatário e exibe suas contas ativas ao perder foco do campo documento."""
        doc = self.campo_doc.value.strip()
        self.destinatario_confirmado = False
        self.dropdown_conta_destino.opacity = 0
        self.dropdown_conta_destino.disabled = True
        self.dropdown_conta_destino.options = []

        if not doc:
            self.nome_destinatario_text.value = ""
            e.page.update()
            return

        cliente = PerfilController.buscar_cliente_por_documento(doc)
        if not cliente:
            self.nome_destinatario_text.value = "❌ Destinatário não encontrado."
        else:
            contas = [c for c in cliente.contas if c.get_estado_da_conta()]
            if not contas:
                self.nome_destinatario_text.value = "❌ Destinatário não possui conta ativa."
            else:
                nome = cliente.pessoa.get_nome()
                self.nome_destinatario_text.value = f"👤 {nome}"
                self.dropdown_conta_destino.options = [
                    ft.dropdown.Option(str(c.get_numero_conta())) for c in contas
                ]
                self.dropdown_conta_destino.opacity = 1
                self.dropdown_conta_destino.disabled = False
                self.destinatario_confirmado = True

        e.page.update()

    def atualizar_saldo(self, e):
        """Atualiza saldo, tipo e limite da conta de origem selecionada."""
        numero = self.conta_ref.current.value
        self.saldo_text.value = ""
        self.tipo_conta_text.value = ""
        self.limite_text.value = ""

        if numero:
            resultado, erro = ContaController.obter_extrato(numero)

            if erro or not isinstance(resultado, tuple) or len(resultado) != 2:
                self.saldo_text.value = "Erro ao carregar saldo."
            else:
                saldo, conta = resultado
                self.saldo_text.value = f"💰 Saldo disponível: R$ {saldo:.2f}"
                self.tipo_conta_text.value = f"🏷 Tipo da conta: {conta.__class__.__name__}"
                self.limite_text.value = f"🔒 Limite: R$ {conta.limite_transferencia:.2f}"

        e.page.update()

    def realizar_pagamento(self, e):
        """Processa o pagamento após validar os campos."""
        page = e.page

        try:
            conta_origem = int(self.conta_ref.current.value)
            conta_destino = int(self.conta_destino_ref.current.value)
        except (ValueError, TypeError):
            self.notificador.erro(page, "Erro ao selecionar conta. Tente novamente.")
            return

        resultado = PagamentoController.processar_pagamento(
            conta_origem_num=conta_origem,
            doc_destino=self.campo_doc.value.strip(),
            valor=self.campo_valor.get_valor(),
            descricao=self.campo_desc.value,
            senha=self.campo_senha.value.strip(),
            conta_destino_numero=conta_destino
        )

        if resultado["sucesso"]:
            self.notificador.sucesso(page, resultado["mensagem"])
            self.atualizar_saldo(e)
            self.resetar_campos()
        else:
            self.notificador.erro(page, "\n".join(resultado["erros"]))

        page.update()

    def resetar_campos(self):
        """Limpa e reseta todos os campos após pagamento bem-sucedido."""
        self.__init__(self.banco, self.cliente)