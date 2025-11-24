"""
Imports
"""
import random
import sys
import os
# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

try:
    from src.constants.constPieces import *
    from src.constants.constMagics import *
    from src.bitboard_based_classes.precomputation.precompute import generate_bishop_movement_mask, generate_rook_movement_mask, generate_all_blocker_configs
except:
    from constants.constPieces import *
    from constants.constMagics import *
    from bitboard_based_classes.precomputation.precompute import generate_bishop_movement_mask, generate_rook_movement_mask, generate_all_blocker_configs

"""
Functions
"""
def generate_magic_numbers(pieceType):
    """
    Method:
        Generates magic numbers for rooks
    """
    # Initiate vars
    pieceMask = 0
    clearMask = 0
    magicNumbers = []
    
    # Iterate through each square in the board
    for i in range(64):
        
        # Add a bit to the current index
        pieceMask = 1 << i
        
        # Generate blockers
        if pieceType == ROOK:
            movementMask = generate_rook_movement_mask(pieceMask)
        elif pieceType == BISHOP:
            movementMask = generate_bishop_movement_mask(pieceMask)
        
        blockers = generate_all_blocker_configs(movementMask)
        
        # Find magic number
        while True:
            found = False
            magicNumber = random.randint(0, 0b1111111111111111111111111111111111111111111111111111111111111111) & random.randint(0, 0b1111111111111111111111111111111111111111111111111111111111111111)
            
            # Hold key values
            keys = []
        
            # Iterate through each blocker
            for idx, blocker in enumerate(blockers):
                key = (blocker*magicNumber) >> (ROOK_SHIFTS[i])
                
                if key in keys:
                    break
                elif idx == len(blockers) - 1:
                    found = True
                    break
                else:
                    keys.append(key)
                
            if found:
                print(f'Found magic number for index {i}: {magicNumber}')
                magicNumbers.append(magicNumber)
                break
        
        pieceMask &= clearMask
        
    return magicNumbers

if __name__ == "__main__":
    print("Generating rook magics...")
    rookMagics = generate_magic_numbers(ROOK)
    print("Rook magics generated:")
    print(str(rookMagics))
    
    print("Generating bishop magics...")
    bishopMagics = generate_magic_numbers(BISHOP)
    print("Bishop magics generated:")
    print(str(bishopMagics))