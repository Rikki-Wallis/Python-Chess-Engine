"""
Imports
"""
import pygame as pg

try:
    from src.array_based_classes.normal_game import NormalGame
    from src.constants.constColours import *
    from src.constants.constFlags import *
    from src.bots.bot import Bot
    
except:
    from array_based_classes.normal_game import NormalGame
    from constants.constColours import *
    from constants.constFlags import *
    from bots.bot import Bot

"""
Classes
"""
class Engine2DGame(NormalGame):
    
    """ ---------------------------------------------------------- Constructor ----------------------------------------------------------"""
    
    
    def __init__(self, gui, arbiter, board, player1, player2):
        super().__init__(gui, arbiter, board, player1, player2)
        
        # Get colour user would like to play as
        humanColour = self.get_user_input()
        engineColour = BLACK if humanColour == WHITE else WHITE
        
        # Assign players
        self.player1 = humanColour
        self.player2 = engineColour
        
        # Create engine
        self.engineDepth = 2
        self.engine = Bot("Son Of Array", engineColour, self.engineDepth, self.arbiter, self.arbiter)
        
        
    """---------------------------------------------------------- Overridden Methods ------------------------------------------------------"""

    def get_user_input(self):
        """
        Method:
            Gets user input from terminal of which colour they
            want to play as
        """
        while True:
            colour = input(f"Enter colour to play as ({WHITE}/{BLACK}): ")
            
            if colour not in [WHITE, BLACK]:
                print(f"Invalid input, please enter {WHITE} or {BLACK}")
                continue
            else:
                return colour
    
    def player_2_move(self):
        """
        Method:
            Handles engines move
        """
        
        # Get best move
        move = self.engine.find_best_move(self.board)
        
        # Make sure move is not none
        if move is None:
            self.running = False
            return False
        
        move.make_move()
        pg.event.pump()
        
        # Update screen
        self.gui.draw_board()
        self.gui.draw_pieces(self.board)
        
        return True