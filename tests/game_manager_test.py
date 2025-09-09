import unittest
import os
import sys
import socket
from rich.traceback import install

install()

root_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(root_dir)

from src.managers.game_manager import GameManager
from src.core.config import GameSymbols
from src.protocols.enums import GameWarning, GameActions, GameStatus
from src.protocols.errors import GameError
from src.core.types import SystemMessage, ServerWarning
from src.utils.validation_utils import was_message_successful, was_successful

class TestGameManager(unittest.TestCase):

    def setUp(self) -> None:
        self.gm = GameManager()
        self.client1 = socket.socket()
        self.client2 = socket.socket()
        self.client3 = socket.socket()
        self.player1 = {
            "player_name": "Sato",
            "symbol": GameSymbols.CIRCLE,
            "client": self.client1
            }
        self.player2 = {
            "player_name": "Diogo",
            "symbol": GameSymbols.CROSS,
            "client": self.client2
            }
        self.player3 = {
            "player_name": "Input",
            "symbol": GameSymbols.CIRCLE,
            "client": self.client3
            }

    def test_switch_current_player(self) -> None:
        self.gm.add_player(**self.player1)
        self.gm.add_player(**self.player2)

        # Sem parâmetros, pega o primeiro jogador adicionado
        self.gm.switch_current_player()
        first_current_player = self.gm.get_player(self.gm.get_current_player())

        # Pega o próximo player automaticamente
        self.gm.switch_current_player()
        second_current_player = self.gm.get_player(self.gm.get_current_player())

        success = (
            was_successful(first_current_player["symbol"], self.player1["symbol"]),
            was_successful(second_current_player["symbol"], self.player2["symbol"])
        )
        self.assertTupleEqual(success, (True, True))

    def test_apply_action_exit_in_game(self) -> None:
        success = (False, False)
        self.gm.add_player(**self.player1)
        self.gm.add_player(**self.player2)

        # Simula começo de partida e seleção de jogadores
        player1_id = self.gm.get_player_id(self.player1["symbol"])
        slot = 0
        # print("Começando")
        if player1_id is not None:
            # print("Primeiro IF")
            self.gm.set_current_player(player1_id)
            message_start: SystemMessage = {
                "type": GameActions.START,
                "payload": {}
                }
            return_start = self.gm.apply_action(message_start)
            if was_message_successful(return_start):
                # print("Segundo IF")
                message_make_movement: SystemMessage = {
                    "type": GameActions.MAKE_MOVEMENT,
                    "payload": {"slot": slot}
                }
                self.gm.apply_action(message_make_movement)

                message_exit: SystemMessage = {
                    "type": GameActions.EXIT,
                    "payload": {}
                }
                return_exit = self.gm.apply_action(message_exit).get("type", {})
                success = (
                    self.gm.is_current_state(GameStatus.FINISHED),
                    was_successful(return_exit, ServerWarning.DISCONNECT_CLIENT.value)
                )
        self.assertTupleEqual(success, (True, True))

    def test_apply_action_exit(self) -> None:
        self.gm.add_player(**self.player1)
        self.gm.add_player(**self.player2)

        message_exit: SystemMessage = {
            "type": GameActions.EXIT,
            "payload": {}
        }
        return_exit = self.gm.apply_action(message_exit).get("type", {})
        success = (
            self.gm.is_current_state(GameStatus.FINISHED),
            was_successful(return_exit, ServerWarning.DISCONNECT_CLIENT.value)
        )
        self.assertTupleEqual(success, (True, True))

    def test_apply_action_start(self) -> None:
        self.gm.add_player(**self.player1)
        self.gm.add_player(**self.player2)

        message_start: SystemMessage = {
            "type": GameActions.START,
            "payload": {}
        }
        return_start = self.gm.apply_action(message_start)
        if return_start["type"] == ServerWarning.GAME_READY_TO_START.value:
            self.gm.start_game()
        self.assertTrue(self.gm.is_current_state(GameStatus.ONGOING))

    def test_apply_action_restart(self) -> None:
        success = (False, False, False)
        self.gm.add_player(**self.player1)
        self.gm.add_player(**self.player2)

        message_start: SystemMessage = {
            "type": GameActions.START,
            "payload": {}
        }
        return_start = self.gm.apply_action(message_start)

        if return_start["type"] == ServerWarning.GAME_READY_TO_START.value:
            self.gm.start_game()

            player_id = self.gm.get_player_id(self.player1["symbol"])
            if player_id is not None:
                self.gm.set_current_player(player_id)
                slot = 0
                message_make_movement: SystemMessage = {
                    "type": GameActions.MAKE_MOVEMENT,
                    "payload": {"slot": slot}
                }
                return_make_movement = self.gm.apply_action(message_make_movement)
                if was_message_successful(return_make_movement): # Movimento
                    message_restart: SystemMessage = {
                        "type": GameActions.RESTART,
                        "payload": {}
                    }
                    has_change_board = self.gm.board_was_used()
                    slot_used = self.gm.slot_was_used(slot)
                    return_restart = self.gm.apply_action(message_restart)
                    if was_message_successful(return_restart): # Restart
                        was_restarted = self.gm.is_current_state(GameStatus.WAITING)
                        success = (has_change_board, slot_used, was_restarted)
        self.assertTupleEqual(success, (True, True, True))

    def test_apply_action_make_movement(self) -> None:
        sucess = (False, False)
        self.gm.add_player(**self.player1)
        self.gm.add_player(**self.player2)
        # Simula começo de partida e seleção de jogadores
        player1_id = self.gm.get_player_id(self.player1["symbol"])
        slot = 0
        # print("Começando")
        if player1_id is not None:
            # print("Primeiro IF")
            self.gm.set_current_player(player1_id)
            message_start: SystemMessage = {
                "type": GameActions.START,
                "payload": {}
                }
            return_start = self.gm.apply_action(message_start)
            if was_message_successful(return_start):
                # print("Segundo IF")
                message_make_movement: SystemMessage = {
                    "type": GameActions.MAKE_MOVEMENT,
                    "payload": {"slot": slot}
                }
                return_make_movement = self.gm.apply_action(message_make_movement)
                if was_message_successful(return_make_movement):
                    # print("Terceiro IF")
                    has_change_board = self.gm.board_was_used()
                    slot_used = self.gm.slot_was_used(slot)
                    sucess = (has_change_board, slot_used)
        self.assertTupleEqual(sucess, (True, True))

    def test_remove_player_error_non_existent_player(self) -> None:
        self.gm.add_player(**self.player1)
        self.gm.add_player(**self.player2)
        return_1 = self.gm.remove_player(991959)
        self.assertEqual(return_1, GameError.NON_EXISTENT_PLAYER)

    def test_remove_player_error_party_empty(self) -> None:
        return_1 = self.gm.remove_player(10)
        self.assertEqual(return_1, GameError.EMPTY_PARTY)

    def test_remove_player(self) -> None:
        self.gm.add_player(**self.player1)
        self.gm.add_player(**self.player2)
        player2_id = self.gm.get_player_id(GameSymbols.CROSS)
        return_1, return_2 = None, None
        if isinstance(player2_id, int):
            return_1 = self.gm.in_player_list(player2_id)
            self.gm.remove_player(player2_id)
            return_2 = self.gm.in_player_list(player2_id)
        self.assertTupleEqual((return_1, return_2), (True, False))

    def test_add_player_sucess(self) -> None:
        return_1 = self.gm.add_player(**self.player1)
        return_2 = self.gm.add_player(**self.player2)
        self.assertTupleEqual((return_1, return_2), (GameWarning.OK, GameWarning.OK))

    def test_add_player_error_full_party(self) -> None:
        return_1 = self.gm.add_player(**self.player1)
        return_2 = self.gm.add_player(**self.player2)
        return_3 = self.gm.add_player(**self.player3)
        self.assertTupleEqual(
            (return_1, return_2, return_3),
            (GameWarning.OK, GameWarning.OK, GameError.FULL_PARTY)
            )

    def test_add_player_error_already_symbol_selected(self) -> None:
        return_1 = self.gm.add_player(**self.player1)
        return_2 = self.gm.add_player(**self.player3)
        self.assertTupleEqual(
            (return_1, return_2),
            (GameWarning.OK, GameError.SYMBOL_ALREADY_SELECTED)
        )

    def tearDown(self) -> None:
        self.gm.reset_all()

if __name__ == "__main__":
    suite = unittest.TestSuite()
    all_methods = unittest.defaultTestLoader.loadTestsFromTestCase(TestGameManager)
    suite.addTest(all_methods)
    runner = unittest.TextTestRunner()
    runner.run(suite)
