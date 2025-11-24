"""
Imports
"""
try:
    from src.base_classes.piece import Piece
    from src.constants.constPieces import *
    from src.constants.constFlags import *
    from src.constants.constColours import *
    from src.array_based_classes.array_move import ArrayMove
except:
    from base_classes.piece import Piece
    from constants.constPieces import *
    from constants.constFlags import *
    from constants.constColours import *
    from array_based_classes.array_move import ArrayMove


"""
Classes
"""
class Pawn(Piece):
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
            Generates all possible moves for the pawn.
            Includes illegal moves, this is handled in
            a different function
        
        Parmams:
            board (Board)
        """
        
        # Direction that the pawn can move depends on the colour of the piece
        direction = (-1, 0) if self.colour == WHITE else (1, 0)
        # Also need to check if pawn can move two spaces
        startRow = 6 if self.colour == WHITE else 1
        loopTimes = 2 if self.currentPosition[0] == startRow else 1
        
        promotionRow = 0 if self.colour == WHITE else 7
        
        numRows = len(board.get_board())
        numCols = len(board.get_board()[0])
        moves = []
        
        row, col = self.currentPosition
        for _ in range(loopTimes):
            
            row += direction[0]
            col += direction[1]
            
            if row < 0 or row >= numRows or col < 0 or col >= numCols:
                break
                
            # No piece occupying square
            if board.get_piece(row, col) is None:
                if row == promotionRow:
                    moves.append(ArrayMove(board, self.currentPosition, (row, col), flag=PROMOTION))
                else:
                    moves.append(ArrayMove(board, self.currentPosition, (row, col)))
                
            # same colour
            else:
                break
        
        return (moves + self.get_attacks(board))
            
    def get_attacks(self, board):
        """
        Method:
            Pawns are the only piece that doesn't capture where
            it can move to. Handle attacks away from get_moves()
            function. Returns a list of positions.
        
        Params:
            board (Board)
        """
        
        directions = [(-1, 1), (-1,-1)] if self.colour == WHITE else [(1,1), (1,-1)]
        numRows = len(board.get_board())
        numCols = len(board.get_board()[0])
        attacks = []
        promotionRow = 0 if self.colour == WHITE else 7
        enpassantRow = 3 if self.colour == WHITE else 4
        
        for direction in directions:
            
            vectorRow, vectorCol = direction
            row, col = self.currentPosition
            
            row += vectorRow
            col += vectorCol
            
            if row < 0 or row >= numRows or col < 0 or col >= numCols: 
                continue
            
            if board.get_piece(row, col) != None and board.get_piece(row, col).get_colour() != self.colour:
                if row == promotionRow:
                    attacks.append(ArrayMove(board, self.currentPosition, (row, col), flag=PROMOTION))
                else:
                    attacks.append(ArrayMove(board, self.currentPosition, (row, col)))
                    
        # Handle possible enpassant
        if self.currentPosition[0] == enpassantRow:
            
            direction = -1 if self.colour == WHITE else 1
            # get piece to the right and left, try block to handle out of bounds errors
            try:
                leftPiece = board.get_piece(enpassantRow, self.currentPosition[1]-1)
            except:
                leftPiece = None
                
            try:
                rightPiece = board.get_piece(enpassantRow, self.currentPosition[1]+1)
            except:
                rightPiece = None
            
            if leftPiece is not None and leftPiece == board.get_last_move().get_home_piece() and leftPiece.get_type() == PAWN:
                if self.currentPosition[1]-1 < 0:
                    pass
                else:
                    attacks.append(ArrayMove(board, self.currentPosition, ((self.currentPosition[0]+direction), (self.currentPosition[1]-1)), flag=ENPASSANT))
            
            if rightPiece is not None and rightPiece == board.get_last_move().get_home_piece() and rightPiece.get_type() == PAWN:
                if self.currentPosition[1]-1 < 0:
                    pass
                else:
                    attacks.append(ArrayMove(board, self.currentPosition, ((self.currentPosition[0]+direction), (self.currentPosition[1]+1)), flag=ENPASSANT))

        return attacks
            
            
        
        
        
        
                
        
        
            
        
        