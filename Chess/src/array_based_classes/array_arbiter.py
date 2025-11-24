"""
Imports
"""
try:
    from src.constants.constPieces import *
    from src.constants.constFlags import *
    from src.constants.constColours import *
    from src.base_classes.arbiter import Arbiter
except:
    from constants.constPieces import *
    from constants.constFlags import *
    from constants.constColours import *
    from base_classes.arbiter import Arbiter

"""
Classes
"""
class ArrayArbiter(Arbiter):
    def __init__(self):
        super().__init__()
    
    """------------------------------------------------ Overridden Methods ----------------------------------------------------------"""    
    
    
    def filter_moves(self, board, moves, colour):
        """
        Method:
            Filters moves to not include those that result in the 
            king being in check
        
        Params:
            board (Board)
            moves (list[Move])
            colour (ENUM)
        """
        # Initiate variables
        filtered = []
        shortCastle = False
        longCastle = False
        cColour = colour
        
        # Iterate over each move, make move, check if in check, append if not
        for move in moves:
            
            # Some moves allow the king to be taken so remove those
            if move.get_target_piece() != None and move.get_target_piece().get_type() == KING: 
                continue
            
            # Handle promotion case
            elif move.get_flag() == PROMOTION:
                move.make_move(promotionChoice='P')
            
            # Handle castle case
            elif move.get_flag() == SHORT_CASTLE:
                shortCastle = True
                shortFrom = move.get_move_from()
                move.make_move()
            
            elif move.get_flag() == LONG_CASTLE:
                longCastle = True
                longFrom = move.get_move_from()
                move.make_move()
            
            else:
                move.make_move()
            
            if not self.is_in_check(board, cColour):
                filtered.append(move)
            
            move.undo_move()
        
        # Make sure that castling does not lead to a check
        if shortCastle:
            moveToList = [move.moveTo for move in filtered]
            row, col = shortFrom
            col += 1
            if (row, col) not in moveToList:
                for i, move in enumerate(filtered):
                    if move.get_flag() == SHORT_CASTLE or move.get_is_check():
                        del filtered[i]          
                
        if longCastle:
            moveToList = [move.moveTo for move in filtered]
            row, col = longFrom
            col -= 1
            if (row, col) not in moveToList:
                for i, move in enumerate(filtered):
                    if move.get_flag() == LONG_CASTLE or move.get_is_check():
                        del filtered[i]

        return filtered
    
    
    def get_all_attacks(self, board, colour):
        """
        Method:
            Returns a list of squares attacked by the
            given colour
        
        Params:
            board (Board)
        """
        # Initiate variables
        attacks = []
        
        # iterate over board
        for row, rank in enumerate(board.get_board()):
            for item in rank:
                
                if item != None and item.get_colour() == colour:
                    
                    # If the piece is a pawn handle only attacks
                    if item.get_type() == PAWN:
                        moves = item.get_attacks(board)
                    
                    # Otherwise, get moves
                    else:
                        moves = item.get_moves(board)
                        
                    attacks += moves
        
        return attacks
    
    
    def get_all_moves(self, board):
        """
        Method:
            Returns a list of all the possible moves for the
            current colour
            
        Params:
            board (Board)
        """
        # Initiate vars
        moves = []
        
        # Iterate over board
        for row, rank in enumerate(board.get_board()):
            for item in rank:
                
                # Piece is present, add to moves
                if item != None and item.get_colour() == board.get_colour():
                    moves.extend(item.get_moves(board))
        
        return moves
    
    
    def get_king_position(self, king):
        """
        Method:
            Returns the position of the given king
        
        Params:
            king (Piece)
        """
        return king.get_position()

    
    def look_for_check(self, board, king, attacks):
        """
        Method:
            Looks for if the king is in check
        
        Params:
            board (Board)
            king (Piece)
            attacks (list[Move])
        """
        kingPos = self.get_king_position(king)
        
        for move in attacks:
            if move.moveTo == kingPos:
                return True
        
        return False
    
    
    def generate_material_count(self, board):
        """
        Method:
            Returns the material count for both sides in a dictionary
        
        Params:
            board (Board)
        """
        # Initiate count dict
        count = {
            f'{WHITE} {PAWN}' : 0,
            f'{WHITE} {ROOK}' : 0,
            f'{WHITE} {BISHOP}' : 0,
            f'{WHITE} {QUEEN}' : 0,
            f'{WHITE} {KING}' : 0,
            f'{WHITE} {KNIGHT}' : 0,
            f'{BLACK} {PAWN}' : 0,
            f'{BLACK} {ROOK}' : 0,
            f'{BLACK} {BISHOP}' : 0,
            f'{BLACK} {QUEEN}' : 0,
            f'{BLACK} {KING}' : 0,
            f'{BLACK} {KNIGHT}' : 0
        }
        
        # Iterate over board
        for row, rank in enumerate(board.get_board()):
            for item in rank:
                
                # Piece is present, add to moves
                if item != None:
                    count[f'{item.get_colour()} {item.get_type()}'] += 1
        
        return count