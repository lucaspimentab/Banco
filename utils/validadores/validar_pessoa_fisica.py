from datetime import datetime
from utils.validadores.validar_pessoa import ValidarPessoa as Validar
from utils.constantes import IDADE_MINIMA

class ValidarPessoaFisica(Validar):
    """
    Classe utilitária que herda de ValidarPessoa validações básicas e 
    implementa validações específicas de pessoas físicas.
    """
    @staticmethod
    def todos_campos(nome: str, email: str, cpf: str, cep: str, numero_endereco: str, telefone: str, data_nascimento: str) -> list[str]:
        """
        Valida todos os campos de uma pessoa física. 
        
        Usa a validação da classe pai pra validar campos comuns entre os tipos de Pessoa e
        valida demais atributos específicos de PessoaFisica.

        Args:
            nome (str): Nome da pessoa.
            email (str): Email da pessoa.
            cpf (str): CPF da pessoa.
            cep (str): CEP da pessoa.
            numero_endereco (str): Número de endereço da pessoa.
            telefone (str): Telefone da pessoa.
            data_nascimento (str): Data de nascimento da pessoa.

        Returns:
            erros (list[str]): Lista de erros encontrados.
        """
        erros = Validar._campos_comuns(nome, email, cep, numero_endereco, telefone)

        try:
            ValidarPessoaFisica.cpf(cpf)
        except ValueError as e:
            erros.append(str(e))
        
        try:
            ValidarPessoaFisica.data_nascimento(data_nascimento)
        except ValueError as e:
            erros.append(str(e))

        return erros

    @staticmethod
    def cpf(cpf: str) -> None:
        """
        Valida se o CPF é válido no formato básico.
        Aceita strings com ou sem pontos/traços.

        Args:
            cpf (str): Número de CPF a ser validado.

        Raises:
            ValueError: Se o CPF estiver em branco.
            ValueError: Se o CPF não contiver exatamente 11 dígitos numéricos.
        """
        cpf_limpo = Validar._limpar_numeros(cpf)

        if not cpf_limpo:
            raise ValueError("O CPF não pode estar em branco.")

        if not cpf_limpo.isdigit() or len(cpf_limpo) != 11:
            raise ValueError("O CPF deve conter exatamente 11 dígitos numéricos.")
    
    @staticmethod
    def data_nascimento(data: datetime, idade_minima: int = IDADE_MINIMA) -> None:
        """
        Valida a data de nascimento. 
        Verifica se a data não é futura e se a pessoa tem a idade mínima.

        Args:
            data (str | datetime): Data no formato "dd/mm/aaaa" ou datetime já convertido.
            idade_minima (int): Idade mínima permitida (padrão segundo IDADE_MINIMA).

        Raises:
            ValueError: Se a data for inválida.
            ValueError: Se a data for no futuro ou indicar idade menor que a mínima.
            ValueError: Se a data indicar idade menor que a mínima.
            TypeError: Se o tipo de entrada for inválido.
        """
        if isinstance(data, str):
            try:
                data = datetime.strptime(data, "%d/%m/%Y")
            except ValueError:
                raise ValueError("Data de nascimento inválida. Use o formato dd/mm/aaaa.")
        elif not isinstance(data, datetime):
            raise TypeError("Data de nascimento deve ser uma string ou datetime.")

        if data > datetime.now():
            raise ValueError("Data de nascimento não pode ser no futuro.")

        hoje = datetime.today()
        idade = hoje.year - data.year - ((hoje.month, hoje.day) < (data.month, data.day))
        if idade < idade_minima:
            raise ValueError(f"Abaixo da idade mínima de {idade_minima} anos.")
