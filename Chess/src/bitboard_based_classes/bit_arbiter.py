"""
Imports
"""
try:
    from src.base_classes.arbiter import Arbiter
    from src.constants.constColours import *
    from src.constants.constPieces import *
    from src.constants.constFlags import *
    from src.constants.constCastlingBoards import *
except:
    from base_classes.arbiter import Arbiter
    from constants.constColours import *
    from constants.constPieces import *
    from constants.constFlags import *
    from constants.constCastlingBoards import *

"""
Classes
"""
class BitArbiter(Arbiter):
    def __init__(self, moveGenerator):
        self.moveGenerator = moveGenerator
    
    
    """ ---------------------------------------------------------- Overridden Methods ---------------------------------------------------------- """
    
    
    def is_in_check(self, board, colour):
        """
        Method:
            Returns a bool, if the king given is
            in check
        
        Params:
            board (BitBoard)
            colour (ENUM) - The colour of the king we are looking for is in check
        """
        # Intiate vars
        oColour = BLACK if colour == WHITE else WHITE
        
        return self.moveGenerator.get_all_attacks(board, oColour) & board.get_board()[f'{colour} {KING}']
    
    
    def is_in_checkmate(self, board):
        """
        Method:
            Returns a bool, if the current position is checkmate
        
        Params:
            board (BitBoard)
        """
        cColour = board.get_colour()
        # Fetch moves in current position
        moves = self.moveGenerator.get_all_moves(board)
        filtered = self.filter_moves(board, moves, cColour)
        
        if not self.is_in_check(board, cColour) and len(filtered) == 0:
            return True
        
        return False
    
    
    def is_in_stalemate(self, board):
        """
        Method:
            Returns a bool, if the current position is stalemate
        
        Params:
            board (BitBoard)    
        """
        cColour = board.get_colour()
        # Fetch moves in current position
        moves = self.moveGenerator.get_all_moves(board)
        filtered = self.filter_moves(board, moves, cColour)
        
        if self.is_in_check(board, cColour) and len(filtered) == 0:
            return True
        
        return False
    
    
    def generate_material_count(self, board):
        """
        Method:
            Returns the material count for both sides in a dictionary
        
        Params:
            board (BitBoard)
        """
        count = {}
        
        for key, bitboard in board.get_board().items():
            
            # Ignore occupancy masks
            if key == BLACK or key == WHITE:
                continue
            
            # Calculate number of pieces by counting the number of 1s in the bitboard
            count[key] = bin(bitboard).count('1')
        
        return count
    
    
    def filter_moves(self, board, moves, colour):
        """
        Method:
            Filters out moves that would leave the king in check
        
        Params:
            board (BitBoard)
            moves (list[BitMove])
            colour (ENUM)
        """
        filtered = []
        for move in moves:
            
            if move.moveTo == 0 or move.isCheck or move.moveTo.bit_length() > 64:
                continue
            
            if move.get_flag() == SHORT_CASTLE or move.get_flag() == LONG_CASTLE:
                
                flag = move.get_flag()
                oColour = WHITE if colour == BLACK else BLACK
                attacks = self.moveGenerator.get_all_attacks(board, oColour)
                
                if self.is_in_check(board, colour):
                    continue 
                
                if flag == SHORT_CASTLE and colour == WHITE:
                    emptyPos = WHITE_SHORT_EMPTY_CASTLE_POS
                
                elif flag == SHORT_CASTLE and colour == BLACK:
                    emptyPos = BLACK_SHORT_EMPTY_CASTLE_POS
                
                elif flag == LONG_CASTLE and colour == WHITE:
                    emptyPos = WHITE_LONG_MOVE_THROUGH_CHECK
                
                elif flag == LONG_CASTLE and colour == BLACK:
                    emptyPos = BLACK_LONG_MOVE_THROUGH_CHECK
                
                if attacks & emptyPos:
                    continue
            
            if move.get_flag() == PROMOTION:
                move.make_move(promotionChoice=QUEEN)
            else:
                move.make_move()

            if not self.is_in_check(board, colour):
                filtered.append(move)
            
            move.undo_move()
        
        return filtered