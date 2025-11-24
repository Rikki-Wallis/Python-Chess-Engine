"""
Imports
"""
import pygame as pg

try:
    from src.bitboard_based_classes.bit_game import BitGame
    from src.constants.constColours import *
    from src.constants.constFlags import *
except:
    from bitboard_based_classes.bit_game import BitGame
    from constants.constColours import *
    from constants.constFlags import *
    

"""
Classes
"""
class EngineBitboardGame(BitGame):
    
    """ ---------------------------------------------------------- Constructor ----------------------------------------------------------"""
    
    
    def __init__(self, gui, arbiter, board, player1, player2, engine):
        super().__init__(gui, arbiter, board, player1, player2)
        
        # Assign players
        self.player1 = player1
        self.player2 = player2
        self.engine = engine
        
        
    """---------------------------------------------------------- Overridden Methods ------------------------------------------------------"""
    
    def player_2_move(self):
        """
        Method:
            Handles engines move
        """
        
        # TODO: Draw monkey thinking
        self.gui.draw_thinking()
        #self.gui.draw_evaluation_bar(self.engine.evaluate(self.board))
        
        # Get best move
        move = self.engine.find_best_move(self.board, self.engine.depth)
        
        # Make sure move is not none
        if move is None:
            self.running = False
            return False
        
        move.make_move()
        pg.event.pump()
        
        # TODO: draw monkey not thinking
        self.gui.draw_waiting()
        self.gui.draw_evaluation_bar(self.engine.evaluate(self.board))
        
        # Update screen
        self.gui.draw_board()
        self.gui.draw_pieces(self.board)
        
        return True