"""
Imports
"""
try:
    from src.base_classes.piece import Piece
    from src.array_based_classes.array_move import ArrayMove
    from src.constants.constPieces import *
except:
    from base_classes.piece import Piece
    from array_based_classes.array_move import ArrayMove
    from constants.constPieces import *

"""
Classes
"""
class Rook(Piece):
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
            Generates all possible moves for the rook.
            Includes illegal moves, this is handled in
            a different function
        
        Parmams:
            board (List[List[Piece?None]])
        """
        
        # Define vars
        directions = [(-1,0), (0,1), (1,0), (0,-1)]
        numRows = len(board.get_board())
        numCols = len(board.get_board()[0])
        moves = []
        
        # Iterate over each direction and scan for moves
        for vectorRow, vectorCol in directions:
            
            row, col = self.currentPosition
            
            # Scan for moves while not out of bounds
            while True:
                row += vectorRow
                col += vectorCol
                
                if row < 0 or row >= numRows or col < 0 or col >= numCols:
                    break
                
                # No piece occupying square
                if board.get_piece(row, col) is None:
                    moves.append(ArrayMove(board, self.currentPosition, (row, col)))
                    
                # same colour
                elif board.get_piece(row, col).get_colour() == self.colour:
                    break
                    
                # Must be a capture
                else:
                    moves.append(ArrayMove(board, self.currentPosition, (row, col)))
                    break
                
        return moves
                
                
                
                
                
                
                
                
                
    