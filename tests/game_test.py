import unittest
import os
import sys
from random import choice, randint
from rich.traceback import install


install()

root_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(root_dir)

from src.core.game import TicTacToe
from src.core.config import GameSymbols
from src.core.exceptions import DrawError

class TestTicTacToe(unittest.TestCase):

    def setUp(self) -> None:
        self.game = TicTacToe()
        self.player1 = GameSymbols.CIRCLE
        self.player2 = GameSymbols.CROSS
        self.win_movements = [0, 1, 2]
        self.loose_movements = [3, 6, 7]

    def test_player1_win(self) -> None:
        #   0 | 1 | 2
        #   3 | 4 | 5
        #   6 | 7 | 9
        for p1, p2 in zip(self.win_movements, self.loose_movements):
            self.game.set_current_player(self.player1)
            self.game.make_movement(p1)
            self.game.set_current_player(self.player2)
            self.game.make_movement(p2)
        # self.game.show_board()
        winner = self.game.check_winner(with_symbols=True)
        self.assertTrue(winner == self.player1)

    def test_player2_win(self) -> None:
        #   0 | 1 | 2
        #   3 | 4 | 5
        #   6 | 7 | 8
        for p1, p2 in zip(self.loose_movements, self.win_movements):
            self.game.set_current_player(self.player1)
            self.game.make_movement(p1)
            self.game.set_current_player(self.player2)
            self.game.make_movement(p2)
        # self.game.show_board()
        winner = self.game.check_winner(with_symbols=True)
        self.assertTrue(winner == self.player2)

    def test_draw(self) -> None:
        movements1 = [0, 1, 4, 5, 6]
        movements2 = [2, 3, 7, 8, 0]
        with self.assertRaises(DrawError):
            for p1, p2 in zip(movements1, movements2):
                self.game.set_current_player(self.player1)
                self.game.make_movement(p1)
                self.game.set_current_player(self.player2)
                self.game.make_movement(p2)
            self.game.check_winner()

    def test_simulation_round(self) -> None:
        players = [self.player1, self.player2]
        attemps = 5
        while attemps > 0:
            winner = None
            i = randint(0, 1)
            player = players[i]
            print(f"Começa com {player.value.upper()}")
            try:
                avaliable_slots = list(range(0, 9)) # Slots disponíveis 0-9
                while avaliable_slots and winner is None:
                    # Pega um número aleatório dentro dos válidos
                    slot = choice(avaliable_slots)
                    # Usa o slot e tira dos disponíveis
                    avaliable_slots.remove(slot)

                    # Seleciona um player
                    player = players[i]
                    self.game.set_current_player(player)
                    # Faz uma jogada
                    self.game.make_movement(slot)
                    # Garante o próximo player
                    i = (i + 1) % len(players)
                    winner = self.game.check_winner(with_symbols=True)
            except DrawError:
                self.game.show_board()
                print("O jogo terminou com EMPATE", end="\n\n")
            self.game.show_board()
            if isinstance(winner, GameSymbols):
                print(f"Vencedor: {winner.value.upper()}")
            self.game.reset()
            attemps -= 1

if __name__ == "__main__":
    suite = unittest.TestSuite()
    all_methods = unittest.defaultTestLoader.loadTestsFromTestCase(TestTicTacToe)
    test_draw = TestTicTacToe("test_draw")
    simulation = TestTicTacToe("test_simulation_round")
    suite.addTest(simulation)
    runner = unittest.TextTestRunner()
    runner.run(suite)
