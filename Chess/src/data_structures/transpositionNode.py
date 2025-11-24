class TranspositionNode:
    def __init__(self, depth, score, flag, best_move):
        self.depth = depth # Depth of search
        self.score = score # Evaluation
        self.flag = flag   # Type: EXACT, LOWER, UPPER 
        self.best_move = best_move