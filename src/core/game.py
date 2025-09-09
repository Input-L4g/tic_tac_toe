from typing import Tuple, Optional, Union
from src.core.types import GameBoard
from src.core.config import GameSymbols, GAME_REPR_SYMBOLS, VICTORIOUS_INDEX_MOVES
from src.core.exceptions import DrawError, GameEndsError, PlayerNotDefinedError

# Coord no tabuleiro:
# 0 | 1 | 2
# 3 | 4 | 5
# 6 | 7 | 8
# Sendo representado linearmente:
# [0, 1, 2, 3, 4, 5, 6, 7, 8]
# Onde será montado com base na lista linear

def valide_conditions(func):
    """
    Um decorator que verifica as condições necessárias para
    realizar quaisquer ações no jogo.

    Verifica se já existe um vencedor ou se não possui um
    jogador inicial definido.
    """
    def wrapper(self: "TicTacToe", *args, **kwargs):
        if self.winner is not None:
            raise GameEndsError(f"O jogo já acabou, vencedor: {self.get_player_repr(self.winner)}")
        if self.current_player is None:
            raise PlayerNotDefinedError("O player ainda não foi definido!")
        return func(self, *args, **kwargs)
    return wrapper

class TicTacToe:
    """
    Representa um jogo de Jogo da Velha.

    Attributes:
        board (GameBoard): Tabuleiro do jogo. É definido
            com 9 valores inicialmente None;
        current_player (int | None): O player atual. Representado
            por 0 (circle) ou 1 (cross). Inicialmente é None.
    """
    def __init__(self) -> None:
        """Inicializa a classe TicTacToe."""
        self.board: GameBoard = [None] * 9
        self.current_player: Optional[int] = None
        self.winner: Optional[int] = None

#! ========== COMMANDS ==========

    def reset(self) -> None:
        """Reseta todo o tabuleiro e os atributos."""
        self.board = [None] * 9
        self.current_player = None
        self.winner = None

    def show_board(self) -> None:
        """Mostra o tabuleiro com os valores formatados."""
        for i, value in enumerate(self.board):
            end = ' | '
            if i % 3 == 2:
                end = '\n'
            if value is not None:
                value = self.get_player_repr(value).value
            else:
                value = "-"
            print(value, end=end)

    @valide_conditions
    def make_movement(
        self,
        slot: int
        ) -> None:
        """
        Faz um movimento no tabuleiro.

        Args:
            slot (int): Slot do tabuleiro que terá
                o movimento feito. Deve ser de 0 até 8.
        """
        self.board[slot] = self.current_player

    @valide_conditions
    def check_winner(
        self,
        with_symbols: bool = False
        ) -> Optional[Union[int, GameSymbols]]:
        """
        Verifica se tem algum vencedor.

        Args:
            with_symbols (bool): Indica se o retorno deve
                ser formatado para o símbolo do vencedor.
                Por padrão é False.

        Raises:
            DrawError: Indica que não houve nenhum vencedor,
                mesmo após todas as jogadas possíveis.

        Returns:
            (GameSymbols| int | None):
                - GameSymbols: O símbolo do jogador vencedor.
                    será retornado apenas se o parâmetro
                    `with_symbols` for True.
                - int: O jogador vencedor.
                - None: Nenhum vencedor até o momento.
        """
        # Coord no tabuleiro:
        #   1 | 2 | 3
        #   4 | 5 | 6
        #   7 | 8 | 9

        for block in VICTORIOUS_INDEX_MOVES:
            values = self._get_board_block_values(block)
            if None in values:
                continue
            target = values[0]
            if all(target == value for value in values[1:]) and target is not None:
                self.winner = target
                if with_symbols:
                    return self.get_player_repr(self.winner)
                return self.winner
        if None not in self.board:
            raise DrawError("Houve um EMPATE")
        return None


#! ========== SETTERS ==========

    def set_current_player(self, player: GameSymbols) -> None:
        """
        Define um outro jogador como principal.

        Args:
            player (GameSymbols): Símbolo do jogador.
        """
        self.current_player = GAME_REPR_SYMBOLS[player]

#! ========== GETTERS ==========

    def get_player_id(self, repr_symbol: GameSymbols) -> int:
        """
        Pega o id lógico de um jogador pelo símbolo.

        Args:
            repr_symbol (GameSymbols): Símbolo do jogador procurado.

        Returns:
            int: Id lógico do player.
        """
        return GAME_REPR_SYMBOLS[repr_symbol]

    def get_player_repr(self, target: int) -> GameSymbols:
        """
        Pega o símbolo real de um valor no tabuleiro.

        Args:
            target (int): Valor do jogador. Deve
                ser 0 ou 1.

        Returns:
            GameSymbols: Símbolo do valor.
        """
        return next(
            symbol
            for symbol, value in GAME_REPR_SYMBOLS.items()
            if value == target
        )

    def _get_board_block_values(
        self,
        block: Tuple[int, int, int]
        ) -> Tuple[Optional[int], ...]:
        """
        Pega os valores de um determinado bloco
        do tabuleiro.

        Args:
            block(tuple): Bloco do tabuleiro.

        Returns:
            tuple: Valores do bloco.
        """
        return tuple(self.board[i] for i in block)
