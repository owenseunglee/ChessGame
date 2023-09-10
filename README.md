# ChessGame

 need to keep track of which player's turn it is. As in standard chess, white moves first. The first player to move their king onto row 8 is the winner, unless black finishes the next move after white does, in which case it's a tie. Pieces move and capture the same as in standard chess. As in standard chess, a player is not allowed to expose their own king to check (including moving a piece that was blocking a check such that it no longer does). Unlike standard chess, a player is not allowed to put the opponent's king in check (including moving a piece that was blocking a check such that it no longer does).

Locations on the board will be specified using "algebraic notation", with columns labeled a-h and rows labeled 1-8, with row 1 being the start side and row 8 the finish side, as shown in the diagram above.

Here's a very simple example of how the class could be used:

game = ChessVar()
move_result = game.make_move('c2', 'e3')
game.make_move('g1', 'f1')
state = game.get_game_state()
