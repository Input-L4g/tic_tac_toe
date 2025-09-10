from enum import Enum

class GameSymbols(Enum):
    CIRCLE = 'o'
    CROSS = 'x'

GAME_REPR_SYMBOLS = {
    GameSymbols.CIRCLE: 0,
    GameSymbols.CROSS: 1
}

VICTORIOUS_INDEX_MOVES = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8), # Linhas
    (0, 3, 6), (1, 4, 7), (2, 5, 8), # Colunas
    (0, 4, 8), (2, 4, 6) # Diagonais
)

RESPONSE_CODES = {
    "SUCCES": 0,
    "HOST_NOT_FOUND": 1001,
    "CONNECTION_REFUSED": 1002,
    "TIMEOUT": 1003,
    "NETWORK_ERROR": 1004,
    "UNKNOWN": 1000,
}

RESPONSE_MESSAGES = {
    0: "Sucesso na operação.",
    1001: "Erro: host inválido ou não encontrado.",
    1002: "Erro: conexão recusada (server não está rodando).",
    1003: "Erro: conexão expirou (timeout).",
    1004: "Erro: Um erro na rede ocorreu.",
    1000: "Erro: Algum erro desonhecido ocorreu."
}
