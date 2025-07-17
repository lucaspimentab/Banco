class ContaInativaError(Exception):
    """
    Exceção lançada quando uma operação é feita em uma conta inativa.
    """

    def __init__(self, numero_conta: str = None):
        mensagem = (
            f"A conta {numero_conta} está inativa e não pode realizar operações." if numero_conta 
            else "A conta está inativa e não pode realizar operações."
        )
        super().__init__(mensagem)
