import os

# Caminho absoluto até a raiz + dados/contas.json
CAMINHO_DADOS_JSON = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "dados", "contas.json")
)