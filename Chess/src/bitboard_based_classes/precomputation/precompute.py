"""
Imports
"""
import itertools

try:
    from src.constants.constFilesAndRanks import *
    from src.constants.constPieces import *
    from src.constants.constMagics import *
except:
    from constants.constFilesAndRanks import *
    from constants.constPieces import *
    from constants.constMagics import *


"""
Functions
"""
def generate_rook_movement_mask(rookMask):
    """
    Method:
        Generates the movement mask for a rook
        on a given square for an empty board.
    
    Params:
        rookMask (int)
    """
    # Fetch current rank and file mask the rook is on
    rankMask = 0
    fileMask = 0
    
    if rookMask & RANK1:
        rankMask = RANK1
    elif rookMask & RANK2:
        rankMask = RANK2
    elif rookMask & RANK3:
        rankMask = RANK3
    elif rookMask & RANK4:
        rankMask = RANK4
    elif rookMask & RANK5:
        rankMask = RANK5
    elif rookMask & RANK6:
        rankMask = RANK6
    elif rookMask & RANK7:
        rankMask = RANK7
    elif rookMask & RANK8:
        rankMask = RANK8

    if rookMask & A_FILE:
        fileMask = A_FILE
    elif rookMask & B_FILE:
        fileMask = B_FILE
    elif rookMask & C_FILE:
        fileMask = C_FILE
    elif rookMask & D_FILE:
        fileMask = D_FILE
    elif rookMask & E_FILE:
        fileMask = E_FILE
    elif rookMask & F_FILE:
        fileMask = F_FILE
    elif rookMask & G_FILE:
        fileMask = G_FILE
    elif rookMask & H_FILE:
        fileMask = H_FILE
    
    # Combine the rank and file masks to get the movement mask
    movementMask = rankMask | fileMask
    # Remove the rook's current position from the movement mask
    movementMask &= ~rookMask
    
    return movementMask


def generate_bishop_movement_mask(bishopMask):
    """
    Method:
        Generates the movement mask for a bishop
        on a given square for an empty board.
    
    Params:
        bishopMask (int)
    """
    # Fetch current diag and anti-diag the bishop is on
    diagMask = 0
    antiDiagMask = 0
    
    if bishopMask & DIAG_0:
        diagMask = DIAG_0
    elif bishopMask & DIAG_1:
        diagMask = DIAG_1
    elif bishopMask & DIAG_2:
        diagMask = DIAG_2
    elif bishopMask & DIAG_3:
        diagMask = DIAG_3
    elif bishopMask & DIAG_4:
        diagMask = DIAG_4
    elif bishopMask & DIAG_5:
        diagMask = DIAG_5
    elif bishopMask & DIAG_6:
        diagMask = DIAG_6
    elif bishopMask & DIAG_7:
        diagMask = DIAG_7
    elif bishopMask & DIAG_8:
        diagMask = DIAG_8
    elif bishopMask & DIAG_9:
        diagMask = DIAG_9
    elif bishopMask & DIAG_10:
        diagMask = DIAG_10
    elif bishopMask & DIAG_11:
        diagMask = DIAG_11
    elif bishopMask & DIAG_12:
        diagMask = DIAG_12
    
    if bishopMask & DIAG_13:
        antiDiagMask = DIAG_13
    elif bishopMask & DIAG_14:
        antiDiagMask = DIAG_14
    elif bishopMask & DIAG_15:
        antiDiagMask = DIAG_15
    elif bishopMask & DIAG_16:
        antiDiagMask = DIAG_16
    elif bishopMask & DIAG_17:
        antiDiagMask = DIAG_17
    elif bishopMask & DIAG_18:
        antiDiagMask = DIAG_18
    elif bishopMask & DIAG_19:
        antiDiagMask = DIAG_19
    elif bishopMask & DIAG_20:
        antiDiagMask = DIAG_20
    elif bishopMask & DIAG_21:
        antiDiagMask = DIAG_21
    elif bishopMask & DIAG_22:
        antiDiagMask = DIAG_22
    elif bishopMask & DIAG_23:
        antiDiagMask = DIAG_23
    elif bishopMask & DIAG_24:
        antiDiagMask = DIAG_24
    elif bishopMask & DIAG_25:
        antiDiagMask = DIAG_25

    # Get the movement mask
    movementMask = diagMask | antiDiagMask
    # Remove the bishop's current position from the movement mask
    movementMask &= ~bishopMask
    
    return movementMask


def generate_all_blocker_configs(movementMask):
    """
    Method:
        Returns a list of all possible blocker combinations
        of a given movement mask
    """
    powerset = []
    bitPositions = [i for i in range(64) if (movementMask & (1 << i)) != 0]
    
    # Iterate through all possible lengths of subsets, from 0 to the length of the bitstring
    for r in range(len(bitPositions) + 1):
        # Generate combinations of bits of current length
        for combo in itertools.combinations(bitPositions, r):
            # Add subset into powerset
            subset = sum(1 << pos for pos in combo)
            powerset.append(subset)
    
    return powerset


def generate_attack_mask(pieceType, pieceMask, movementMask, blockers, shiftValues):
    attacks = 0
    
    for shift, boundary in shiftValues:
        currentPos = pieceMask
    
        while True:
            # Check for invalid positions
            if currentPos.bit_length() > 64 or currentPos == 0:
                break
            
            # For rooks, check boundary BEFORE shifting
            if pieceType == ROOK and (currentPos & boundary):
                break
            
            # Shift to the next position
            if shift > 0:
                currentPos <<= shift
            else:
                currentPos >>= abs(shift)
            
            # Check if the new position is valid
            if currentPos.bit_length() > 64 or currentPos == 0:
                break
            
            # Add to attacks based on piece type
            if pieceType == ROOK:
                attacks |= currentPos
            elif currentPos & movementMask:
                attacks |= currentPos
            
            # Check for blockers
            if currentPos & blockers:
                attacks |= currentPos
                break
                
            # For bishops, check boundary AFTER shifting and adding to attacks
            if pieceType == BISHOP and (currentPos & boundary):
                break
    
    return attacks


def generate_lookup_table(pieceType):
    """
    Method:
        generates the lookup table for the
        given piece type
    
    Params:
        pieceType (ENUM)
    """
    # Initiate vars
    magicBitboard = {}
    currentMask = 0
    maxIndex = 64
    
    if pieceType == BISHOP:
        shiftValues = [(7, H_FILE | RANK8), (9, A_FILE | RANK8), (-7, A_FILE | RANK1), (-9, H_FILE | RANK1)]
    else:
        shiftValues = [(1, H_FILE), (-1, A_FILE), (8, RANK8), (-8, RANK1)]
    
    for i in range(maxIndex):
        currentMask = 1 << i
        
        magicBitboard[i] = {}
        
        # Generate movement mask for the rook at the current square
        if pieceType == ROOK:
            movementMask = generate_rook_movement_mask(currentMask)
        else:
            movementMask = generate_bishop_movement_mask(currentMask)
        # Generate all possible blocker configurations for the movement mask
        blockerConfigs = generate_all_blocker_configs(movementMask)
        
        # Generate the attack mask for each blocker configuration
        for blockers in blockerConfigs:
            attackMask = generate_attack_mask(pieceType, currentMask, movementMask, blockers, shiftValues)
            
            # Obtain key to lookup table
            if pieceType == ROOK:
                key = (blockers*ROOK_MAGICS[i]) >> (ROOK_SHIFTS[i])
                
            else:
                key = (blockers*BISHOP_MAGICS[i]) >> (BISHOP_SHIFTS[i])
            
            # Add to lookup table
            magicBitboard[i][key] = attackMask
        
        currentMask &= 0
    
    return magicBitboard