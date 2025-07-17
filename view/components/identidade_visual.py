from flet import Colors, TextStyle, FontWeight

"""
Definições visuais reutilizáveis do sistema bancário.
"""


# Paleta de cores
CORES = {
    "fundo": "#f2f4f7",       # fundo suave
    "primaria": "#0077cc",    # azul institucional
    "primaria_hover": "#005fa3",
    "secundaria": "#e3f2fd",  # azul claro
    "erro": "#e53935",        # vermelho claro
    "sucesso": "#2e7d32",     # verde
    "texto": "#212121",       # preto suave
    "icone_sidebar": "#ffffff",
    "fundo_sidebar": "#004a80",
}

# Tamanhos de fonte
FONTES = {
    "titulo": 22,
    "subtitulo": 18,
    "normal": 16,
    "pequena": 13,
}

# Estilos pré-definidos
ESTILOS_TEXTO = {
    "titulo": TextStyle(size=FONTES["titulo"], weight=FontWeight.BOLD, color=CORES["texto"]),
    "subtitulo": TextStyle(size=FONTES["subtitulo"], weight=FontWeight.W_500, color=CORES["texto"]),
    "normal": TextStyle(size=FONTES["normal"], color=CORES["texto"]),
    "erro": TextStyle(size=FONTES["pequena"], color=CORES["erro"]),
}

# Ícones padrão
ICONES_CAMPOS = {
    "nome": "person",
    "cpf": "badge",
    "telefone": "call",
    "email": "mail",
    "senha": "lock",
    "cep": "location_on",
    "numero": "pin",
    "data_nascimento": "calendar_today",
    "valor": "attach_money"
}