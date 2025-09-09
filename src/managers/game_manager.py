# from __future__ import annotations

from typing import Optional
from random import choice
from src.protocols.enums import (
    GameStatus, GameWarning,
    GameActions, ServerWarning
    )
from src.protocols.errors import GameError
from src.protocols.message_protocol import create_message
from src.core.config import GameSymbols
from src.core.game import TicTacToe
from src.core.types import (
    SystemMessage, PayLoad,
    SystemComunication, ValidationResult,
    PlayerList, PlayerDict,
    SocketConection, PlayerId
    )
from src.utils.validation_utils import was_successful


class GameManager:
    """
    Representa um Manager das ações sob a classe TicTacToe.

    Attributes:
        game (TicTacToe): Um instância do jogo Tic-Tac-Toe.
        player (PlayerList): Lista de players ativos.
        next_player_id (int): Contador de id dos players.
            Indica o id do próximo jogador a se conectar.
        winner (PlayerId | None): O vencedor da partida. Se
            ninguém venceu ainda ou deu empate, fica como None.
        status (GameStatus): Indica o status atual do jogo.
            Veja `GameStatus.__doc__` para as informações
            dos status.
    """
    def __init__(self) -> None:
        self.game: TicTacToe = TicTacToe()
        self.players: PlayerList = []
        self.next_player_id: PlayerId = 0
        self.winner: Optional[PlayerId] = None
        self.status: GameStatus = GameStatus.WAITING

#! ========= COMMANDS =========

    def switch_current_player(
        self,
        random_initial_player: bool = False
        ) -> None:
        """
        Passa o turno para o próximo jogador da lista.

        Se um jogador inicial ainda não foi definido, será
        escolhido o primeiro da lista, caso o parâmetro
        `random_initial_player` for False.

        Args:
            random_initial_player (bool): Escolhe um player
                inicial aleatório. Só irá funcionar se um player
                inicial ainda não foi escolhido.
        """
        current_player_id = self.get_current_player()
        if current_player_id is not None:
            len_players = len(self.players)
            current_player_dict = self.get_player(current_player_id)
            assert current_player_dict is not None
            current_player_index = self.players.index(current_player_dict)
            next_player_id = self.players[(current_player_index + 1) % len_players]["id"]
        else:
            next_player_id = (
                choice(self.players)["id"] if
                random_initial_player else
                self.players[0]["id"]
            )
        self.set_current_player(next_player_id)

    def start_game(self) -> None:
        """Começa o jogo."""
        self.status = GameStatus.ONGOING
        self.reset_board()

    def reset_all(self) -> None:
        """
        Reseta tudo do jogo.

        Isso inclui: Jogadores, atributos, partidas e o tabuleiro.
        """
        self.reset_board()
        self.remove_all_player()
        self.reset_manager()

    def reset_manager(self) -> None:
        """Reseta todos os atributos do GameManager."""
        self.next_player_id: PlayerId = 0
        self.winner: Optional[PlayerId] = None
        self.status: GameStatus = GameStatus.WAITING

    def reset_board(self) -> None:
        """Reseta o tabuleiro."""
        self.game.reset()

    def remove_all_player(self) -> ValidationResult:
        """
        Remove todos os player do jogo.

        Returns:
            ValidationResult: Resultado da ação.
                - GameError.EMPTY_PARTY: Indica que não
                    há jogador para remover.
                - GameWarning.OK: Indica que todos os
                    jogadores foram removidos com sucesso.
        """
        if not self.players:
            return GameError.EMPTY_PARTY
        self.players = []
        return GameWarning.OK

    def remove_player(
        self,
        player_id: PlayerId
        ) -> ValidationResult:
        """
        Remove um jogador com base no id.

        Args:
            player_id (PlayerId): Id do jogador.

        Returns:
            ValidationResult: Indica o resultado
                da ação.
                - GameError.NON_EXISTENT_PLAYER: O player
                    procurado não existe.
                - GameError.EMPTY_PARTY: Não há
                    jogador para remover.
                - GameWarning.OK: O jogador for
                    removido.
        """
        if not self.players:
            return GameError.EMPTY_PARTY
        for i, player in enumerate(self.players):
            if player["id"] == player_id:
                self.players.pop(i)
                break
        else:
            return GameError.NON_EXISTENT_PLAYER
        return GameWarning.OK

    def add_player(
        self,
        player_name: str,
        symbol: GameSymbols,
        client: SocketConection
        ) -> ValidationResult:
        """
        Adiciona jogadores ao jogo.
        Tem um limite de 2 jogadores.

        Args:
            player_name (str): Nome do jogador.
            symbol (GameSymbols): Símbolo do jogador
                em jogo. Pode ser apenas:
                - GameSymbols.CIRCLE: Indica 'O' no jogo.
                - GameSymbols.CROSS: Indica o 'X' no jogo.
            client (socket): O socket do client que fez
                a requisição.

        Returns:
            ValidationResult: O resultado da ação:
                - GameError.FULL_PARTY: Indica que
                    o jogo já tem 2 jogadores.
                - GameError.SYMBOL_ALREADY_SELECTED: Indica
                    que o símbolo escolhido já foi escolhido
                    por outro jogador.
                - GameWarning.OK: Indica que o jogador foi
                    adicionado com sucesso.

        **Note**: Para verificar os jogadores ativos no jogo e
            suas informações, veja o atributo `players`.
        """
        if len(self.players) >= 2:
            return GameError.FULL_PARTY
        validation_result = self._validate_player_symbol(symbol)
        if not was_successful(validation_result):
            return validation_result
        player_id = self.next_player_id
        self.next_player_id += 1
        self.players.append(
            {
                "id": player_id,
                "name": player_name,
                "symbol": symbol,
                "client": client
            }
        )
        return GameWarning.OK

    def apply_action(
        self,
        message: SystemMessage
        ) -> SystemMessage:
        """
        Valida, processa e aplica as seguintes ações:
            - GameActions.MAKE_MOVEMENT.
            - GameActions.RESTART.
            - GameActions.EXIT.
            - GameActions.START.

        Args:
            message (SystemMessage): Requisição da ação.
                Veja `/core/types.py` para ver o formato da mensagem.

        Returns:
            SystemMessage: Mensagem com as informações do
                resultado a aplicação e processamento.
        """
        t, pl = message["type"], message["payload"]
        action = GameActions(t)
        result = self._process_action(action, pl)
        error = self._get_error_return(result)
        payload: PayLoad = {
            "success": error is None,
            "action": action,
            "error": error
        }
        return create_message(result, payload)

#! ========= PROCESSING =========

    def _process_action(
        self,
        action: GameActions,
        payload: PayLoad
        ) -> SystemComunication:
        """
        Processa e aplica as devidas validações
        com base numa ação requisitada.

        Args:
            action (GameActions): Indica qual
                ação será processada.
            payload (PayLoad): Informações sobre
                a ação.

        Returns:
            SystemComunication: O resultado
                do processo da ação.
        """
        if action == GameActions.MAKE_MOVEMENT:
            result = self._process_make_movement(payload)

        elif action == GameActions.RESTART:
            result = self._process_restart()

        elif action == GameActions.EXIT:
            result = self._process_exit()

        elif action == GameActions.START:
            result = self._process_start()

        else:
            return GameError.INVALID_ACTION
        return result

    def _process_start(self) -> SystemComunication:
        """
        Processa a ação de `start`.

        Returns:
            SystemWarning: Indica um aviso do sistema.
        """
        result = self._validate_start_action()
        if was_successful(result):
            self.status = GameStatus.READY_TO_START
            return ServerWarning.GAME_READY_TO_START
        return result

    def _process_restart(self) -> ValidationResult:
        """
        Processa a ação `restart`.

        Returns:
            ValidationResult: Resultado do processamento.
                - GameError.GAME_NOT_STARTED: Indica que o
                    jogo ainda não começou.
                - GameWarning.OK: Indica sucesso do processamento.
        """
        validation = self._validate_restart()
        if was_successful(validation):
            self.status = GameStatus.WAITING
            self.game.reset()
        return validation

    def _process_exit(self) -> ServerWarning:
        """
        Processa a ação `exit`.

        Returns:
            ServerWarning: Indica um aviso ao Server.
            - ServerWarning.DISCONNECT_CLIENT: Indica
                que o player em questão, quer se desconectar.
        """
        self.status = GameStatus.FINISHED
        return ServerWarning.DISCONNECT_CLIENT

    def _process_make_movement(
        self,
        payload: PayLoad
        ) -> ValidationResult:
        """
        Processa a ação `make_movement`.

        Args:
            payload (PayLoad): Informação útil para o
                processamento.

        Returns:
            ValidationResult: Indica o resultado da validação.
                - GameWarning.WINNER_REACHED
                - GameError.INVALID_SLOT
                - GameError.OCCUPIED_SLOT
                - GameWarning.OK

        **Note**:
            Veja `GameWarning.__doc__` ou `GameError.__doc__`
            para ver o significa de cada retorno.
        """
        result = payload.get(
            "slot",
            GameError.GAME_ACTION_ERROR
        )
        if not isinstance(result, int):
            return result

        validation = self._validate_movement_action(result)
        if was_successful(validation):
            self.game.make_movement(result)
            # winner = self.game.check_winner(with_symbols=True)
            # if isinstance(winner, GameSymbols):
            #     self.winner = winner
            #     self.status = GameStatus.FINISHED
            #     return GameWarning.WINNER_REACHED
        return validation

#! ========= VALIDATIONS =========

    def _validate_restart(self) -> ValidationResult:
        """
        Realiza validações em relação a ação de restart.

        Returns:
            ValidationResult: Indica o resultado da validação.
                - GameError.GAME_NOT_STARTED: Indica que o
                    jogo ainda não começou.
                - GameWarning.OK: Indica sucesso da validação.
        """
        if self.status in [GameStatus.READY_TO_START, GameStatus.WAITING]:
            return GameError.GAME_NOT_STARTED
        return GameWarning.OK

    def _validate_player_symbol(
        self,
        symbol: GameSymbols
        ) -> ValidationResult:
        """
        Realiza validações em relação a escolha do símbolo
        para um jogador.

        Args:
            symbol (GameSymbols): Símbolo escolhido.

        Returns:
            ValidationRetult: Erro ou sucesso da validação.
                - GameError.SYMBOL_ALREADY_SELECTED: Indica que
                    o símbolo já foi escolhido por outro jogador.
                - GameWarning.OK: Indica que o símbolo está disponível
                    para uso.
        """
        if any(player["symbol"] == symbol for player in self.players):
            return GameError.SYMBOL_ALREADY_SELECTED
        return GameWarning.OK

    def _validate_change_players_action(
        self,
        player_id: PlayerId
        ) -> ValidationResult:
        """
        Realiza as validações relacionadas a troca de
        jogador atual.

        Args:
            player_id (PlayerId): O `id` do jogador que será
                colocado como atual.

        Returns:
            ValidationRetult:
                - GameError.NON_EXISTENT_PLAYER: Indica que o player solicitado
                    não existe no jogo.
                - GameWarning.OK: Indica nenhum problema na ação.
        """
        player = self.get_player(player_id)
        if player is None:
            return GameError.NON_EXISTENT_PLAYER
        if self.game.current_player == player:
            return GameError.SAME_PLAYER
        return GameWarning.OK

    def _validate_movement_action(
        self,
        slot: int
        ) -> ValidationResult:
        """
        Realiza as validações relacionadas a seleção
        de slot no tabuleiro.

        Args:
            slot (int): O slot escolhido do tabuleiro.

        Returns:
            ValidationResult: Resultado da validação.
                - GameWarning.WINNER_REACHED
                - GameError.INVALID_SLOT
                - GameError.OCCUPIED_SLOT
                - GameWarning.OK

        **Note**
            Veja o `.__doc__` do retorno para ver mais informações.
        """
        if self.winner is not None: # Já tem um vencedor
            return GameWarning.WINNER_REACHED
        if not 0 <= slot < len(self.game.board): # Slot fora do intervalo
            return GameError.INVALID_SLOT
        if self.game.board[slot] is not None: # Slot usado
            return GameError.OCCUPIED_SLOT
        return GameWarning.OK # Tudo certo

    def _validate_start_action(self) -> ValidationResult:
        """
        Realiza validações em relação a ação de começar o jogo.

        Returns:
            ValidationReult: O resultado da validação.
                - GameError.GAME_HAS_STARTED: Indica que o jogo
                    já começou.
                - GameError.INSUFFICIENT_PLAYERS: Indica que não
                    tem players suficiente para começar uma partida.
                - GameWarning.OK: Indica nenhum problema na ação.
        """
        if len(self.players) < 2:
            return GameError.INSUFFICIENT_PLAYERS
        was_started = self.status == GameStatus.ONGOING
        if was_started or (self.winner is not None and self.board_was_used()):
            return GameError.GAME_HAS_STARTED
        return GameWarning.OK

#! ========= SETTERS =========

    def set_current_player(
        self,
        player_id: PlayerId
        ) -> ValidationResult:
        """
        Define um jogador atual.

        Args:
            player_id (PlayerId): Id do jogador.

        Returns:
            ValidationResult: Resultado da ação.
                - GameError.NON_EXISTENT_PLAYER: O `player_id`
                    não existe.
                - GameWarning.OK: Sucesso na operação.
        """
        player = self.get_player(player_id)
        if player is not None:
            self.game.set_current_player(player["symbol"])
            return GameWarning.OK
        return GameError.NON_EXISTENT_PLAYER

#! ========= PREDICATES =========

    def is_current_state(self, expected_status: GameStatus) -> bool:
        """
        Verifica se o estado atual é um esperado.

        Args:
            expected_status (GameStatus): Status atual
                esperado.

        Returns:
            bool: True, se o status atual é o esperado,
                caso contrário, False.
        """
        return was_successful(expected_status, self.status)

    def slot_was_used(self, slot: int) -> bool:
        """
        Verifica se um slot especificado já
        foi usado.

        Args:
            slot (int): Slot procurado.

        Returns:
            bool: True, caso o slot foi usado, False
                caso contrário.
        """
        return self.game.board[slot] is not None

    def board_was_used(self) -> bool:
        """
        Verifica algum slot do tabuleiro foi usado.

        Returns:
            bool: True, caso ele tenha algum slot é
            diferente de None, caso contrário, False.
        """
        return any(slot is not None for slot in self.game.board)

    def in_player_list(
        self,
        player_id: PlayerId
        ) -> bool:
        """
        Verifica se um id está na lista de players.

        Args:
            player_id (PlayerId): Id do player procurado.

        Returns:
            bool: True, se o player estiver na lista, False
                para se ele não estiver.
        """
        return self.get_player(player_id) is not None

#! ========= GETTERS =========

    def get_player_id(self, symbol: GameSymbols) -> Optional[int]:
        """
        Pega o id de um player com base no símbolo dele.

        Args:
            symbol (GameSymbols): Símbolo procurado.

        Returns:
            (int | None): Resultado da procura.
                - int: O id encontrado;
                - None: Nenhum jogador foi encontrado.
        """
        return next(
            (
                player["id"] for player in self.players if player["symbol"] == symbol
            ), None
        )

    def get_current_player(self) -> Optional[PlayerId]:
        """
        Pega o player do turno atual.

        Returns:
            (PlayerId | None): O Id do jogador atual, ou
                None para nenhum jogador.
        """
        current_player = self.game.current_player
        if current_player is not None:
            symbol = self.game.get_player_repr(current_player)
            return self.get_player_id(symbol)
        return None

    def get_player(self, player_id: PlayerId) -> Optional[PlayerDict]:
        """
        Procura um player pelo id.

        Args:
            player_id (PlayerId): Id do player procurado.

        Returns:
            (PlayerDict | None): As informações do player,
                ou None para nenhum player encontrado.
        """
        return next(
            (
                player for player in self.players if player["id"] == player_id
            ), None
        )

    def _get_error_return(
        self,
        value: SystemComunication
        ) -> Optional[SystemComunication]:
        """
        Verifica se um retorno indica um erro.
        Seguindo GameWarning e SystemWarning.

        Args:
            value (SystemComunication): O valor que será validado
                como erro ou seguro.

        Returns:
            (SystemComunication | None): O erro detectado, caso
                contrário, None.
        """
        safe_return = [
            GameWarning.OK,
            ServerWarning.GAME_READY_TO_START,
            ServerWarning.DISCONNECT_CLIENT
        ]
        return value if value not in safe_return else None
