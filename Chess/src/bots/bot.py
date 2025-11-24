"""
Imports
"""
try:
    from src.data_structures.transpositionNode import TranspositionNode
    from src.bots.static.move_order import *
    from src.bots.static.evaluation import evaluate_nuanced
    from src.bots.static.move_order import *
    from src.constants.constFlags import *
    from src.constants.constPieces import *
    from src.constants.constBounds import *
    from src.constants.constColours import *
except:
    from data_structures.transpositionNode import TranspositionNode
    from bots.static.evaluation import evaluate_nuanced
    from bots.static.move_order import *
    from bots.static.move_order import order_moves
    from constants.constFlags import *
    from constants.constPieces import *
    from constants.constBounds import *
    from constants.constColours import *
    
class Bot:
    
    def __init__(self, name, colour, depth, arbiter, moveGenerator):
        self.name = name
        self.colour = colour
        self.depth = depth
        self.arbiter = arbiter
        self.moveGenerator = moveGenerator
        self.transpositionTable = {}
        self.tt_hits = 0
        self.tt_lookups = 0
        
        self.killer_moves = {}
        self.max_killers = 2

        self.history = {}


    
    def evaluate(self, board):
        pass
    

    def alpha_beta_search(self, board, depth, alpha, beta, ply=0):
        """
        Alpha-beta search with transposition table, killer moves, and history heuristic
        """
        alphaOrigin = alpha
        zobrist = board.get_current_zobrist()
        ttMove = None
        
        # Check transposition table
        self.tt_lookups += 1
        
        if zobrist in self.transpositionTable:
            node = self.transpositionTable[zobrist]
            
            if node.best_move is not None:
                ttMove = node.best_move
            
            if node.depth >= depth:
                self.tt_hits += 1
                
                if node.flag == EXACT:
                    return node.score
                elif node.flag == LOWER:
                    alpha = max(alpha, node.score)
                elif node.flag == UPPER:
                    beta = min(beta, node.score)
                
                if alpha >= beta:
                    return node.score
        
        # Base case - leaf node
        if depth == 0:
            score = self.quiesce(board, alpha, beta)
            self.transpositionTable[zobrist] = TranspositionNode(0, score, EXACT, None)
            return score
        
        # Get all legal moves
        moves = self.moveGenerator.get_all_moves(board)
        filtered = self.arbiter.filter_moves(board, moves, board.get_colour())
        
        # Terminal position
        if not filtered:
            score = self.evaluate(board)
            self.transpositionTable[zobrist] = TranspositionNode(depth, score, EXACT, None)
            return score
        
        # Order moves with advanced heuristics
        filtered = order_moves(filtered, self.killer_moves, self.history, ttMove, ply)
        
        maximizingPlayer = (board.get_colour() == WHITE)
        bestMove = None
        
        if maximizingPlayer:
            value = float('-inf')
            
            for move in filtered:
                if move.get_flag() == PROMOTION:
                    move.make_move(promotionChoice=QUEEN)
                else:
                    move.make_move()
                
                if move.isCapture and depth == 1:
                    score = self.alpha_beta_search(board, depth, alpha, beta, ply+1)
                else:  
                    score = self.alpha_beta_search(board, depth-1, alpha, beta, ply+1)
                move.undo_move()
                
                if score > value:
                    value = score
                    bestMove = move
                
                alpha = max(alpha, value)
                
                # Beta cutoff - update killer and history
                if beta <= alpha:
                    store_killer_move(move, ply, self.killer_moves, self.max_killers)
                    update_history(move, depth, self.history)
                    break
        else:
            value = float('inf')
            
            for move in filtered:
                if move.get_flag() == PROMOTION:
                    move.make_move(promotionChoice=QUEEN)
                else:
                    move.make_move()
                
                score = self.alpha_beta_search(board, depth-1, alpha, beta, ply+1)
                move.undo_move()
                
                if score < value:
                    value = score
                    bestMove = move
                
                beta = min(beta, value)
                
                # Alpha cutoff - update killer and history
                if beta <= alpha:
                    store_killer_move(move, ply, self.killer_moves, self.max_killers)
                    update_history(move, depth, self.history)
                    break
        
        # Determine flag for TT storage
        if value <= alphaOrigin:
            flag = UPPER
        elif value >= beta:
            flag = LOWER
        else:
            flag = EXACT
        
        self.transpositionTable[zobrist] = TranspositionNode(depth, value, flag, bestMove)
        
        return value
    
    
    def find_best_move(self, board, depth):
        """
        Find best move with iterative deepening and aspiration windows
        """
        self.tt_hits = 0
        self.tt_lookups = 0
        clear_search_data(self.killer_moves, self.history) 
        
        bestMove = None
        prevScore = 0
        
        # Iteratively search from depth 1 to target depth
        for current_depth in range(1, depth + 1):
            
            # Aspiration window sizing
            if current_depth <= 2:
                # Use full window for shallow depths
                alpha, beta = float('-inf'), float('inf')
                
            else:
                # Use aspiration window based on previous score
                window_size = 50  # Can be tuned
                alpha = prevScore - window_size
                beta = prevScore + window_size
            
            # Try to search with aspiration window
            attempts = 0
            max_attempts = 3
            
            while attempts < max_attempts:
                bestScore = self._search_root(board, current_depth, alpha, beta)
                
                # Check if we failed high or low
                if bestScore <= alpha:
                    # Failed low - widen window downward
                    alpha = float('-inf')
                    attempts += 1
                elif bestScore >= beta:
                    # Failed high - widen window upward
                    beta = float('inf')
                    attempts += 1
                else:
                    # Search completed successfully within window
                    break
            
            # Update best move and score for next iteration
            zobrist = board.get_current_zobrist()
            if zobrist in self.transpositionTable:
                node = self.transpositionTable[zobrist]
                if node.best_move is not None:
                    bestMove = node.best_move
            
            prevScore = bestScore
        
        return bestMove
    
    def _search_root(self, board, depth, alpha, beta):
        """Helper method to search root with given alpha-beta window"""
        # Get all legal moves
        moves = self.moveGenerator.get_all_moves(board)
        filtered = self.arbiter.filter_moves(board, moves, self.colour)
        
        # Order moves using TT from previous depth
        zobrist = board.get_current_zobrist()
        ttMove = None
        
        if zobrist in self.transpositionTable:
            node = self.transpositionTable[zobrist]
            if node.best_move is not None:
                ttMove = node.best_move
        
        filtered = order_moves(filtered, self.killer_moves, self.history, ttMove, ply=0)
        
        alphaOrigin = alpha
        bestScore = float('-inf') if self.colour == WHITE else float('inf')
        bestMove = None
        
        # Search each move
        for move in filtered:
            if move.get_flag() == PROMOTION:
                move.make_move(promotionChoice=QUEEN)
            else:
                move.make_move()
            
            score = self.alpha_beta_search(board, depth - 1, alpha, beta, ply=1)
            move.undo_move()
            
            if self.colour == WHITE:
                if score > bestScore:
                    bestScore = score
                    bestMove = move
                alpha = max(alpha, bestScore)
            else:
                if score < bestScore:
                    bestScore = score
                    bestMove = move
                beta = min(beta, bestScore)
            
            # Early exit on cutoff
            if beta <= alpha:
                break
        
        # Store root position in TT
        if bestScore <= alphaOrigin:
            flag = UPPER
        elif bestScore >= beta:
            flag = LOWER
        else:
            flag = EXACT
        
        self.transpositionTable[zobrist] = TranspositionNode(depth, bestScore, flag, bestMove)
        
        return bestScore

    def perft(self, board, depth):
        """Performance test - counts leaf nodes at given depth"""
        if depth == 0:
            return 1
        
        nodes = 0
        moves = self.moveGenerator.get_all_moves(board)
        legal_moves = self.arbiter.filter_moves(board, moves, board.get_colour())
        
        for move in legal_moves:
            if move.get_flag() == PROMOTION:
                for piece in [QUEEN, ROOK, BISHOP, KNIGHT]:
                    move.make_move(promotionChoice=piece)
                    nodes += self.perft(board, depth - 1)
                    move.undo_move()
            else:
                move.make_move()
                nodes += self.perft(board, depth - 1)
                move.undo_move()
        
        return nodes

    def quiesce(self, board, alpha, beta, ply=0, max_ply=3):
        """
        Quiesce search using minimax with max depth limit
        """
        # Check max depth to prevent infinite loops
        if ply >= max_ply:
            return self.evaluate(board)
        
        staticEval = self.evaluate(board)
        
        # White's turn (maximizing)
        if board.get_colour() == WHITE:
            if staticEval >= beta:
                return beta
            if staticEval > alpha:
                alpha = staticEval
            
            moves = self.moveGenerator.get_all_moves(board)
            filtered = self.arbiter.filter_moves(board, moves, WHITE)
            
            for move in filtered:
                if not move.isCapture:
                    continue
                
                if move.get_flag() == PROMOTION:
                    move.make_move(QUEEN)
                else:
                    move.make_move()
                
                score = self.quiesce(board, alpha, beta, ply + 1, max_ply)
                move.undo_move()
                
                if score >= beta:
                    return beta
                if score > alpha:
                    alpha = score
            
            return alpha
        
        # Black's turn (minimizing)
        else:
            if staticEval <= alpha:
                return alpha
            if staticEval < beta:
                beta = staticEval
            
            moves = self.moveGenerator.get_all_moves(board)
            filtered = self.arbiter.filter_moves(board, moves, BLACK)
            
            for move in filtered:
                if not move.isCapture:
                    continue
                
                if move.get_flag() == PROMOTION:
                    move.make_move(QUEEN)
                else:
                    move.make_move()
                
                score = self.quiesce(board, alpha, beta, ply + 1, max_ply)
                move.undo_move()
                
                if score <= alpha:
                    return alpha
                if score < beta:
                    beta = score
            
            return beta