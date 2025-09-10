from enum import Enum
from typing import Optional
from src.core.config import RESPONSE_MESSAGES
from src.core.types import (
    PayLoad,
    SystemMessage,
    MessageType,
    ResponseCode,
    ResponseMessage
)

def create_message(
    msg_type: MessageType,
    payload: PayLoad
    ) -> SystemMessage:
    """
    Cria uma Mensagem do Sistema.

    Args:
        msg_type (MessageType): Tipo da mensagem.
            Será usada apenas como valor da constante.

        payload (PayLoad): Informação útil da mensagem.

    Returns:
        SystemMessage: Mensagem gerada.
    """
    type_ = msg_type
    if isinstance(msg_type, Enum):
        type_ = msg_type.value
    return {"type": type_, "payload": payload}

def create_error_message(
        error_code: ResponseCode,
        traceback: Optional[Exception] = None
    ) -> ResponseMessage:
    """
    Cria uma mensagem de erro.

    Args:
        error_code (ResponseCode): Código do erro.

    Returns:
        ErrorMessage: Mensagem de erro formatada.
    """
    return {
        "code": error_code,
        "message": RESPONSE_MESSAGES.get(error_code),
        "traceback": traceback
        }
