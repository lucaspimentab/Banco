from datetime import datetime

def data_hora_atual_str() -> str:
    """
    Retorna a data e hora atual formatada como string.

    Returns:
        str: Data e hora no formato 'YYYY-MM-DD HH:MM:SS'.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def converter_str_para_datetime(data_str: str, formato: str = "%d/%m/%Y") -> datetime:
    """
    Converte uma string para objeto datetime usando o formato informado.

    Args:
        data_str (str): String representando a data.
        formato (str, opcional): Formato da data na string. Padrão é "%d/%m/%Y".

    Returns:
        datetime: Objeto datetime convertido.

    Raises:
        ValueError: Se a string não estiver no formato esperado.
    """
    try:
        return datetime.strptime(data_str, formato)
    except ValueError as e:
        # Repassa o erro com mensagem mais amigável
        raise ValueError(f"Data '{data_str}' não está no formato esperado '{formato}'.") from e
