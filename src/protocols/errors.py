from enum import Enum

class GameError(Enum):
    """
    Um Enum que contém todos os erros detectados do jogo
    em tempo de execução.

    - INVALID_PAYLOAD: Um PayLoad com informações não esperadas foi passado.
    - GAME_HAS_STARTED: Indica que o jogo já foi começado.
    - GAME_ALREADY_FINISHED: Indica que o jogo já foi finalizado.
    - GAME_NOT_STARTED: Indica que o jogo ainda não foi começado.
    - EMPTY_PARTY: Indica que não tem nenhum jogador no jogo.
    - SYMBOL_ALREADY_SELECTED: Indica que um outro jogador já escolheu.
    - NON_EXISTENT_PLAYER: Indica que um player procurado não existe no jogo.
    - INVALID_COMMAND: Um comando inválido.
    - INVALID_ACTION: Uma ação inválida.
    - INVALID_SLOT: Um slot inválido no tabuleiro do jogo.
    - FULL_PARTY: O jogo já está cheio de jogadores.
    - OCCUPIED_SLOT: Um slot selecionado já foi usado.
    - SAME_PLAYER: Um player em questão, é o do turno atual.
    - GAME_ACTION_ERROR: Um erro gerado por algum ação no jogo.
    - ERROR: Indica um erro genérico ou não identificado.
    """
    INVALID_PAYLOAD = 'invalid_payload'
    GAME_ALREADY_FINISHED = 'game_already_finished'
    GAME_HAS_STARTED = 'game_has_started'
    GAME_NOT_STARTED = 'game_not_started'
    EMPTY_PARTY = 'empty_party'
    SYMBOL_ALREADY_SELECTED = 'symbol_already_selected'
    NON_EXISTENT_PLAYER = 'non_existent_player'
    INVALID_COMMAND = 'invalid_command'
    INVALID_ACTION = 'invalid_action'
    INVALID_SLOT = 'invalid_slot'
    FULL_PARTY = 'full_party'
    INSUFFICIENT_PLAYERS = 'insufficient_playes'
    OCCUPIED_SLOT = 'occupied_slot'
    SAME_PLAYER = 'same_player'
    GAME_ACTION_ERROR = 'game_action_error'
    ERROR = 'error'
