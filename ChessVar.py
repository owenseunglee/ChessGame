# Author: Owen Lee
# GitHub username: owenseunglee
# Date: 08/17/2023
# Description:  This program contains an abstract board game that is a variant of chess. As in standard chess, white
#               moves first. The first player to move their king onto row 8 is the winner, unless black finishes the
#               next move after white does, in which case it's a tie. Pieces move and capture the same as in standard
#               chess. As in standard chess, a player is not allowed to expose their own king to check (including
#               moving a piece that was blocking a check such that it no longer does). Unlike standard chess, a player
#               is not allowed to put the opponent's king in check (including moving a piece that was blocking a check
#               such that it no longer does). Locations on the board will be specified using "algebraic notation", with
#               columns labeled a-h and rows labeled 1-8, with row 1 being the start side and row 8 the finish side.

class Piece:
    """ A parent class that represents chess pieces"""
    def __init__(self, name, color, pos):
        self._color = color
        self._type = name
        self._pos = pos

    def get_color(self):
        """ A get method to get the piece color"""
        return self._color

    def get_type(self):
        """ A get method to get the piece type"""
        return self._type

    def get_pos(self):
        """ A get method to get the piece position"""
        return self._pos

    def is_legal(self, end_piece, current_pos, end_pos, board, board_obj):
        """ This method will check movement validation for chess pieces"""
        raise NotImplementedError("This method is implemented under the inherited classes")


class King(Piece):
    """ A class that represents King"""
    def __init__(self, color, pos):
        super().__init__("King", color, pos)

    def is_legal(self, end_piece, current_pos, end_pos, board, board_obj):
        """ Overriden method to validate the King's movement"""

        # separate the column and the row number and assign them to different variables
        current_col, current_row = ord(current_pos[0]), int(current_pos[1])
        end_col, end_row = ord(end_pos[0]), int(end_pos[1])

        row_diff = 0
        col_diff = 0

        # calculate the row difference
        if current_row > end_row:
            row_diff = current_row - end_row
        elif current_row < end_row:
            row_diff = end_row - current_row

        # calculate the column difference
        if current_col > end_col:
            col_diff = current_col - end_col
        elif current_col < end_col or current_col == end_col:
            col_diff = end_col - current_col

        # check if the King only moves 1 tile/board in every direction
        if row_diff == 1 or row_diff == 0:
            if col_diff == 1 or col_diff == 0:
                return True
        else:
            return False


class Bishop(Piece):
    def __init__(self, color, pos):
        super().__init__("Bishop", color, pos)

    def is_legal(self, end_piece, current_pos, end_pos, board, board_obj):
        """ Overriden method to validate the Bishop's movement"""

        # separate the column and the row number and assign them to different variables
        current_col, current_row = ord(current_pos[0]), int(current_pos[1])
        end_col, end_row = ord(end_pos[0]), int(end_pos[1])

        # column a - h, negative means moving leftward
        col_diff = end_col - current_col
        # row 1 - 8, negative means moving downward
        row_diff = end_row - current_row

        # Bishops cannot move horizontally, vertically or different on absolute value of row and columns
        if (current_col == end_col or current_row == end_row) or (abs(row_diff) != abs(col_diff)):
            return False

        row_step = 0
        col_step = 0

        # assign appropriate difference to take depending on differences of column and row
        if col_diff > 0 and row_diff > 0: # check
            # moving quad 2
            col_step = 1
            row_step = -1
        elif col_diff < 0 and row_diff < 0:
            # moving quadrant 4
            col_step = -1
            row_step = 1
        elif col_diff < 0 < row_diff: # check
            # moving quad 3
            col_step = -1
            row_step = -1
        elif col_diff > 0 > row_diff: # check
            # moving quad 1
            col_step = 1
            row_step = 1
        # check for blocked path, it will return value of True when a piece is blocking the path
        path_check = self.is_path_blocked(current_col, current_row, end_col, end_row, row_step, col_diff, row_diff, col_step,
                                          board)
        if path_check:
                # return False, telling that it is not a valid move
            return False

        else:
            return True

    def is_path_blocked(self, current_col, current_row, end_col, end_row, row_step, col_diff, row_diff, col_step, board):
        """ A method to check if the Bishop's path is blocked"""
        current_row_num = current_row
        current_col_num = 0

        # column conversion table
        if current_col == 97:
            current_col_num = 0
        elif current_col == 98:
            current_col_num = 1
        elif current_col == 99:
            current_col_num = 2
        elif current_col == 100:
            current_col_num = 3
        elif current_col == 101:
            current_col_num = 4
        elif current_col == 102:
            current_col_num = 5
        elif current_col == 103:
            current_col_num = 6
        elif current_col == 104:
            current_col_num = 7
        # row conversion table
        if current_row == 8:
            current_row = 0
        elif current_row == 7:
            current_row = 1
        elif current_row == 6:
            current_row = 2
        elif current_row == 5:
            current_row = 3
        elif current_row == 4:
            current_row = 4
        elif current_row == 3:
            current_row = 5
        elif current_row == 2:
            current_row = 6
        elif current_row == 1:
            current_row = 7

        # check for Bishop's movement in quadrant 2
        if col_diff > 0 and row_diff > 0:
            current_row_num = current_row_num + col_step # check
            current_row = current_row + row_step # check
            current_col = current_col + col_step # check
            current_col_num = current_col_num + col_step # check
            # traverse through until starting and ending points meet
            while current_col != end_col and current_row != end_row:
                if board[current_row][current_col_num].get(f"{chr(current_col)}{str(current_row_num)}") is not None:
                    return True

                # increment each values to bring up values from each indexes
                current_row = current_row + row_step
                current_col = current_col + col_step
                current_col_num = current_col_num + col_step
                current_row_num = current_row_num + col_step

        # check for Bishop's movement in quadrant 3
        elif col_diff < 0 < row_diff:
            current_row_num = current_row_num + 1
            current_row = current_row + row_step
            current_col = current_col + col_step
            current_col_num = current_col_num + col_step

            while current_col != end_col:
                if board[current_row][current_col_num].get(f"{chr(current_col)}{str(current_row_num)}") is not None:
                    return True

                current_row = current_row + row_step
                current_col = current_col + col_step
                current_col_num = current_col_num + col_step
                current_row_num = current_row_num + 1

        # check for Bishop's movement in quadrant 1
        elif col_diff > 0 > row_diff:
            current_row_num = current_row_num - 1 # just fixed
            current_row = current_row + row_step
            current_col = current_col + col_step
            current_col_num = current_col_num + col_step

            while current_col != end_col:
                if board[current_row][current_col_num].get(f"{chr(current_col)}{str(current_row_num)}") is not None:
                    return True

                current_row = current_row + row_step
                current_col = current_col + col_step
                current_col_num = current_col_num - 1
                current_row_num = current_row_num + row_step

        # check for Bishop's movement in quadrant 4
        elif col_diff < 0 and row_diff < 0:
            current_row_num = current_row_num + col_step
            current_row = current_row + row_step
            current_col = current_col + col_step
            current_col_num = current_col_num + col_step

            while current_col != end_col and current_row != end_row:
                if board[current_row][current_col_num].get(f"{chr(current_col)}{str(current_row_num)}") is not None:
                    pos_check = board[current_row][current_col_num].get(f"{chr(current_col)}{str(current_row_num)}")
                    return True
                current_row = current_row + row_step
                current_col = current_col + col_step
                current_col_num = current_col_num + col_step
                current_row_num = current_row_num + row_step
        return False


class Knight(Piece):
    def __init__(self, color, pos):
        super().__init__("Knight", color, pos)

    def is_legal(self, end_piece, current_pos, end_pos, board, board_obj):
        """ Overriden method to validate the Knight's movement"""
        # separate the columns and the rows
        current_col, current_row = ord(current_pos[0]), int(current_pos[1])
        end_col, end_row = ord(end_pos[0]), int(end_pos[1])

        col_diff = end_col - current_col
        row_diff = end_row - current_row
        # Knight cannot move horizontally nor vertically
        if current_pos[0] == end_pos[0] or current_pos[1] == end_pos[1]:
            return False
        # check for Knight's legal movement
        elif col_diff == 2 or col_diff == -2:
            if row_diff != 1 and row_diff != -1:
                return False
            else:
                return True

        elif col_diff == 1 or col_diff == -1:
            if row_diff != 2 and row_diff != -2:
                return False
            else:
                return True


class Rook(Piece):
    def __init__(self, color, pos):
        super().__init__("Rook", color, pos)

    def is_legal(self, end_piece, current_pos, end_pos, board, board_obj):
        """ Overriden method to validate the Rook's movement"""
        # separate the columns and the rows
        current_col, current_row = ord(current_pos[0]), int(current_pos[1])
        end_col, end_row = ord(end_pos[0]), int(end_pos[1])
        # negative means moving leftward
        col_diff = end_col - current_col
        # negative means moving downward
        row_diff = end_row - current_row

        # check if the Rook is moving only vertically or horizontally
        if col_diff == 0 or row_diff == 0:
            # check for blocked path
            path_check = self.is_path_blocked(current_col, end_col, current_row, end_row, col_diff, row_diff, board)
            if path_check:
                # if blocked path, return false
                return False

            else:
                return True

        return False

    def is_path_blocked(self, current_col, end_col, current_row, end_row, col_diff, row_diff, board):
        # check for board's rows and columns range
        current_col_num = current_col
        current_row_num = current_row
        # column conversion table
        if current_col == 97:
            current_col_num = 0
        elif current_col == 98:
            current_col_num = 1
        elif current_col == 99:
            current_col_num = 2
        elif current_col == 100:
            current_col_num = 3
        elif current_col == 101:
            current_col_num = 4
        elif current_col == 102:
            current_col_num = 5
        elif current_col == 103:
            current_col_num = 6
        elif current_col == 104:
            current_col_num = 7
        # row conversion table
        if current_row == 8:
            current_row = 0
        elif current_row == 7:
            current_row = 1
        elif current_row == 6:
            current_row = 2
        elif current_row == 5:
            current_row = 3
        elif current_row == 4:
            current_row = 4
        elif current_row == 3:
            current_row = 5
        elif current_row == 2:
            current_row = 6
        elif current_row == 1:
            current_row = 7

        # checking for left or right movement
        if col_diff != 0 and row_diff == 0:
            # positive means moving right
            if col_diff > 0:
                col_step = 1

            else:
                col_step = -1
            current_col_num = current_col_num + col_step
            current_col = current_col + col_step
            # check until starting column number meets ending column number
            while current_col != end_col:
                # check left/right tile for a piece
                if board[current_row][current_col_num].get(f"{chr(current_col)}{str(current_row)}") is not None:
                    return True
                # otherwise keep checking next tiles
                current_col_num = current_col_num + col_step
                current_col = current_col + col_step

        # checking for up or down movement
        if row_diff != 0 and col_diff == 0:
            # positive means moving upward
            if row_diff > 0:
                # rows will decrease
                row_step = -1
                # rows for keys will increase
                row_num_step = 1

            else:
                row_step = 1
                row_num_step = -1
            # add one to start from the next movable tile
            current_row = current_row + row_step
            current_row_num = current_row_num + row_num_step
            # check until starting row number meets ending row number
            while current_row_num != end_row:
                # check right above/below tile for a piece
                if board[current_row][current_col_num].get(f"{chr(current_col)}{str(current_row_num)}") is not None:
                    return True
                # otherwise keep checking next tiles
                current_row = current_row + row_step
                current_row_num = current_row_num + row_num_step

        return False



class ChessVar:
    """ A class that represents """
    def __init__(self):
        self._board_obj = self.chess_board()
        self._game_state = 'UNFINISHED'
        self._player_turn = 'white'
        self._next_turn = 'None'
        self._white_king_reached_row_8 = False
        self._black_king_reached_row_8 = False

    def make_move(self, start_pos, end_pos):

        # check game status
        if self._game_state in ["WHITE_WON", "BLACK_WON", "TIE"]:
            return False
        # assign the board from Board object
        board = self.get_board()

        start_piece = None
        end_piece = None

        # get piece object
        for row in board:
            for column in row:
                if start_pos in column:
                    start_piece = column[start_pos]

                if end_pos in column:
                    end_piece = column[end_pos]

        # check player's turn
        # returns true if correct player's turn
        check_player_turn = self.is_player_turn(start_piece, start_pos)

        # check piece's legal movement
        # returns true if legal movement
        validation_check = self.is_valid(start_piece, end_piece, start_pos, end_pos, board, self._board_obj)

        # check for correct player's turn and legal movement for pieces
        if check_player_turn and validation_check:
            # update the board
            self.update_board(start_piece, start_pos, end_pos, board)
            # update game state/player's turn
            self.update_game_state(self._player_turn, end_pos, board)
            return True

        else:
            return False

    def chess_board(self):
        # labels for rows and columns
        rows = list(range(1, 9))
        columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        # create 2d list
        chess_board = [['_' for _ in range(8)] for _ in range(8)]

        # label indexes with rows and columns
        for row in rows:
            for column in range(len(columns)):
                col_letter = columns[column]
                key = f"{col_letter}{row}"
                value = None
                # since rows are decrementing, subtract row from 8, which is the max row number
                row_index = 8 - row
                col_index = column
                # create dictionaries for 2d list
                piece = {key: value}
                chess_board[row_index][col_index] = piece

        # Initialize chess pieces and place chess pieces on designated places
        chess_board[7][0] = {'a1': King('white', 'a1')}
        chess_board[6][0] = {'a2': Rook('white', 'a2')}
        chess_board[7][1] = {'b1': Bishop('white', 'b1')}
        chess_board[6][1] = {'b2': Bishop('white', 'b2')}
        chess_board[7][2] = {'c1': Knight('white', 'c1')}
        chess_board[6][2] = {'c2': Knight('white', 'c2')}
        chess_board[7][5] = {'f1': Knight('black', 'f1')}
        chess_board[6][5] = {'f2': Knight('black', 'f2')}
        chess_board[6][6] = {'g2': Bishop('black', 'g2')}
        chess_board[7][6] = {'g1': Bishop('black', 'g1')}
        chess_board[6][7] = {'h2': Rook('black', 'h1')}
        chess_board[7][7] = {'h1': King('black', 'h2')}
        return chess_board

    def display(self):
        """ A method to display the chess board"""
        for i in self._board_obj:
            print(i)

    def get_board(self):
        """ A get method to get the chess board"""
        return self._board_obj

    def set_update_board(self, board):
        """ A set method to set the updated board to initial board"""
        self._board_obj = board

    def update_board(self, start_piece, start_pos, end_pos, board):
        """ A method to update the board when the player has made a move"""

        # separate the column and the row
        col_start, row_start = start_pos[0], int(start_pos[1])
        col_end, row_end = end_pos[0], int(end_pos[1])
        row_start_index = 8 - row_start
        row_end_index = 8 - row_end
        col_start_index = ord(col_start) - ord('a')
        col_end_index = ord(col_end) - ord('a')

        # automatically remove captured piece if the piece color is different
        board[row_end_index][col_end_index] = {end_pos: start_piece}
        # change starting position to None
        board[row_start_index][col_start_index] = {start_pos: None}

        self.set_update_board(board)

    def get_piece(self, pos):
        """ A get method to get the pieces"""
        col, row = pos[0], int(pos[1])
        row_index = 8 - row
        col_index = ord(col) - ord('a')

        return self._board_obj[row_index][col_index][pos]



    def is_player_turn(self, start_piece, start_pos):
        """ A method to check correct player's turn """
        # check if the player entered the correct starting position
        if not (len(start_pos) == 2 and 'a' <= start_pos[0] <= 'h' and '1' <= start_pos[1] <= '8'):
            return False
        # assign color of the piece
        check_turn = start_piece.get_color()
        # check for correct player's turn
        if check_turn == self._player_turn:
            return True

        else:
            return False

    def is_valid(self, start_piece, end_piece, start_pos, end_pos, board, board_obj):
        # check starting position and end position
        if start_pos == end_pos or start_pos is None or start_piece is None:
            return False
        # check the existence of both start_piece and end_piece
        if start_piece is not None and end_piece is not None:
            # check if they have the same color
            if start_piece.get_color() == end_piece.get_color() or end_piece.get_type() == 'King':
                return False

            # check for legal movement and blocked path
            check_valid = start_piece.is_legal(end_piece, start_pos, end_pos, board, board_obj)
            if check_valid:
                return True

            else:
                return False

        # check condition for moving one piece to an empty space
        elif start_piece is not None and end_piece is None:
            # check for legal movement and blocked path
            check_valid = start_piece.is_legal(end_piece, start_pos, end_pos, board, board_obj)
            if check_valid:
                return True

            else:
                return False

    def update_game_state(self, player_turn, end_pos, board):
        """ A method to update the player's turn"""

        end_index = int(end_pos[1])
        # check if the type of the piece on row8 is King
        if end_index == 8 and board[0][ord(end_pos[0]) - ord('a')][end_pos].get_type() == 'King':
            # check for color
            if self._player_turn == 'white':
                self._white_king_reached_row_8 = True
            elif self._player_turn == 'black':
                self._black_king_reached_row_8 = True

        # check if the white King is on row8
        if self._white_king_reached_row_8 and not self._black_king_reached_row_8:
            if self._player_turn == 'white':
                is_black_in_row7 = False
                # traverse through row7
                for i in range(8):
                    pos = f"{chr(ord('a') + i)}7"
                    piece = board[1][i][pos]
                    # find and check for black King's existence on row7
                    if piece is not None and piece.get_type() == "King" and piece.get_color() == "black":
                        is_black_in_row7 = True
                        break
                # if black King exists, set the next turn to black and continue the play
                if is_black_in_row7:
                    self._next_turn = 'black'

                else:
                    # if not, white player wins the game
                    self._game_state = 'WHITE_WON'
                    print("White King reached row 0")
        # check condition for black King's position and winning condition
        if self._black_king_reached_row_8 and not self._white_king_reached_row_8:
            if self._player_turn == 'black':
                self._game_state = 'BLACK_WON'
        # check condition for black King's position and winning condition
        if self._black_king_reached_row_8 and self._white_king_reached_row_8:
            if self._player_turn == 'black':
                self._game_state = 'TIE'

        # switch player's color after each turn
        if player_turn == 'white':
            self._player_turn = 'black'
        elif player_turn == 'black':
            self._player_turn = 'white'

    def get_game_state(self):
        """ A get method for game state"""
        return self._game_state

    def get_player_turn(self):
        """ A get method for player's turn"""
        return self._player_turn

    def get_white_black(self):
        return self._white_king_reached_row_8

