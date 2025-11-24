"""
Imports
"""
try:
    from src.bitboard_based_classes.bit_move import BitMove
    from src.constants.constFilesAndRanks import *
    from src.constants.constPieces import *
except:
    from bitboard_based_classes.bit_move import BitMove
    from constants.constFilesAndRanks import *
    from constants.constPieces import *


"""
Functions
"""
def get_knight_moves(board, colour, mask):
    """
    Method:
        Returns a list of all possible moves for the 
        knight in a given position
    
    Params:
        board (Bitboard)
        colour (ENUM)
        mask (int)
    """
    # Get attacks and positions of the same colour pieces
    attackMask = get_knight_attacks(board, colour, mask)
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
    
    return moves


def get_knight_attacks(board, colour, mask=None):
    """
    Method:
        Returns a bitmask of all possible knight attacks
        in a given position. If mask is given, just return
        the attacks for that knight
    
    Params:
        board (Bitboard)
        colour (ENUM)
        mask (int)
    """
    # Get bitstring for the knight
    if mask is None:
        knightBitboard = board.get_board()[f'{colour} {KNIGHT}']
    else:
        knightBitboard = mask
    
    # Initiate vars
    attacks = 0
    shiftValues = [15, 17, -15, -17, 6, 10, -6, -10]
    
    # Obtain attacks
    for shift in shiftValues:
        # Shift bits and create a mask
        if shift > 0:
            targetMask = (knightBitboard << shift)
        else:
            targetMask = (knightBitboard >> abs(shift))
        
        # Wrap around prevention
        if shift in [-17, -10, 6, 15] and knightBitboard & A_FILE:
            continue
        elif shift in [-15, -6, 10, 17] and knightBitboard & H_FILE:
            continue
        elif shift in [-10, 6] and knightBitboard & B_FILE:
            continue
        elif shift in [10, -6] and knightBitboard & G_FILE:
            continue
        
        # Add attack to attacks
        attacks |= targetMask
    
    return attacks