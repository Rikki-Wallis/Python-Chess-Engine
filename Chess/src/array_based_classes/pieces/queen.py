"""
Imports
"""
try:
    from src.base_classes.piece import Piece
    from src.array_based_classes.pieces.rook import Rook
    from src.array_based_classes.pieces.bishop  import Bishop
    from src.constants.constPieces import *
except:
    from base_classes.piece import Piece
    from array_based_classes.pieces.rook import Rook
    from array_based_classes.pieces.bishop  import Bishop
    from constants.constPieces import *
    
"""
Classes
"""
class Queen(Piece):
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
            Generates all possible moves for the queen.
            Includes illegal moves, this is handled in
            a different function
        
        Parmams:
            board (Board)
        """
        
        # The movement of the queen can be thought of as a combination
        # of the rook and the bishops movement, therefor we just
        # need to fetch their possible moves in a position and return that
        
        rook = Rook(ROOK, self.colour)
        bishop = Bishop(BISHOP, self.colour)
        
        # Mock their current position on the board
        rook.update_position(self.currentPosition[0], self.currentPosition[1])
        bishop.update_position(self.currentPosition[0], self.currentPosition[1])
        
        # Fetch moves
        rookMoves = rook.get_moves(board)
        bishopMoves = bishop.get_moves(board)
        
        return rookMoves + bishopMoves
        
        
        