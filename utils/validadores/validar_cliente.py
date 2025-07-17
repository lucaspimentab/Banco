import re

class ValidarCliente:
    """
    Classe utilitária para validações específicas de dados do cliente.
    Atualmente implementa validação de força de senha.
    """
    
    @staticmethod
    def senha(senha: str) -> None:
        """
        Valida a força da senha. A senha deve conter pelo menos:
        - 8 caracteres
        - Uma letra maiúscula
        - Uma letra minúscula
        - Um número
        - Um caractere especial

        Raises:
            ValueError: Se a senha não atender aos critérios.
        """
        if (
            len(senha) < 8
            or not re.search(r"[A-Z]", senha)
            or not re.search(r"[a-z]", senha)
            or not re.search(r"[0-9]", senha)
            or not re.search(r"[\W_]", senha)
        ):
            raise ValueError(
                "A senha deve ter pelo menos 8 caracteres, incluindo uma letra maiúscula, uma letra minúscula, um número e um caractere especial."
            )
