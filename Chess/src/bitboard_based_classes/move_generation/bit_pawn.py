# TODO: Add enpassant
"""
Imports
"""
try:
    from src.bitboard_based_classes.bit_move import BitMove
    from src.constants.constFilesAndRanks import *
    from src.constants.constFlags import *
    from src.constants.constColours import *
    from src.constants.constPieces import *
except:
    from bitboard_based_classes.bit_move import BitMove
    from constants.constFilesAndRanks import *
    from constants.constFlags import *
    from constants.constColours import *
    from constants.constPieces import *

"""
Functions
"""
def get_pawn_moves(board, colour, mask):
    """
    Method:
        Returns a list of all possible moves for the 
        pawn in a given position
    
    Params:
        board (Bitboard)
        colour (ENUM)
        mask (int)
    """
    # Fetch attack mask
    attackMask = get_pawn_attacks(board, colour, mask)
    # Get bitstring for all pieces of the same colour
    friendlyMask = board.get_board()[f'{colour}']
    # Get bitstring for all pieces of the opposite colour
    enemyMask = board.get_board()[f'{BLACK if colour == WHITE else WHITE}']
    
    # Promotion Specific bitmask
    promotionRank = RANK8 if colour == WHITE else RANK1
    
    # Initiate vars
    attackMask &= enemyMask
    moves = []
    
    # Determine if single or double move
    if (colour == WHITE and mask & RANK2) or (colour == BLACK and mask & RANK7):
        shiftValues = [8, 16]
    else:
        shiftValues = [8]
    
    # Obtain a move mask
    for shift in shiftValues:
        if colour == WHITE:
            targetMask = (mask << shift)
        else:
            targetMask = (mask >> shift)
        
        # If target is occupied, skip
        if targetMask & (friendlyMask | enemyMask):
            break
        
        if targetMask & promotionRank:
            moves.append(BitMove(board, mask, targetMask, flag=PROMOTION))
        else:
            # Create the move and add to list
            moves.append(BitMove(board, mask, targetMask))
    
    # Add attacks to move
    while attackMask:
        # Fetch least significant bit that is set to 1 and obtain index
        lsb = attackMask & -attackMask
        index = lsb.bit_length() - 1
        
        # Create masks for the result of the move
        moveToMask = 0
        moveToMask |= (1 << index)
        
        # Create the move and add to list
        if moveToMask & promotionRank:
            moves.append(BitMove(board, mask, moveToMask, flag=PROMOTION))
        else:
            moves.append(BitMove(board, mask, moveToMask))
        
        # Remove the lsb from the move mask
        attackMask &= attackMask - 1
    
    # Add possible enpassants
    
    # Define variables
    if colour == WHITE:
        # Fetch masks
        enemyStartingRank = RANK7
        enpassantTarget = RANK5
        # Fetch target squares
        leftMoveTo = mask << 9
        rightMoveTo = mask << 7
        
    else:
        # Fetch masks
        enemyStartingRank = RANK2
        enpassantTarget = RANK4
        # Fetch target squares
        leftMoveTo = mask >> 7
        rightMoveTo = mask >> 9
    
    leftBoundary = A_FILE
    rightBoundary = H_FILE
    leftTargetSquare = mask << 1
    rightTargetSquare = mask >> 1
    
    # Early exit conditions
    if not enpassantTarget & mask:
        return moves
    
    lastMove = board.get_last_move()
    
    if lastMove is None:
        return moves
    
    previousType = lastMove.pieceType
    
    if not previousType == PAWN:
        return moves
    
    previousMoveTo = lastMove.moveTo
    previousMoveFrom = lastMove.moveFrom
    
    if not previousMoveTo & enpassantTarget:
        return moves

    if not previousMoveFrom & enemyStartingRank:
        return moves
    
    # We have eliminated general cases, now find if the pawn is in the correct position to be taken
    # Boundary check
    checkLeft = True
    checkRight = True
    if leftBoundary & mask:
        checkRight = False
    elif rightBoundary & mask:
        checkLeft = False
    
    # Check the target square where if the enemy pawn exists an enpassant can be made
    if checkLeft and leftTargetSquare & previousMoveTo:
        moves.append(BitMove(board, mask, leftMoveTo, flag=ENPASSANT))
    elif checkRight and rightTargetSquare & previousMoveTo:
        moves.append(BitMove(board, mask, rightMoveTo, flag=ENPASSANT))

    return moves


def get_pawn_attacks(board, colour, mask=None):
    """
    Method:
        Returns an attack mask for the pawns 
        in a given position. If no mask is given,
        return the attacks for all pawns. Otherwise,
        return the attacks for just the pawn provided
    
    Params:
        board (Bitboard)
        colour (ENUM)
        mask (int) 
    """
    # Fetch pawns bitboard
    if mask is None:
        pawnsBitboard = board.get_board()[f'{colour} {PAWN}']
    else:
        pawnsBitboard = mask
    
    # Shift in correct position
    if colour == WHITE:
        leftAttacks = (pawnsBitboard & ~H_FILE) << 9
        rightAttacks = (pawnsBitboard & ~A_FILE) << 7

    else:
        leftAttacks = (pawnsBitboard & ~H_FILE) >> 7
        rightAttacks = (pawnsBitboard & ~A_FILE) >> 9
    
    attacks = leftAttacks | rightAttacks

    return attacks
