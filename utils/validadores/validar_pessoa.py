import re
from abc import ABC

class ValidarPessoa(ABC):
    """
    Classe utilitária abstrata para validações comuns de dados de entrada de Pessoa.
    """
    @staticmethod
    def _campos_comuns(nome: str, email: str, cep: str, numero_endereco: str, telefone: str) -> list[str]:
        """
        Valida os campos comuns entre os tipos de Pessoa (PF/PJ).
        
        Método protegido que serve apenas para evitar duplicação de código na validação
        dos atributos comuns dos tipos de Pessoa.

        Args:
            nome (str): Nome da pessoa.
            email (str): Email da pessoa.
            cep (str): CEP da pessoa.
            numero_endereco (str): Número de endereço da pessoa.
            telefone (str): Telefone da pessoa.

        Returns:
            list[str]: Lista de erros encontrados.
        """
        erros = []

        try:
            ValidarPessoa.nome(nome)
        except ValueError as e:
            erros.append(str(e))

        try:
            ValidarPessoa.email(email)
        except ValueError as e:
            erros.append(str(e))

        try:
            ValidarPessoa.cep(cep)
        except ValueError as e:
            erros.append(str(e))

        try:
            ValidarPessoa.numero_endereco(numero_endereco)
        except ValueError as e:
            erros.append(str(e))

        try:
            ValidarPessoa.telefone(telefone)
        except ValueError as e:
            erros.append(str(e))

        return erros

    @staticmethod
    def _limpar_numeros(texto: str) -> str:
        """
        Remove todos os caracteres que não são dígitos da string.

        Args:
            texto (str): Texto a ser limpo.

        Returns:
            str: Texto contendo apenas dígitos.
        """
        return re.sub(r'\D', '', texto)

    @staticmethod
    def nome(nome: str) -> None:
        """
        Valida o nome, garantindo que não esteja vazio e que contenha apenas letras e espaços.

        Args:
            nome (str): Nome a ser validado.

        Raises:
            ValueError: Se o nome estiver vazio.
            ValueError: Se o nome contiver caracteres inválidos.
        """
        if not nome.strip():
            raise ValueError("O nome não pode estar em branco.")

        padrao = r'^[A-Za-zÀ-ÿ\s]+$'  # aceita letras (inclusive acentuadas) e espaços
        if not re.match(padrao, nome):
            raise ValueError("Nome inválido. Use apenas letras e espaços, sem números ou símbolos.")

    @staticmethod
    def email(email: str) -> None:
        """
        Valida o formato do email.

        Args:
            email (str): Email a ser validado.

        Raises:
            ValueError: Se o email estiver vazio.
            ValueError: Se o email não corresponder ao formato esperado.
        """
        if not email.strip():
            raise ValueError("O email não pode estar em branco.")

        # Regex simples para validar email
        padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(padrao, email):
            raise ValueError("Email inválido.")
  
    @staticmethod
    def cep(cep: str) -> None:
        """
        Valida o CEP, removendo caracteres não numéricos antes da validação.

        Args:
            cep (str): CEP a ser validado.

        Raises:
            ValueError: Se o CEP estiver vazio.
            ValueError: Se o CEP não conter 8 dígitos numéricos após limpeza.
        """
        cep_limpo = ValidarPessoa._limpar_numeros(cep)
        if not cep_limpo:
            raise ValueError("O CEP não pode estar em branco.")

        if len(cep_limpo) != 8:
            raise ValueError("CEP inválido. Deve conter 8 dígitos numéricos.")

    @staticmethod
    def numero_endereco(numero_casa: str) -> None:
        """
        Valida o número do endereço, removendo caracteres não numéricos antes da validação.

        Args:
            numero_casa (str): Número do endereço a ser validado.

        Raises:
            ValueError: Se o número do endereço estiver vazio.
            ValueError: Se o número do endereço não for composto somente por dígitos após limpeza.
        """
        numero_limpo = ValidarPessoa._limpar_numeros(numero_casa)
        if not numero_limpo:
            raise ValueError("O número do endereço não pode estar em branco.")

        if not numero_limpo.isdigit():
            raise ValueError("Número do endereço inválido. Deve conter apenas dígitos.")

    @staticmethod
    def telefone(telefone: str) -> None:
        """
        Valida o número de telefone brasileiro.

        Args:
            telefone (str): Número de telefone com ou sem formatação.

        Raises:
            ValueError: Se o telefone estiver vazio.
            ValueError: Se o telefone for inválido.
            ValueError: Se o telefone não tiver a quantia certa de dígitos.
        """
        telefone_limpo = ValidarPessoa._limpar_numeros(telefone)

        if not telefone_limpo:
            raise ValueError("O telefone não pode estar em branco.")
        elif len(telefone_limpo) == 10:
            # fixo: DDD + número (ex: 3133345678)
            if not re.match(r'^[1-9]{2}[2-5]\d{7}$', telefone_limpo):
                raise ValueError("Telefone fixo inválido.")
        elif len(telefone_limpo) == 11:
            # celular: DDD + 9 + número (ex: 31999999999)
            if not re.match(r'^[1-9]{2}9\d{8}$', telefone_limpo):
                raise ValueError("Telefone celular inválido.")
        else:
            raise ValueError("Número de telefone deve conter 10 ou 11 dígitos.") 
  