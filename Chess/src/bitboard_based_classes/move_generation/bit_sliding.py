"""
Imports
"""
try:
    from src.bitboard_based_classes.bit_move import BitMove
    from src.bitboard_based_classes.precomputation.precompute import generate_rook_movement_mask, generate_bishop_movement_mask
    from src.constants.constPieces import *
    from src.constants.constColours import *
    from src.constants.constMagics import *
except:
    from bitboard_based_classes.bit_move import BitMove
    from bitboard_based_classes.precomputation.precompute import generate_rook_movement_mask, generate_bishop_movement_mask
    from constants.constPieces import *
    from constants.constColours import *
    from constants.constMagics import *

"""
Functions
"""
def get_sliding_moves(board, colour, mask, pieceType, lookupTables):
    """
    Method:
        Returns a list of all possible moves for the 
        rook in a given position
    
    Params:
        board (Bitboard)
        colour (ENUM)
        mask (int)
        pieceType(ENUM)
        lookupTables(dict{dict})
    """
    # Get attacks for piece in current position
    moveMask = get_sliding_attacks(board, colour, mask, pieceType, lookupTables)
    
    # Initiate vars
    moves = []
    
    # Fetch all moves from the move mask
    while moveMask:
        # Fetch least significant bit that is set to 1 and obtain index
        lsb = moveMask & -moveMask
        index = lsb.bit_length() - 1
        
        # Create masks for the result of the move
        moveToMask = 0
        moveToMask = (1 << index)
        
        # Create the move and add to list
        moves.append(BitMove(board, mask, moveToMask))
        
        # Remove the lsb from the move mask
        moveMask &= moveMask - 1
    
    return moves


def get_sliding_attacks(board, colour, mask, pieceType, lookupTables):
    """
    Method:
        Returns a bitmask of all possible attacks for the
        the given piece in a position
        
    Params:
        board (Bitboard)
        colour (ENUM)
        mask (int)
        pieceType(ENUM)
        lookupTables(dict{dict})
    """
    # Initiate vars
    cColour = colour
    
    # Generate movementMask for piece
    if pieceType == ROOK:
        movementMask = generate_rook_movement_mask(mask)
    else:
        movementMask = generate_bishop_movement_mask(mask)
    
    # Fetch occupancy mask and obtain blockers
    occupancyMask = board.get_board()[WHITE] | board.get_board()[BLACK]
    blockers = movementMask & occupancyMask
    # Get position of piece
    i = (mask.bit_length()-1)
    
    # Obtain key to hashmap
    if pieceType == ROOK:
        key = (blockers*ROOK_MAGICS[i]) >> (ROOK_SHIFTS[i])
    else:
        key = (blockers*BISHOP_MAGICS[i]) >> (BISHOP_SHIFTS[i])
    
    # Obtain the correct lookup table
    if i < 0 or key not in lookupTables[pieceType][i]:
        return 0
    
    attackMask = lookupTables[pieceType][i][key]
    attackMask &= ~board.get_board()[cColour]
    
    return attackMask

def print_bitboard(bitboard):
    """
    Prints a 64-bit integer as an 8x8 chessboard.
    
    :param bitboard: 64-bit integer representing the bitboard
    """
    board = []
    for rank in range(8):
        row = []
        for file in range(8):
            # Calculate the bit position (0 is bottom-left, 63 is top-right)
            bit_position = rank * 8 + file
            # Check if the bit at the position is set
            row.append('1' if (bitboard & (1 << bit_position)) else '0')
        board.append(row)