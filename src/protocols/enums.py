from enum import Enum

class GameActions(Enum):
    """
    Enum que contém as ações do jogo.

    - MAKE_MOVEMENT: Indica um movimento no tabuleiro.
    - EXIT: Indica a saída de um player
    - START: Indica o ínicio de uma partida.
    - RESTART: Indica um reset da partida em andamento.
    """
    MAKE_MOVEMENT = 'make_movement'
    EXIT = 'exit'
    START = 'start'
    RESTART = 'restart'

class ServerWarning(Enum):
    """
    Enum que contém avisos para o servidor.

    - OK: Indica que nada de errado ocorreu
    - DISCONNECT_CLIENT: Indica que um client deve ser desconectado.
    - GAME_READY_TO_START: Indica que o jogo já pode começar.
    """
    OK = 'ok'
    DISCONNECT_CLIENT = 'disconnect_client'
    GAME_READY_TO_START = 'game_ready_to_start'

class GameWarning(Enum):
    """
    Enum que contém avisos do jogo ao servidor
    e comunicação interna.

    - PLAYER_REMOVED: Indica que um player foi removido
    - WINNER_REACHED: Indica que um player já venceu o jogo.
    - GAME_HAS_STARTED: Indica que o jogo já foi começado.
    - OK: Indica sucesso em alguma operação ou validação.
    """
    PLAYER_REMOVED = 'player_removed'
    WINNER_REACHED = 'winner_reached'
    OK = 'ok'

class GameStatus(Enum):
    """
    Enum que contém os status do jogo.

    - READY_TO_START: O jogo já está pronto para começar.
    - WAITING: O jogo está esperando jogadores.
    - ONGOING: O jogo já começou.
    - FINISHED: O jogo foi finalizado.
    """
    READY_TO_START = 'read_to_start'
    WAITING = 'waiting'
    ONGOING = 'ongoing'
    FINISHED = 'finished'
