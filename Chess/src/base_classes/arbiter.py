"""
Imports
"""
try:
    from src.constants.constColours import *
    from src.constants.constPieces import *
except:
    from constants.constColours import *
    from constants.constPieces import *

"""
Classes
"""
class Arbiter:
    
    """ ---------------------------------------------------------- Constructor ----------------------------------------------------------"""
    
    
    def __init__(self):
        pass
    
    
    """ ---------------------------------------------------------- Abstract Methods ----------------------------------------------------------"""
    
    
    def filter_moves(self, board, moves, colour):
        pass
    
    def get_all_attacks(self, board, colour):
        pass
    
    def get_all_moves(self, board):
        pass
    
    def get_king_position(self, king):
        pass
    
    def look_for_check(self, board, king, attacks):
        pass
    
    def generate_material_count(self, board):
        pass
    
    
    """ ---------------------------------------------------------- Rules Methods ----------------------------------------------------------"""
    
    
    def is_in_check(self, board, colour):
        """
        Method:
            Returns a bool, if the king given is
            in check
        
        Params:
            board (Board)
            colour (ENUM) - The colour of the king we are looking for is in check
        """
        # Fetch colours
        cColour = colour
        oColour = BLACK if cColour == WHITE else WHITE
        
        # Fetch current colour's king and all attacks for oppoenent pieces
        king = board.get_king(cColour)
        attacks = self.get_all_attacks(board, oColour)
        
        if self.look_for_check(board, king, attacks):
            return True
        
        return False
    
    
    def is_in_checkmate(self, board):
        """
        Method:
            Returns a bool, if the king given is
            in checkmate
        
        Params:
            board (Board)
        """
        # If not in check, cannot be in checkmate
        if not self.is_in_check(board, board.get_colour()):
            return False
        
        # Fetch all possible moves
        cColour = board.get_colour()
        moves = self.get_all_moves(board)
        moves = self.filter_moves(board, moves, board.get_colour())
        
        # If there are no legal moves must be checkmate
        if len(moves) == 0:
            return True
        
        # Otherwise it is not checkmate
        return False
        
        
    def is_in_stalemate(self, board):
        """
        Method:
            Returns a bool, if the king given is
            in stalemate
        
        Params:
            board (Board)
        """
        # If in check can't be stalemate
        if self.is_in_check(board, board.get_colour()):
            return False
        
        # Fetch all possible moves
        moves = self.get_all_moves(board)
        moves = self.filter_moves(board, moves, board.get_colour())
        
        # If there are no legal moves must be stalemate
        if len(moves) == 0:
            return True
        
        # Otherwise it is not stalemate
        return False
        

    def is_in_insufficient_material(self, board):
        """
        Method:
            Returns a bool, if there is insufficient
            material to continue the game
        """
        materialCount = self.generate_material_count(board)

        # Can't be insufficient material if there are these pieces
        if materialCount[f'{WHITE} {PAWN}'] > 0 or materialCount[f'{BLACK} {PAWN}'] > 0:
            return False
        
        elif materialCount[f'{WHITE} {ROOK}'] > 0 or materialCount[f'{BLACK} {ROOK}'] > 0:
            return False
        
        elif materialCount[f'{WHITE} {QUEEN}'] > 0 or materialCount[f'{BLACK} {QUEEN}'] > 0:
            return False
        
        wCount = materialCount[f'{WHITE} {BISHOP}'] + materialCount[f'{WHITE} {KNIGHT}']
        bCount = materialCount[f'{BLACK} {BISHOP}'] + materialCount[f'{BLACK} {KNIGHT}']
        
        if wCount > 1 and bCount > 1:
            return False
        
        return True
        
    
    def is_in_repetition(self, board):
        """
        Method:
            Returns a bool, if the current position
            has been repeated 3 times
        
        Params:
            board (Board)
        """
        # Obtain hash key of current position    
        hashKey = board.hash_position()

        # Check if the position has been reach 3 times before
        if hashKey in board.get_position_hash() and board.get_position_count(hashKey) >= 3:
            return True
        
        return False
            


    def is_in_fifty_move_rule(self, board):
        """
        Method:
            Returns a bool, if the fifty move rule
            has been reached
        
        Params:
            board (Board)
        """
        if board.get_half_move_clock() >= 100:
            return True
        
        return False
