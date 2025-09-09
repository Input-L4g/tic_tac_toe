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
