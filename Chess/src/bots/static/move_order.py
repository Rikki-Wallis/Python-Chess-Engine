"""
Imports
"""
try:
    from src.constants.evaluation.constBonusAndPenalty import *
except:
    from constants.evaluation.constBonusAndPenalty import *

"""
Callable Methods
"""
def order_moves(moves, killer_moves, history, ttMove=None, ply=0):
    """
    Enhanced move ordering with killer and history heuristics
    
    Priority:
    1. TT move (from previous search)
    2. Captures (sorted by MVV-LVA)
    3. Killer moves (non-captures that caused cutoffs)
    4. History moves (quiet moves with good history scores)
    5. Other quiet moves
    """
    if not moves:
        return moves
    
    tt_moves = []
    captures = []
    killers = []
    quiets = []
    
    for move in moves:
        # TT move gets highest priority
        if ttMove and moves_equal(move, ttMove):
            tt_moves.append(move)
        elif move.get_is_capture():
            captures.append((move, score_capture(move)))
        elif is_killer_move(move, ply, killer_moves):
            # Killer moves are quiet moves that caused cutoffs
            killers.append(move)
        else:
            # Score quiet moves by history heuristic
            quiets.append((move, get_history_score(move, history)))
    
    # Sort captures by MVV-LVA
    captures.sort(key=lambda x: x[1], reverse=True)
    captures = [move for move, _ in captures]
    
    # Sort quiet moves by history score
    quiets.sort(key=lambda x: x[1], reverse=True)
    quiets = [move for move, _ in quiets]
    
    return tt_moves + captures + killers + quiets


"""
Helper Methods
"""
def moves_equal(move1, move2):
    """Check if two moves are the same"""
    if move2 is None:
        return False
    return (move1.moveFrom & move2.moveFrom and move1.moveTo & move2.moveTo)


def score_capture(move):
    """Score captures using MVV-LVA"""
    victimVal = 0
    if move.targetType:
        victimVal = abs(PIECE_VALUE_MG[f'{move.targetType}'])
    
    attackerVal = abs(PIECE_VALUE_MG[f'{move.pieceType}'])
    
    return victimVal * 10 - attackerVal


def clear_search_data(killer_moves, history):
    """Clear killer moves and history for a new search"""
    killer_moves.clear()
    history.clear()


def get_move_key(move):
    """Generate a key for storing move in killer/history tables"""
    return (move.pieceType, move.moveFrom.bit_length() - 1, move.moveTo.bit_length() - 1)


def store_killer_move(move, depth, killer_moves, max_killers):
    """Store a killer move at the given depth"""
    # Don't store captures as killers
    if move.get_is_capture():
        return
    
    move_key = get_move_key(move)
    
    if depth not in killer_moves:
        killer_moves[depth] = []
    
    # If this move is already a killer, don't duplicate
    if move_key in killer_moves[depth]:
        return
    
    # Add new killer and keep only the most recent ones
    killer_moves[depth].insert(0, move_key)
    if len(killer_moves[depth]) > max_killers:
        killer_moves[depth].pop()


def is_killer_move(move, depth, killer_moves):
    """Check if a move is a killer move at this depth"""
    if depth not in killer_moves:
        return False
    
    move_key = get_move_key(move)
    return move_key in killer_moves[depth]


def update_history(move, depth, history):
    """Update history heuristic for a move that caused a cutoff"""
    if move.get_is_capture():
        return
    
    move_key = get_move_key(move)
    
    if move_key not in history:
        history[move_key] = 0
    
    # Bonus increases with depth
    history[move_key] += depth * depth


def get_history_score(move, history):
    """Get the history score for a move"""
    move_key = get_move_key(move)
    return history.get(move_key, 0)