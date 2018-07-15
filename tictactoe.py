from num2words import num2words
from utils import rotate_list
import operator
from copy import deepcopy


class TicTacToe:
    PIECE_EMPTY = ":white_medium_square:"
    PIECE_1 = ":heavy_multiplication_x:"
    PIECE_2 = ":o:"

    def __init__(self, p1_name: str, p2_name: str, rows: int=3, columns: int=3):
        self.p1_name = p1_name
        self.p2_name = p2_name
        self.players_turn = p1_name
        self.player_dict = {
            p1_name: TicTacToe.PIECE_1,
            p2_name: TicTacToe.PIECE_2,
        }
        self.current_players_piece = self.player_dict[self.players_turn]
        self.rows = rows
        self.columns = columns
        self.number_in_a_row = 3
        self.playing_board = [[TicTacToe.PIECE_EMPTY] * rows for _ in range(columns)]
        self.turn_count = 0
        self.num_of_pieces_played = 0

    def create_board(self):
        # Create x-axis
        x_axis = [f":regional_indicator_{letter}:"
                  for i, letter in enumerate("abcdefghijklmnopqrstuvwxyz") if i < self.rows]
        playing_board_str = " ".join(x_axis) + "\n"

        # Create rows of empty cells and append a y-axis
        for i, board_row in enumerate(self.playing_board):
            playing_board_str += (" ".join(board_row) + str(f":{num2words(i + 1)}:" + '\n'))

        return playing_board_str

    def place_piece(self, x_position: int, y_position: int):
        x_position = int(x_position) - 1
        y_position = int(y_position) - 1

        piece_on_board = self.playing_board[x_position][y_position]

        if piece_on_board != self.PIECE_EMPTY:
            return False

        self.playing_board[x_position][y_position] = self.current_players_piece

        if self.players_turn == self.p1_name:
            self._increment_turn_count()

        self.num_of_pieces_played += 1

        return True

    def switch_players_turn(self):
        if self.players_turn == self.p1_name:
            self.players_turn = self.p2_name
        else:
            self.players_turn = self.p1_name

        self.current_players_piece = self.player_dict[self.players_turn]

    def check_for_win(self):
        def horiziontal_win():
            for row in self.playing_board:
                if all(piece == self.current_players_piece for piece in row):
                    return True

        def vertical_win(board=None):
            board = board or self.playing_board

            for i in range(self.columns):
                column = [row[i] for row in board]
                if all(piece == self.current_players_piece for piece in column):
                    return True

        def diagonal_up_win():
            return _diagonal_win("+")

        def diagonal_down_win():
            return _diagonal_win("-")

        def _diagonal_win(op):
            ops = {"+": operator.add, "-": operator.sub}

            board_copy = deepcopy(self.playing_board)
            board_copy = [rotate_list(row, ops[op](i, 1)) for i, row in enumerate(board_copy)]

            return vertical_win(board_copy)

        if horiziontal_win() or vertical_win() or diagonal_up_win() or diagonal_down_win():
            return True

    def _increment_turn_count(self):
        self.turn_count += 1
