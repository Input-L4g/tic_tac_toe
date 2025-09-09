from json import dumps, loads
from src.core.types import SystemMessage

def serialize(message: SystemMessage) -> bytes:
    """
    Serializa uma mensagem do sistema e converte
    para bytes.

    Args:
        message (SystemMessage): Mensagem do sistema.

    Returns:
        bytes: A mensagem serializada em bytes.
    """
    data = dumps(message)
    return data.encode()

def deserialize(message: bytes) -> SystemMessage:
    """
    Deserializa uma mensagem do sistema, convertendo
    para o formato original.

    Args:
        message (bytes): Mensagem serializada em bytes.

    Returns:
        SystemMessage: A mensagem deserializada e formatada.
    """
    data = message.decode()
    return loads(data)
