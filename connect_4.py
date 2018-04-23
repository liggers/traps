from copy import deepcopy


def rotate_list(list_to_rotate, rotate_num):
    for x in range(rotate_num):
        list_to_rotate.append(list_to_rotate.pop(0))

    return list_to_rotate


class Connect4:
    def __init__(self, player1_name, player2_name):
        self.rows = 6
        self.columns = 7
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.players_turn = player1_name
        self.piece_empty = ':white_circle:'
        self.piece_1 = ':red_circle:'
        self.piece_2 = ':large_blue_circle:'
        self.player_dict = {
            player1_name: self.piece_1,
            player2_name: self.piece_2,
        }
        self.number_in_a_row = 4
        self.list_of_rows = [[self.piece_empty] * self.columns for x in range(self.rows)]
        self.number_of_pieces_played = 0

    def create_board(self):
        result = ''
        for x in self.list_of_rows:
            result += ' '.join(x) + '\n'

        result += (":one: :two: :three: :four: :five: :six: :seven:\n"
                   f"`It is {self.players_turn}'s turn. You are` {self.player_dict[self.players_turn]}\n"
                   f'`Enter a column # to drop a piece`')
        return result

    def drop_piece(self, column_num):
        column_num -= 1
        for index, row in enumerate(reversed(self.list_of_rows)):
            if str(row[column_num]) == str(self.piece_empty):
                row[column_num] = self.player_dict[self.players_turn]
                self.number_of_pieces_played += 1
                return True
        return False

    def switch_players_turn(self):
        if self.players_turn == self.player1_name:
            self.players_turn = self.player2_name
        else:
            self.players_turn = self.player1_name

    def check_for_win(self):
        check_for_win_board = self.list_of_rows[::-1]

        def horizontal_win():
            for row in check_for_win_board:
                for index, piece in enumerate(row):
                    if index > self.columns - self.number_in_a_row:
                        break
                    elif piece == self.player_dict[self.players_turn]:
                        if all(next_piece == self.player_dict[self.players_turn]
                               for next_piece in row[index: self.number_in_a_row + index]):
                            return True
                    else:
                        continue

        def vertical_win():
            for x in range(0, self.columns):
                column = [row[x] for row in check_for_win_board]
                for index, piece in enumerate(column):
                    if index > self.rows - self.number_in_a_row:
                        break
                    elif piece == self.player_dict[self.players_turn]:
                        if all(next_piece == self.player_dict[self.players_turn]
                               for next_piece in column[index: self.number_in_a_row + index]):
                            return True
                    else:
                        continue

        def diagonal_up_win():
            workable_board = deepcopy(check_for_win_board)
            diag_board = [rotate_list(rotate_row, (index + 1)) for index, rotate_row in enumerate(workable_board)]
            for x in range(0, self.columns):
                column = [row[x] for row in diag_board]
                for index, piece in enumerate(column):
                    if index > self.rows - self.number_in_a_row:
                        break
                    elif piece == self.player_dict[self.players_turn]:
                        if all(next_piece == self.player_dict[self.players_turn]
                               for next_piece in column[index: self.number_in_a_row + index]):
                            return True
                    else:
                        continue

        def diagonal_down_win():
            workable_board = deepcopy(check_for_win_board)
            diag_board = [rotate_list(rotate_row, (self.number_in_a_row - index - 1))
                          for index, rotate_row in enumerate(workable_board)]
            for x in range(0, self.columns):
                column = [row[x] for row in diag_board]
                for index, piece in enumerate(column):
                    if index > self.rows - self.number_in_a_row:
                        break
                    elif piece == self.player_dict[self.players_turn]:
                        if all(next_piece == self.player_dict[self.players_turn]
                               for next_piece in column[index: self.number_in_a_row + index]):
                            return True
                    else:
                        continue

        if horizontal_win() or vertical_win() or diagonal_up_win() or diagonal_down_win():
            return True
