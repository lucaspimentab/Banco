import flet as ft
from urllib.parse import quote, unquote, urlparse, parse_qs

from view.telas.tela_login import TelaLogin
from view.telas.tela_cadastro import TelaCadastro
from view.telas.tela_usuario import TelaUsuario
from controller.auth_controller import AuthController


def navegar(page: ft.Page, route: str):
    """
    Controla a navegação entre as telas da aplicação.

    Args:
        page (ft.Page): Página atual do aplicativo Flet.
        route (str): Caminho da rota para navegação.
    """
    page.views.clear()

    def redirecionar_para_painel(usuario_id: str):
        """Redireciona o usuário autenticado para o painel principal."""
        rota_segura = f"/painel/{quote(usuario_id, safe='')}/perfil"
        page.go(rota_segura)

    if route == "/login":
        # Tela inicial para login do usuário
        tela_login = TelaLogin(
            on_login_sucesso=redirecionar_para_painel,
            on_ir_cadastro=lambda: page.go("/cadastro")
        )
        page.views.append(ft.View("/login", controls=[tela_login.criar_view(page)]))

    elif route == "/cadastro":
        # Tela para cadastro de novos usuários
        tela_cadastro = TelaCadastro(
            on_cadastro_sucesso=lambda: page.go("/login"),
            on_voltar_login=lambda: page.go("/login")
        )
        view = ft.View("/cadastro", controls=[tela_cadastro.view])
        page.views.append(view)

        def _apos_renderizacao(e):
            """Atualiza os campos após renderização da página (responsividade)."""
            tela_cadastro.atualizar_campos_visiveis(e)

        page.on_resize = _apos_renderizacao

    elif route.startswith("/painel/"):
        # Tela principal do usuário já autenticado
        parsed = urlparse(route)
        rota_limpa = parsed.path
        query = parse_qs(parsed.query)

        # Identifica se deve resetar estado da subrota atual
        resetar = query.get("resetar", ["false"])[0] == "true"

        partes = rota_limpa.split("/")
        usuario_id = unquote(partes[2])

        # Obtém o cliente autenticado da sessão ativa
        cliente = AuthController.sessao_ativa.get(usuario_id)

        if not cliente:
            # Caso cliente não esteja autenticado, redireciona para login
            page.go("/login")
            return

        # Define a subrota padrão como perfil caso não especificada
        subrota = partes[3] if len(partes) > 3 else "perfil"

        nova_tela_usuario = TelaUsuario(
            banco=None,
            cliente=cliente,
            on_logout=lambda e: page.go("/login"),
            subrota=subrota,
            resetar=resetar
        )

        view = ft.View(route, controls=[nova_tela_usuario.view])
        page.views.append(view)

    else:
        # Rota não reconhecida: retorna ao login por segurança
        page.go("/login")

    page.update()