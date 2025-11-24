"""
Imports
"""
try:
    from src.base_classes.piece import Piece
    from src.constants.constPieces import *
    from src.array_based_classes.array_move import ArrayMove
except:
    from base_classes.piece import Piece
    from constants.constPieces import *
    from array_based_classes.array_move import ArrayMove
    
"""
Classes
"""
class Knight(Piece):
    def __init__(self, type, colour):
        """
        Method:
            Initiate class variables for
            piece.
        """
        super().__init__(type, colour)
        
    def get_moves(self, board):
        """
        Method:
            Generates all possible moves for the knight.
            Includes illegal moves, this is handled in
            a different function
        
        Parmams:
            board (Board)
        """
        # Define vars
        directions = [(-2, -1), (-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2)]
        numRows = len(board.get_board())
        numCols = len(board.get_board()[0])
        moves = []
        
        # Iterate over each direction and scan for moves
        for vectorRow, vectorCol in directions:
            
            row, col = self.currentPosition
            
            # Scan for moves while not out of bounds
            row += vectorRow
            col += vectorCol
            
            if row < 0 or row >= numRows or col < 0 or col >= numCols:
                continue
            
            # No piece occupying square
            if board.get_piece(row, col) is None:
                moves.append(ArrayMove(board, self.currentPosition, (row, col)))
                
            # same colour
            elif board.get_piece(row, col).get_colour() == self.colour:
                pass
                
            # Must be a capture
            else:
                if board.get_piece(row, col).get_type() == KING:
                    moves.append(ArrayMove(board, self.currentPosition, (row, col)))
                else:
                    moves.append(ArrayMove(board, self.currentPosition, (row, col)))
                
                
        return moves