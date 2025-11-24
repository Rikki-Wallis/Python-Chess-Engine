"""
Imports
"""
try:
    from src.constants.constPieces import *
except:
    from constants.constPieces import *
"""
Classes
"""
class Piece:
    
    # id counter for pieces makes sure each piece has a unique ID
    _id = 0
    
    def __init__(self, type, colour):
        """
        Method:
            init method for piece class
            
        Params:
            type (ENUM)
            colour (ENUM)
        """
        self.id = Piece._id
        self.type = type
        self.colour = colour
        self.currentPosition = None
        self.timesMoved = 0
        self.active = True
        
        Piece._id += 1
    
    def get_id(self):
        return self.id
    
    def get_type(self):
        return self.type
    
    def get_colour(self):
        return self.colour
    
    def get_position(self):
        return self.currentPosition

    def get_times_moved(self):
        return self.timesMoved
    
    def increment_times_moved(self):
        self.timesMoved += 1
    
    def decrement_times_moved(self):
        self.timesMoved -= 1
    
    def get_active(self):
        return self.active
    
    def set_active(self, active):
        self.active = active
    
    def update_position(self, row=None, col=None):
        """
        Method:
            Sets the piece's position ot either None
            (removing piece from board) or to the
            given row, col params
            
        Params:
            row (int?None)
            col (int?None)
        """
        # Update position to none
        if row is None or col is None:
            self.currentPosition = None
        # Update position to params
        else:
            self.currentPosition = (row, col)
    
    def __str__(self):
        pieces = {
            ROOK : 'R',
            PAWN : 'P',
            BISHOP : 'B',
            KNIGHT : 'N',
            KING : 'K',
            QUEEN : 'Q'
        }
        
        return pieces[self.type]