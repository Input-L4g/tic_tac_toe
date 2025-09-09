# from __future__ import annotations
import socket
from typing import (
    Tuple,
    TypeAlias,
    List,
    Protocol,
    Literal,
    Optional,
    TypedDict,
    Union
)
from src.protocols.enums import GameWarning, ServerWarning, GameActions
from src.protocols.errors import GameError
from src.core.config import GameSymbols

IpAddress: TypeAlias = str
ConectionPort: TypeAlias = int

SocketConection: TypeAlias = socket.socket
Address: TypeAlias = Tuple[IpAddress, ConectionPort]

PlayerId: TypeAlias = int
GameBoard: TypeAlias = List[Optional[int]]

SystemComunication: TypeAlias = Union[GameWarning, ServerWarning, GameError]
ValidationResult: TypeAlias = Union[GameWarning, GameError]
SystemWarning: TypeAlias = Union[GameWarning, ServerWarning]
MessageType: TypeAlias = Union[GameActions, str]

class GameSymbolsProtocol(Protocol): # pylint: disable=too-few-public-methods
    CROSS: Literal['x']
    CIRCLE: Literal['o']

class PayLoad(TypedDict, total=False):
    slot: int
    player_id: int
    success: bool
    action: GameActions
    error: Optional[SystemComunication]

class SystemMessage(TypedDict):
    """
    type: str -> Tipo da messagem.

    payload: PayLoad -> Informação útil.
    """
    type: MessageType
    payload: PayLoad

class PlayerDict(TypedDict):
    id: PlayerId
    name: str
    symbol: GameSymbols
    client: SocketConection

PlayerList: TypeAlias = List[PlayerDict]
