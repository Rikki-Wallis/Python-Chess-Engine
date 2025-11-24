"""
Imports
"""
try:
    from src.array_based_classes.pieces.rook import Rook
    from src.array_based_classes.pieces.bishop import Bishop
    from src.array_based_classes.pieces.knight import Knight
    from src.array_based_classes.pieces.king import King
    from src.array_based_classes.pieces.queen import Queen
    from src.array_based_classes.pieces.pawn import Pawn
    from src.base_classes.board import Board
    from src.constants.constPieces import *
    from src.constants.constColours import *
    
except:
    from array_based_classes.pieces.rook import Rook
    from array_based_classes.pieces.bishop import Bishop
    from array_based_classes.pieces.knight import Knight
    from array_based_classes.pieces.king import King
    from array_based_classes.pieces.queen import Queen
    from array_based_classes.pieces.pawn import Pawn
    from base_classes.board import Board
    from constants.constPieces import *
    from constants.constColours import *

"""
Classes
"""
RANK_LENGTH = 7
FILE_HEIGHT = 7

class ArrayBoard(Board):

    """------------------------------------------------ Constructer ----------------------------------------------------"""
    
    
    def __init__(self):
        super().__init__()
        
    
    """ -------------------------------------------- Overridden Methods ------------------------------------------------------"""

    
    def additionalSettup(self):
        """
        Method:
            Any additional settup for the board
        """
        self.board = [[None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      ]

        self.bKing = None
        self.wKing = None

        self.setUpDefaultPosition()
        self.set_pieces_list()
        
        
    def set_pieces_list(self):
        """
        Method:
            Sets the pieces list
        """
        self.pieces = []
        for row in self.board:
            for item in row:
                if item is not None:
                    self.pieces.append(item)
    
    
    def get_piece(self, row, col):
        """
        Method:
            Returns the piece at a given position
        """
        return self.board[row][col]

    
    def hash_position(self):
        """
        Method:
            Hashes the current position
        """
        # Create a mutable list for the board representation
        boardRepresentation = list("." * 64)
        
        # Iterate through each piece on the board
        for piece in self.pieces:
            # Only add active pieces
            if piece.get_active():
                # Get index
                pos = piece.get_position()
                index = pos[0] * 8 + pos[1]
                
                if piece.get_colour() == WHITE:
                    boardRepresentation[index] = str(piece).upper()
                else:
                    boardRepresentation[index] = str(piece).lower()
        
        # Add the current colour to move at the end
        boardRepresentation.append(self.currentColour)
        
        # Convert the list back to a string
        return "".join(boardRepresentation)
    
    
    """ ------------------------------------------------ Helper Methods ----------------------------------------------------------"""
    
    
    def add_piece(self, piece, row, col):
        """
        Method:
            Add a piece to the board
        
        Params:
            piece (Piece)
            row (int)
            col (int)
        """
        
        # Check rank and file boundary
        if row > RANK_LENGTH or row < 0:
            raise ValueError
        elif col > FILE_HEIGHT or col < 0:
            raise ValueError
        elif piece is None:
            return
        
        # Add piece
        self.board[row][col] = piece
        piece.update_position(row, col)
    
    
    def remove_piece(self, row, col):
        """
        Method:
            Remove a piece from the board
            and returns it.
        
        Params:
            rank (int)
            file (int)
        """
        
        # Check rank and file boundary
        if row > RANK_LENGTH or col < 0:
            raise ValueError
        elif row > FILE_HEIGHT or col < 0:
            raise ValueError
        
        # Remove the piece
        toReturn = self.board[row][col]
        self.board[row][col] = None
        
        return toReturn
    
    
    def setUpDefaultPosition(self):
        """
        Method:
            Sets up the default board for chess
        """
        colours = [BLACK, WHITE]
        rows = [0, 7]
        pawnRows = [1, 6]
        for idx, colour in enumerate(colours):
            self.add_piece(Rook(ROOK, colour), rows[idx], 0)
            self.add_piece(Rook(ROOK, colour), rows[idx], 7)
            self.add_piece(Knight(KNIGHT, colour), rows[idx], 1)
            self.add_piece(Knight(KNIGHT, colour), rows[idx], 6)
            self.add_piece(Bishop(BISHOP, colour), rows[idx], 2)
            self.add_piece(Bishop(BISHOP, colour), rows[idx], 5)
            self.add_piece(Queen(QUEEN, colour), rows[idx], 3)
            self.add_piece(King(KING, colour), rows[idx], 4)
            
            lenBoard = 8
            for i in range(lenBoard):
                self.add_piece(Pawn(PAWN, colour), pawnRows[idx], i)
        
        self.bKing = self.get_piece(0, 4)
        self.wKing = self.get_piece(7, 4)
    
    
    def setUpOnlyKings(self):
        self.add_piece(King(KING, WHITE), 7, 4)
        self.add_piece(King(KING, BLACK), 0, 4)
        self.add_piece(Pawn(PAWN, WHITE), 7, 7)