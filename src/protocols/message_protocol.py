from typing import Union, TypeAlias
from src.protocols.enums import (
    GameActions,
    GameWarning,
    GameStatus,
    ServerWarning
)
from src.protocols.errors import GameError
from src.core.types import PayLoad, SystemMessage
from enum import Enum

MessageType: TypeAlias = Union[
    GameStatus,
    GameActions,
    GameWarning,
    ServerWarning,
    GameError
]

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
