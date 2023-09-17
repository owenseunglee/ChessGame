# Author: Owen Lee
# GitHub username: owenseunglee
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

    def is_legal(self, end_piece,  current_col, current_row, end_col, end_row, board):
        """ This method will check movement validation for chess pieces"""


class King(Piece):
    """ A class that represents King"""
    def __init__(self, color, pos):
        super().__init__("King", color, pos)

    def is_legal(self, end_piece,  current_col, current_row, end_col, end_row, board):
        """ Overriden method to validate the King's movement"""
        # calculate the row and column difference
        row_diff = abs(current_row - end_row)
        col_diff = abs(current_col - end_col)

        # check if the King only moves 1 tile/board in every direction
        if row_diff in (0, 1) and col_diff in (0, 1):
            return True

        else:
            return False


class Bishop(Piece):
    def __init__(self, color, pos):
        super().__init__("Bishop", color, pos)

    def is_legal(self, end_piece,  current_col, current_row, end_col, end_row, board):
        """ Overriden method to validate the Bishop's movement"""
        # column a - h, negative means moving leftward
        col_diff = end_col - current_col
        # row 1 - 8, negative means moving downward
        row_diff = end_row - current_row
        # Bishops cannot move horizontally, vertically or different on absolute value of row and columns
        if (current_col == end_col or current_row == end_row) or (abs(row_diff) != abs(col_diff)):
            return False
        # assign appropriate difference to take depending on differences of column and row
        col_step = 1 if col_diff > 0 else -1
        row_step = 1 if row_diff < 0 else -1
        # check for blocked path, it will return value of True when a piece is blocking the path
        path_check = self.is_path_blocked(current_col, current_row, end_col, end_row, col_step, row_step, board)
        if path_check:
            # return False, it is not a valid move
            return False

        else:
            return True

    def is_path_blocked(self, current_col, current_row, end_col, end_row, col_step, row_step, board):
        """ A method to check if the Bishop's path is blocked"""
        # place holder
        current_col_num = current_col
        new_current_col = current_col + col_step
        new_current_row = current_row + row_step
        # column and row converter
        col_counter = 0
        for i in range(97, 105):
            if i == current_col:
                current_col_num = col_counter
                break
            else:
                col_counter += 1
        row_counter = 0
        for i in reversed(range(9)):
            if i == current_row:
                current_row = row_counter
                break
            else:
                row_counter += 1

        x, y = current_col_num, current_row
        # checks for a blocked path for Bishop
        while new_current_col != end_col and new_current_row != end_row:
            piece_at_position = board[y][x]
            if piece_at_position.get(f"{chr(new_current_col)}{str(new_current_row)}") is not None:
                return True
            x += col_step
            y += row_step
            new_current_col += col_step
            new_current_row += row_step

        return False


class Knight(Piece):
    def __init__(self, color, pos):
        super().__init__("Knight", color, pos)

    def is_legal(self, end_piece,  current_col, current_row, end_col, end_row, board):
        """ Overriden method to validate the Knight's movement"""
        col_diff = end_col - current_col
        row_diff = end_row - current_row
        # Knight cannot move horizontally nor vertically
        if current_col != end_col and current_row != end_row:
            if (abs(col_diff) == 2 and abs(row_diff) == 1) or (abs(col_diff) == 1 and abs(row_diff) == 2):
                return True
            else:
                return False
        else:
            return False


class Rook(Piece):
    def __init__(self, color, pos):
        super().__init__("Rook", color, pos)

    def is_legal(self, end_piece,  current_col, current_row, end_col, end_row, board):
        """ Overriden method to validate the Rook's movement"""
        # negative means moving leftward
        col_diff = end_col - current_col
        # negative means moving downward
        row_diff = end_row - current_row

        # check if the Rook is moving only vertically or horizontally
        if col_diff == 0 or row_diff == 0:
            # check for blocked path
            path_check = self.is_path_blocked(current_col, end_col, current_row, end_row, board)
            if path_check:
                # if blocked path, return false
                return False

            else:
                return True
        else:
            return False

    def is_path_blocked(self, current_col, end_col, current_row, end_row, board):

        current_col_index = current_col
        current_row_index = current_row
        col_counter = 0
        # convert columns
        for i in range(97, 105):
            if i == current_col:
                current_col_index = col_counter
                break
            else:
                col_counter += 1
        # convert rows
        row_counter = 0
        for i in reversed(range(9)):
            if i == current_row:
                current_row_index = row_counter
                break
            else:
                row_counter += 1

        col_step = 0 if current_col == end_col else 1 if current_col < end_col else -1
        row_step = 0 if current_row == end_row else -1 if current_row < end_row else 1

        current_col += col_step
        current_row += row_step

        current_col_index += col_step
        current_row_index += row_step

        while current_col != end_col or current_row != end_row:
            piece_at_position = board[current_row_index][current_col_index].get(f"{chr(current_col)}{str(current_row)}")
            if piece_at_position is not None:
                return True
            current_col += col_step
            current_row -= row_step
            current_col_index += col_step
            current_row_index += row_step
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
        self._black_king_reached_row_7 = False

    def make_move(self, start_pos, end_pos):

        # check game status
        if self._game_state in ["WHITE_WON", "BLACK_WON", "TIE"]:
            print("Please check the game state")
            return False

        elif len(start_pos) == 2 and 'a' <= start_pos[0] <= 'h' and '1' <= start_pos[1] <= '8':
            # assign the board from Board object
            board = self.get_board()

            start_piece = None
            end_piece = None

            # get piece object
            for row in board:
                for column in row:
                    if start_pos in column:
                        start_piece = column[start_pos]
                        # check for a chess piece
                        if start_piece is None:
                            print("Please select a correct position")
                            return False
                    # get the second piece or a piece at the end position
                    if end_pos in column:
                        end_piece = column[end_pos]

            # check player's turn
            # returns true if correct player's turn
            check_player_turn = self.is_player_turn(start_piece)

            if check_player_turn is None:
                print("Please check player's turn")
                return False

            else:
                # check piece's legal movement
                validation_check = self.is_valid(start_piece, end_piece, start_pos, end_pos, board)

            # check for correct player's turn and legal movement for pieces
            if check_player_turn and validation_check:
                # update the board
                self.update_board(start_piece, start_pos, end_pos, board)
                # update game state/player's turn
                self.update_game_state(self._player_turn, end_pos, board)
                return True

            else:
                return False
        else:
            print("Invalid position")


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

    def is_player_turn(self, start_piece):
        """ A method to check correct player's turn """
        # check if the player entered the correct starting position
        check_turn = start_piece.get_color()
        if check_turn == self._player_turn:
            return True

    def is_valid(self, start_piece, end_piece, start_pos, end_pos, board):
        # separate the row and colum
        current_col, current_row = ord(start_pos[0]), int(start_pos[1])
        end_col, end_row = ord(end_pos[0]), int(end_pos[1])
        # check starting position and end position
        if start_pos == end_pos or start_piece is None:
            return False
        # check the existence of both start_piece and end_piece
        elif start_piece is not None and end_piece is not None:
            # check if they have the same color
            if start_piece.get_color() != end_piece.get_color() and end_piece.get_type() != 'King':
                # check for legal movement and blocked path
                check_valid = start_piece.is_legal(end_piece, current_col, current_row, end_col, end_row, board)
                if check_valid:
                    return True

                else:
                    return False
            else:
                return False
        # check condition for moving one piece to an empty space
        elif start_piece is not None and end_piece is None:
            # check for legal movement and blocked path
            check_valid = start_piece.is_legal(end_piece,  current_col, current_row, end_col, end_row, board)
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
            else:
                self._black_king_reached_row_8 = True

        # check if the white King is on row8
        if self._white_king_reached_row_8 and not self._black_king_reached_row_8:
            if self._player_turn == 'white':
                # traverse through row7
                for i in range(8):
                    pos = f"{chr(ord('a') + i)}7"
                    piece = board[1][i][pos]
                    # find and check for black King's existence on row7
                    if piece is not None and piece.get_type() == "King" and piece.get_color() == "black":
                        self._black_king_reached_row_7 = True
                        break
                # if black King exists, set the next turn to black and continue the play
                if self._black_king_reached_row_7:
                    self._next_turn = 'black'

                else:
                    # if not, white player wins the game
                    self._game_state = 'WHITE_WON'
                    print("White King reached row 0")
        # if the black King did not move to row 8 for some reason, then white wins
        if self._black_king_reached_row_7:
            if self._player_turn == 'black':
                if end_index != 8:
                    self._game_state = 'WHITE_WON'
                    return 0

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
        else:
            self._player_turn = 'white'

    def get_game_state(self):
        """ A get method for game state"""
        return self._game_state

    def get_player_turn(self):
        """ A get method for player's turn"""
        return self._player_turn

    def get_white_black(self):
        return self._white_king_reached_row_8
