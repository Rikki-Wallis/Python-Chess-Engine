"""
Imports
"""
try:
    from src.base_classes.piece import Piece
    from src.array_based_classes.array_move import ArrayMove
    from src.constants.constPieces import *
    from src.constants.constFlags import *
except:
    from base_classes.piece import Piece
    from array_based_classes.array_move import ArrayMove
    from constants.constPieces import *
    from constants.constFlags import *
    
"""
Classes
"""
class King(Piece):
    def __init__(self, type, colour):
        """
        Method:
            Initiate class variables for
            piece.
        """
        super().__init__(type, colour)
        self.i = 0
        
    def get_moves(self, board):
        """
        Method:
            Generates all possible moves for the king.
            Includes illegal moves, this is handled in
            a different function
        
        Parmams:
            board (Board)
        """
        # Define vars
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
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
                moves.append(ArrayMove(board, self.currentPosition, (row, col)))
        
        # Get castling moves
        if self.can_short_castle(board):
            moves.append(ArrayMove(board, self.currentPosition, (self.currentPosition[0], 6), flag=SHORT_CASTLE)) 
        if self.can_long_castle(board):   
            moves.append(ArrayMove(board, self.currentPosition, (self.currentPosition[0], 2), flag=LONG_CASTLE))
            
        return moves
    
    def can_short_castle(self, board):
        """
        Method:
            Returns a bool of if the king can perform a short castle
        
        Params:
            board (Board)
        """
        # If the king has moved cant castle
        if self.timesMoved != 0:
            return False
        
        # Fetch rook
        rook = board.get_piece(self.currentPosition[0], 7)
        
        # Check if the rook is valid to castle
        if rook is None:
            return False
        # If it isnt a rook
        elif rook.get_type() != ROOK:
            return False
        # If it isnt of the same colour
        elif rook.get_colour() != self.colour:
            return False
        # If its already moved
        elif rook.get_times_moved() != 0:
            return False
        
        # Check if there are empty spaces inbetween rook and king
        index5 = board.get_piece(self.currentPosition[0], 5)
        index6 = board.get_piece(self.currentPosition[0], 6)
        
        if index5 is not None or index6 is not None:
            self.i += 1
            return False
        
        return True
    
    def can_long_castle(self, board):
        """
        Method:
            Returns a bool of if the king can perform a long castle
        
        Params:
            board (Board)
        """
        # If the king has moved cant castle
        if self.timesMoved != 0:
            return False
        
        # Fetch rook
        rook = board.get_piece(self.currentPosition[0], 0)
        
        # Check if the rook is valid to castle
        if rook is None:
            return False
        # If it isnt a rook
        elif rook.get_type() != ROOK:
            return False
        # If it isnt of the same colour
        elif rook.get_colour() != self.colour:
            return False
        # If its already moved
        elif rook.get_times_moved() != 0:
            return False
        
        # Check if there are empty spaces inbetween rook and king
        index1 = board.get_piece(self.currentPosition[0], 1)
        index2 = board.get_piece(self.currentPosition[0], 2)
        index3 = board.get_piece(self.currentPosition[0], 3)
        
        if index1 is not None or index2 is not None or index3 is not None:
            return False
        
        return True