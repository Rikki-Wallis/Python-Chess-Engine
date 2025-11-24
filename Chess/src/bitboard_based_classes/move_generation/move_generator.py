"""
Imports
"""
try:    
    from src.bitboard_based_classes.move_generation.bit_king import get_king_moves, get_king_attacks
    from src.bitboard_based_classes.move_generation.bit_knight import get_knight_moves, get_knight_attacks
    from src.bitboard_based_classes.move_generation.bit_pawn import get_pawn_moves, get_pawn_attacks
    from src.bitboard_based_classes.move_generation.bit_sliding import get_sliding_moves, get_sliding_attacks
    from src.bitboard_based_classes.precomputation.precompute import generate_lookup_table
    from src.constants.constPieces import *
    from src.constants.constColours import *

except:
    from bitboard_based_classes.move_generation.bit_king import get_king_moves, get_king_attacks
    from bitboard_based_classes.move_generation.bit_knight import get_knight_moves, get_knight_attacks
    from bitboard_based_classes.move_generation.bit_pawn import get_pawn_moves, get_pawn_attacks
    from bitboard_based_classes.move_generation.bit_sliding import get_sliding_moves, get_sliding_attacks
    from bitboard_based_classes.precomputation.precompute import generate_lookup_table
    from constants.constPieces import *
    from constants.constColours import *


"""
Classes
"""

class MoveGenerator:
    def __init__(self):
        self.rookLookupTable = generate_lookup_table(ROOK)
        self.bishopLookupTable = generate_lookup_table(BISHOP)
        
        self.lookUps = {
            ROOK : self.rookLookupTable,
            BISHOP : self.bishopLookupTable
        }
    
    
    def get_moves(self, board, colour, type, mask):
        """
        Method:
            Parses the piece type and colour to their designated
            get_moves function
        
        Params:
            board (BitBoard)
            colour (str)
            type (str)
            mask (int)    
        """
        if type == KING:
            return get_king_moves(board, colour, mask)
        elif type == QUEEN:
            rookMoves = get_sliding_moves(board, colour, mask, ROOK, self.lookUps)
            bishopMoves = get_sliding_moves(board, colour, mask, BISHOP, self.lookUps)
            
            if rookMoves is None and bishopMoves is None:
                return []
            elif bishopMoves is None:
                return rookMoves
            elif rookMoves is None:
                return bishopMoves
            else:
                return bishopMoves + rookMoves
            
        elif type == ROOK:
            return get_sliding_moves(board, colour, mask, ROOK, self.lookUps)
        elif type == BISHOP:
            return get_sliding_moves(board, colour, mask, BISHOP, self.lookUps)
        elif type == KNIGHT:
            return get_knight_moves(board, colour, mask)
        elif type == PAWN:
            return get_pawn_moves(board, colour, mask)
    
    
    def get_all_moves(self, board, search=None):
        """
        Method:
            Returns all the possible moves for a colour
            in a position
        
        Params:
            board (BitBoard)
            colour (ENUM)
        """
        # Initiate vars
        allMoves = []
        
        if search:
            currentColour = search
        else:
            currentColour = board.get_colour()
        
        # Iterate over all pieces
        for pieceAttribtutes, bitboard in board.get_board().items():
            
            # Ignore non important items
            if pieceAttribtutes == BLACK or pieceAttribtutes == WHITE:
                continue
            
            # Fetch piece attributes
            pieceAttribtutes = pieceAttribtutes.split()
            pType = pieceAttribtutes[1]
            pColour = pieceAttribtutes[0]
            
            if pColour != currentColour:
                continue
            
            # Fetch all pieces of that type and find moves
            while bitboard:
                # Fetch least significant bit that is set to 1 and obtain index
                lsb = bitboard & -bitboard
                index = lsb.bit_length() - 1
                
                # Create the mask for that piece
                pieceMask = 0
                pieceMask |= (1 << index)
                
                # Fetch moves for that piece and add to all moves
                moves = self.get_moves(board, pColour, pType, pieceMask)
                
                if moves is not None:
                    allMoves.extend(moves)
                
                # Remove the lsb from the bitboard
                bitboard &= bitboard - 1
            
        return allMoves
    
    
    def get_all_attacks(self, board, colour):
        """
        Method:
            Returns all attacks for the given colour
            on the board
        
        Params:
            board (BitBoard)
            colour (ENUM)
        """
        # Initiate the attack mask
        attacks = 0
        
        for pieceAttributes, bitboard in board.get_board().items():
            
            # Ignore non important items
            if pieceAttributes == BLACK or pieceAttributes == WHITE:
                continue
            
            # Split attributes
            pieceAttributes = pieceAttributes.split()
            type = pieceAttributes[1]
            pieceColour = pieceAttributes[0]
            
            # Only get attacks for the given colour
            if pieceColour != colour:
                continue
            
            if type == KING:
                attacks |= get_king_attacks(board, colour, bitboard)
            
            elif type == QUEEN:
                while bitboard:
                    # Fetch least significant bit that is set to 1 and obtain index
                    lsb = bitboard & -bitboard
                    index = lsb.bit_length() - 1
                    
                    # Create the mask for that piece
                    pieceMask = 0
                    pieceMask |= (1 << index)
                    
                    attacks |= get_sliding_attacks(board, colour, pieceMask, ROOK, self.lookUps)
                    attacks |= get_sliding_attacks(board, colour, pieceMask, BISHOP, self.lookUps)
                    
                    # Remove the lsb from the bitboard
                    bitboard &= bitboard - 1

                
            elif type == ROOK:
                while bitboard:
                    # Fetch least significant bit that is set to 1 and obtain index
                    lsb = bitboard & -bitboard
                    index = lsb.bit_length() - 1
                    
                    # Create the mask for that piece
                    pieceMask = 0
                    pieceMask |= (1 << index)
                    
                    attacks |= get_sliding_attacks(board, colour, pieceMask, ROOK, self.lookUps)
                    
                    # Remove the lsb from the bitboard
                    bitboard &= bitboard - 1
            
            elif type == BISHOP:
                while bitboard:
                    # Fetch least significant bit that is set to 1 and obtain index
                    lsb = bitboard & -bitboard
                    index = lsb.bit_length() - 1
                    
                    if index > 0:
                        
                        # Create the mask for that piece
                        pieceMask = 0
                        pieceMask |= (1 << index)
                        
                        attacks |= get_sliding_attacks(board, colour, pieceMask, BISHOP, self.lookUps)
                    
                    # Remove the lsb from the bitboard
                    bitboard &= bitboard - 1
            
            elif type == KNIGHT:
                while bitboard:
                    # Fetch least significant bit that is set to 1 and obtain index
                    lsb = bitboard & -bitboard
                    index = lsb.bit_length() - 1
                    
                    if index > 0:
                        
                        # Create the mask for that piece
                        pieceMask = 0
                        pieceMask |= (1 << index)
                        
                        attacks |= get_knight_attacks(board, colour, pieceMask)
                    
                    # Remove the lsb from the bitboard
                    bitboard &= bitboard - 1
                
            elif type == PAWN:
                attacks |= get_pawn_attacks(board, colour, bitboard)
            
        return attacks