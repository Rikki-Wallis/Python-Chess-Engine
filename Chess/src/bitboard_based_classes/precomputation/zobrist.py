"""
Imports
"""
import random

try:
    from src.constants.constPieces import *
    from src.constants.constColours import *
except:
    from constants.constPieces import *
    from constants.constColours import *

"""
Classes
"""
class Zobrist:
    
    def __init__(self):
        # Generate random numbers for each aspect of the game state
        
        # Pieces list
        self.pieceTypes = [PAWN, ROOK, BISHOP, KNIGHT, KING, QUEEN]
        
        # piece type, colour,  square index
        self.pieces = {
            PAWN : {},
            ROOK : {},
            BISHOP : {},
            KNIGHT : {},
            KING : {},
            QUEEN : {},  
        }
        self.piecesLen = 64
        
        # Each player has 4 possible castling right states: none, queenside, kingside, both
        self.castlingRights = []
        self.castlingLen = 16
        
        # Enpassant file (0 = no ep)
        self.enpassantFile = []
        self.sideToMove = None
        self.enpassantLen = 9
        
        self.zobrist()
    
    
    def zobrist(self):
        """
        Method:
            Initiates the random integers that populate the init lists
        """
        random.seed(33856958)
        
        # Add a random number for each square on the board, for each piecetype
        for type in self.pieceTypes:        
            for squareIndex in range(self.piecesLen):
                self.pieces[type][squareIndex] = random.getrandbits(self.piecesLen)

        # Add random number for each type of castling state
        for i in range(self.castlingLen):
            self.castlingRights.append(random.getrandbits(self.piecesLen))
            
        # Add random number for each type of enpassant state
        for i in range(self.enpassantLen):
            self.enpassantFile.append(i if i == 0 else random.getrandbits(self.piecesLen))
        
        self.sideToMove = random.getrandbits(self.piecesLen)

    
    def calculate_zobrist_key(self, board):
        """
        Method:
            Calculate zobrist key from current board position.
            NOTE: this function is slow and should only be used
            when the board is initially setup. During search,
            the key should be updated incrementally instead.
        
        Params:
            board (BitBoard)
        """
        
        # Initate vars
        zobristKey = 0
        
        # Iterate over each square
        for squareIndex in range(self.piecesLen):
            
            index = 0
            index = (1 << squareIndex)
            
            # If the occupancy mask is empty, there can't be a piece there
            if board.get_board()[WHITE] & index and board.get_board()[BLACK] & index:
                continue
            
            # Otherwise search for which piece type it is
            for pieceAttributes, bitboard in board.get_board().items():
                
                # Ignore occupancy masks
                if pieceAttributes == BLACK or pieceAttributes == WHITE:
                    continue
                
                if bitboard & index:
                    pieceAttributes = pieceAttributes.split(' ')
                    type = pieceAttributes[1]
                    
                    zobristKey ^= self.pieces[type][squareIndex]
        
        if board.get_colour() == BLACK:
            zobristKey ^= self.sideToMove
        
        # TODO: For now I can assume that there is no enpassant in this position
        # as we will only consider the initial position. However, in future I will
        # add a proper implementation of this
        zobristKey ^= self.enpassantFile[0]
        
        # TODO: same with castling rights
        zobristKey ^= self.castlingRights[0]
        
        return zobristKey