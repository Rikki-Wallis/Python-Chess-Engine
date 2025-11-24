# TODO: Add castling moves
"""
Imports
"""
try:
    from src.bitboard_based_classes.bit_move import BitMove
    from src.constants.constCastlingBoards import *
    from src.constants.constFlags import *
    from src.constants.constColours import *
    from src.constants.constPieces import *
    from src.constants.constFilesAndRanks import *

except:
    from bitboard_based_classes.bit_move import BitMove
    from constants.constCastlingBoards import *
    from constants.constFlags import *
    from constants.constColours import *
    from constants.constPieces import *
    from constants.constFilesAndRanks import *

"""
Functions
"""
def get_king_moves(board, colour, mask):
    """
    Method:
        Returns a list of all possible moves for the 
        king in a given position
    
    Params:
        board (Bitboard)
        colour (ENUM)
        mask (int)
    """
    # There will always only be one king of each colour so we can use the attack mask directly
    attackMask = get_king_attacks(board, colour)
    # Get bitstring for all pieces of the same colour
    occupancyMask = board.get_board()[f'{colour}']
    
    # Initiate vars
    moveMask = attackMask & ~occupancyMask
    moves = []
    
    # Fetch all moves from the move mask
    while moveMask:
        # Fetch least significant bit that is set to 1 and obtain index
        lsb = moveMask & -moveMask
        index = lsb.bit_length() - 1
        
        # Create masks for the result of the move
        moveToMask = 0
        moveToMask |= (1 << index)
        
        # Create the move and add to list
        moves.append(BitMove(board, mask, moveToMask))
        
        # Remove the lsb from the move mask
        moveMask &= moveMask - 1
    
    # Add castling
    if can_short_castle(board, colour):
        if colour == WHITE:
            moves.append(BitMove(board, mask, WHITE_MOVETO_SHORT_CASTLE_POS, flag=SHORT_CASTLE))
        else:
            moves.append(BitMove(board, mask, BLACK_MOVETO_SHORT_CASTLE_POS, flag=SHORT_CASTLE))
    
    if can_long_castle(board, colour):
        if colour == WHITE:
            moves.append(BitMove(board, mask, WHITE_MOVETO_LONG_CASTLE_POS, flag=LONG_CASTLE))
        else:
            #print(bin(BLACK_MOVETO_LONG_CASTLE_POS))
            moves.append(BitMove(board, mask, BLACK_MOVETO_LONG_CASTLE_POS, flag=LONG_CASTLE))
    
    return moves
    
    
def get_king_attacks(board, colour, mask=None):
    """
    Method:
        Returns a bit string where all 1s represent
        squares that all of the combined pieces of
        the king can attack
    
    Params:
        board (Bitboard)
        colour (ENUM)
    """
    if mask is None:
        kingBitboard = board.get_board()[f'{colour} {KING}']
    else:
        kingBitboard = mask

    attacks = 0
    shiftValues = [1, 7, 8, 9, -1, -7, -8, -9]

    for shift in shiftValues:
        
        # Prevent wraparound
        if shift in [1, -7, 9] and (kingBitboard & H_FILE):
            continue 
        if shift in [-1, 7, -9] and (kingBitboard & A_FILE):
            continue 

        # Apply shift after checking
        if shift > 0:
            targetMask = kingBitboard << shift
        else:
            targetMask = kingBitboard >> abs(shift)

        attacks |= targetMask

    return attacks



def can_short_castle(board, colour):
    """
    Method:
        Returns true if the given colour's king
        can perform a short castle in the current
        position
    
    Params:
        board (Bitboard)
        colour (ENUM)
    """
    # Fetch necassary variables
    timesKingMoved = board.get_king_moved(colour)
    timesRookMoved = board.get_rook_moved(colour, SHORT)
    occupancyMask = board.get_board()[WHITE] | board.get_board()[BLACK]
    rookPos = board.get_rook_pos()[f'{colour} {SHORT}']
    
    if colour == WHITE:
        emptyPos = WHITE_SHORT_EMPTY_CASTLE_POS
        rookDefaultPos = WHITE_SHORT_ROOK_POS
    
    else:
        emptyPos = BLACK_SHORT_EMPTY_CASTLE_POS
        rookDefaultPos = BLACK_SHORT_ROOK_POS
    
    # Check if the current position meets requirements
    if (timesKingMoved < 1 and timesRookMoved < 1) and not occupancyMask & emptyPos and rookPos & rookDefaultPos:
        return True
    
    return False


def can_long_castle(board, colour):
    """
    Method:
        Returns true if the given colour's king
        can perform a long castle in the current
        position
    
    Params:
        board (Bitboard)
        colour (ENUM)
    """
    # Fetch necassary variables
    timesKingMoved = board.get_king_moved(colour)
    timesRookMoved = board.get_rook_moved(colour, LONG)
    occupancyMask = board.get_board()[WHITE] | board.get_board()[BLACK]
    rookPos = board.get_rook_pos()[f'{colour} {LONG}']
    
    if colour == WHITE:
        emptyPos = WHITE_LONG_EMPTY_CASTLE_POS
        rookDefaultPos = WHITE_LONG_ROOK_POS
    
    else:
        emptyPos = BLACK_LONG_EMPTY_CASTLE_POS
        rookDefaultPos = BLACK_LONG_ROOK_POS
    # Check if the current position meets requirements
    if (timesKingMoved < 1 and timesRookMoved < 1) and not occupancyMask & emptyPos and rookPos & rookDefaultPos:
        return True

    return False