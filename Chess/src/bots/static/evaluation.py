"""
Imports
"""
try:
    from src.constants.constColours import *
    from src.constants.evaluation.constBitMasks import *
    from src.constants.evaluation.constBonusAndPenalty import *
    from src.constants.evaluation.constPST import *
    from src.constants.evaluation.constStartingPositions import *
except:
    from constants.constColours import *
    from constants.evaluation.constBitMasks import *
    from constants.evaluation.constBonusAndPenalty import *
    from constants.evaluation.constPST import *
    from constants.evaluation.constStartingPositions import *

"""
Callable Methods
"""

def evaluate_nuanced(board, move_generator, arbiter):
    
    if arbiter.is_in_checkmate(board):
        return -1000000 if board.get_colour() == WHITE else 1000000
    
    elif arbiter.is_in_stalemate(board):
        return 0
    
    elif arbiter.is_in_insufficient_material(board):
        return 0
    
    elif arbiter.is_in_fifty_move_rule(board):
        return 0
    
    # Initiate score
    material_score = 0
    pst_score = 0
    score = 0
    
    """
    Methods in the loop include:
    1. Material count
    2. Piece square Tables
    
    Add extra in here if needed
    in the loop, otherwise create
    a function and call it outside
    """
    
    # Iterate over board
    for piece_attributes, bit_str in board.get_board().items():
        
        # Ignore occupancy masks
        if piece_attributes == BLACK or piece_attributes == WHITE:
            continue
        
        # Get piece type
        piece_attributes = piece_attributes.split(" ")
        type = piece_attributes[1]
        colour = piece_attributes[0]
        
        # Get piece value
        if colour == BLACK:
            piece_val = -PIECE_VALUE_MG[type]
        else:
            piece_val = PIECE_VALUE_MG[type]
        
        # Iterate over bitboard and add score
        while bit_str:
            # Fetch least significant bit that is set to 1 and obtain index
            lsb = bit_str & -bit_str
            index = lsb.bit_length() - 1
            
            # Add material to score
            material_score += piece_val
            
            # Add piece table score to score
            if colour == BLACK:
                pst_score -= PST_MG[colour][type][index]
            else:
                pst_score += PST_MG[colour][type][index]
            
            # Insentivise development
            if (1 << index) & STARTING_POSITIONS[f"{colour} {type}"]:
                if colour == BLACK:
                    score += STARTING_POSITIONS_PENALTIES[type]
                else:
                    score -= STARTING_POSITIONS_PENALTIES[type]
                
            # Remove the lsb from the bitboard
            bit_str &= bit_str - 1
    
    if material_score != 0:
        score += material_score*5
    
    score += material_score
    score += pst_score
    
    score += _mobility_threats(board, move_generator, arbiter)
    score += _update_space(board, move_generator)
    
    score += _evaluate_pawns(board.get_board()[f"{WHITE} {PAWN}"], board.get_board()[f"{BLACK} {PAWN}"])
    
    return score


def evaluate_material(board, move_generator, arbiter):
    
    if arbiter.is_in_checkmate(board):
        return -1000000 if board.get_colour() == WHITE else 1000000
    
    elif arbiter.is_in_stalemate(board):
        return 0
    
    elif arbiter.is_in_insufficient_material(board):
        return 0
    
    elif arbiter.is_in_fifty_move_rule(board):
        return 0
    
    # Initiate score
    score = 0
    
    # Iterate over board
    for piece_attributes, bit_str in board.get_board().items():
        
        # Ignore occupancy masks
        if piece_attributes == BLACK or piece_attributes == WHITE:
            continue
        
        # Get piece type
        piece_attributes = piece_attributes.split(" ")
        type = piece_attributes[1]
        colour = piece_attributes[0]
        
        # Get piece value
        if colour == BLACK:
            piece_val = -PIECE_VALUE_MG[type]
        else:
            piece_val = PIECE_VALUE_MG[type]
        
        # Iterate over bitboard and add score
        while bit_str:
            # Fetch least significant bit that is set to 1 and obtain index
            lsb = bit_str & -bit_str
            index = lsb.bit_length() - 1
            
            # Add material to score
            score += piece_val
            
            # Remove the lsb from the bitboard
            bit_str &= bit_str - 1
            
    return score


"""
Helper Methods
"""

def _mobility_threats(board, move_generator, arbiter):
    
    score = 0
    
    # Fetch all moves for both colours
    white_moves = move_generator.get_all_moves(board, search=WHITE)
    black_moves = move_generator.get_all_moves(board, search=BLACK)
    
    for move in white_moves:
        if move.isCheck:
            score += CHECK
    
    for move in black_moves:
        if move.isCheck:
            score -= CHECK
    
    # Filter moves
    white_moves = arbiter.filter_moves(board, white_moves, WHITE)
    black_moves = arbiter.filter_moves(board, black_moves, BLACK)
    
    # Add pure mobility to score
    score += len(white_moves) - len(black_moves)
    
    # Insentivise threats
    for move in white_moves:
        if move.isCapture:
            score += CAPTURE
    
    for move in black_moves:
        if move.isCapture:
            score -= CAPTURE
    
    
    return score


def _update_space(board, move_generator):
    score = 0
    score += bin(CENTER & ~move_generator.get_all_attacks(board, BLACK)).count('1')
    score -= bin(CENTER & ~move_generator.get_all_attacks(board, WHITE)).count('1')
    return score


def _evaluate_pawns(white_pawns, black_pawns):
    # Initiate score
    score = 0
    
    # Seperate pawns onto different files
    pawns_by_file_white = []
    pawns_by_file_black = []
    for file in FILES:
        pawns_by_file_white.append(file & white_pawns)
        pawns_by_file_black.append(file & black_pawns)
    
    score += _count_doubled_pawns(pawns_by_file_white) - _count_doubled_pawns(pawns_by_file_black)
    score += _count_isolated_pawns(pawns_by_file_white) -  _count_isolated_pawns(pawns_by_file_black) 
    score += _count_passed_pawns(pawns_by_file_white, black_pawns, WHITE) - _count_passed_pawns(pawns_by_file_black, white_pawns, BLACK) 

    return score


def _count_doubled_pawns(pawns_by_file):
    count = 0
    for pawns_on_file in pawns_by_file:
        num_pawns = bin(pawns_on_file).count('1')
        if num_pawns > 1:
            count += num_pawns - 1
    return count


def _count_isolated_pawns(pawns_by_file):
    count = 0
    
    for i, pawns_on_file in enumerate(pawns_by_file):
        if pawns_on_file == 0:
            continue
        
        l, r = i-1, i+1
        
        if not l < 0:
            l_pawns = pawns_by_file[l]
        else:
            l_pawns = 0
        
        if not r > 7:
            r_pawns = pawns_by_file[r]
        else:
            r_pawns = 0
        
        if r_pawns + l_pawns == 0:
            count += bin(pawns_on_file).count('1')

    return count


def _count_passed_pawns(pawns_by_file, opponent_pawns, colour):
    
    blocking_count = 0
    passed_count = 0
    
    for i, pawns_on_file in enumerate(pawns_by_file):
        
        if pawns_on_file == 0:
            continue
        
        # Obtain blocking file
        blocking_file = FILES[i]
        if colour == WHITE:
            shift = 8
        else:
            shift = -8
        
        # If white dynamically search the hsb otherwise search lsb
        blocking_mask = pawns_on_file | (opponent_pawns & blocking_file)
        msb = pawns_on_file.bit_length() - 1
        while True:
            
            if blocking_mask.bit_length() > 64 or blocking_mask <= 0 or msb + shift < 0:
                passed_count += 1
                break
            
            blocking_mask |= (1 << msb + shift)
            
            if colour == WHITE:
                msb += 8
            else:
                msb -= 8
            
            if blocking_mask & opponent_pawns:
                blocking_count += 1
    
    return passed_count * PASSED_PAWN_BONUS - blocking_count * BLOCKED