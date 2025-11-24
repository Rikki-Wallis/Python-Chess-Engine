"""
Imports
"""
try:
    from src.constants.constFlags import *
except:
    from constants.constFlags import *
    

"""
Classes
"""
class Move:
    
    """ ----------------------------------- Constructer ----------------------------------- """
    
    
    def __init__(self, board, moveFrom, moveTo, flag=None):
        # Class vars
        self.board = board
        self.moveFrom = moveFrom
        self.moveTo = moveTo
        self.flag = flag
        
        # Get home and target pieces
        self.additional_settup()


    """ ----------------------------------- Abstract Methods ----------------------------------- """


    def additional_settup(self):
        """
        Method:
            Any additional settup for the move (to be overridden by subclasses)
        """
        pass
    
    
    def handle_remove_pieces(self, action):
        """
        Method:
            handles removing a piece from the board (to be overridden by subclasses)
        """
        pass
    
    
    def handle_short_castle(self, action):
        """
        Method:
            handles short castling (to be overridden by subclasses)
        """
        pass
    
    
    def handle_long_castle(self, action):
        """
        Method:
            handles long castling (to be overridden by subclasses)
        """
        pass
    
    
    def handle_enpassant(self, action):
        """
        Method:
            handles enpassant (to be overridden by subclasses)
        """
        pass
    
    
    def handle_promotion(self, action, promotionChoice=None):
        """
        Method:
            handles promotion (to be overridden by subclasses)
        """
        pass
    
    
    def handle_placing_piece(self, action):
        """
        Method:
            handles placing a piece on the board (to be overridden by subclasses)
        """
        pass
    
    
    def make_update(self, action):
        """
        Method:
            handles updating the board state after a move (to be overridden by subclasses)
        """
        pass
    
    
    """ ----------------------------------- Implemented Methods ----------------------------------- """
    
    
    def make_move(self, promotionChoice=None):
        """
        Method:
            makes the move on the board (to be overridden by subclasses)
        """
        # Remove piece at target and home square
        self.handle_remove_pieces(MAKE)
        
        # Handle flags appropriately
        if self.flag == SHORT_CASTLE:
            self.handle_short_castle(MAKE)
        
        elif self.flag == LONG_CASTLE:
            self.handle_long_castle(MAKE)
            
        elif self.flag == ENPASSANT:
            self.handle_enpassant(MAKE)
        
        elif self.flag == PROMOTION:
            self.handle_promotion(MAKE, promotionChoice=promotionChoice)
        
        # Move piece
        self.handle_placing_piece(MAKE)
        
        # Update board state
        self.make_update(MAKE)
        
    
    def undo_move(self):
        """
        Method:
            undoes the move on the board (to be overridden by subclasses)
        """
        # Remove piece at target and home square
        self.handle_remove_pieces(UNDO)
        
        # Handle flags appropriately
        if self.flag == SHORT_CASTLE:
            self.handle_short_castle(UNDO)
        
        elif self.flag == LONG_CASTLE:
            self.handle_long_castle(UNDO)
            
        elif self.flag == ENPASSANT:
            self.handle_enpassant(UNDO)
        
        elif self.flag == PROMOTION:
            self.handle_promotion(UNDO)
        
        # Move piece
        self.handle_placing_piece(UNDO)
        
        # Update board state
        self.make_update(UNDO)
    
    
    """----------------------------------- Getters and Setters ----------------------------------- """
    
    
    def get_move_from(self):
        return self.moveFrom
    
    
    def get_move_to(self):
        return self.moveTo
    
    
    def get_flag(self):
        return self.flag
    
    
    def get_home_piece(self):
        return self.homePiece
    
    
    def get_target_piece(self):
        return self.targetPiece
    
    
    def get_is_check(self):
        return self.isCheck
    
    
    def get_is_capture(self):
        return self.isCapture