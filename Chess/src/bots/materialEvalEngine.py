try:
    from src.bots.bot import Bot
    from src.bots.static.evaluation import evaluate_material
except:
    from bots.bot import Bot
    from bots.static.evaluation import evaluate_material
    
class MaterialEngine(Bot):
    def __init__(self, name, colour, depth, arbiter, moveGenerator):
        super().__init__(name, colour, depth, arbiter, moveGenerator)
        
    def evaluate(self, board):
        return evaluate_material(board, self.moveGenerator, self.arbiter)