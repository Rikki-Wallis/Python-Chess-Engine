"""
Imports
"""
import pygame as pg

try:
    from src.base_classes.game import Game
    from src.constants.constFlags import *
except:
    from base_classes.game import Game
    from constants.constFlags import *


"""
Classes
"""
class NormalGame(Game):
    """---------------------------------------------------------- Super Methods ----------------------------------------------------------"""
    
    def __init__(self, gui, arbiter, board, player1, player2):
        super().__init__(gui, arbiter, board, player1, player2)
        
        
    """---------------------------------------------------------- Overridden Methods ------------------------------------------------------"""
    
    def handle_click_down(self, row, col):
        """
        Method:
            Handles mouse click down events
        
        Params:
            row (int)
            col (int)
        """
        
        # Obtain piece at clicked square
        piece = self.board.get_piece(row, col)
        
        # If a piece is clicked and is the right colour
        if piece is not None and piece.get_colour() == self.board.get_colour():
            
            # Update display
            self.gui.draw_board()
            self.gui.draw_pieces(self.board)
            
            # Update variables
            self.selectedPiece = True
            self.selectedRow, self.selectedCol = row, col
            self.selectedMoves = self.arbiter.filter_moves(self.board, piece.get_moves(self.board), self.board.get_colour())
            self.gui.draw_moves(self.selectedMoves)
    
    
    def handle_click_up(self, row, col):
        """
        Method:
            Handles mouse click up events
        
        Params:
            row (int)
            col (int)
        """
        # If a piece isnt selected, ignore
        if self.selectedPiece is None:
            return
        
        # Find legal move locations
        moveToList = [move.get_move_to() for move in self.selectedMoves]
        
        # If legal move handle
        if (row, col) in moveToList:
            # Get move and handle
            move = self.selectedMoves[moveToList.index((row, col))]
            
            if move.get_flag() == PROMOTION:
                choice = self.handle_promotion()
                move.make_move(promotionChoice=choice)
            
            else:
                move.make_move()
                
            # Update display
            self.gui.draw_board()
            self.gui.draw_pieces(self.board)
            
            # Reset vars
            self.selectedPiece = None
            self.selectedRow, self.selectedCol = None, None
            self.selectedMoves = None
            
            return True
            
    
    def player_1_move(self):
        """
        Method:
            Handles player 1 move
        """
        
        for event in pg.event.get():
            return self.handle_event(event)


    def player_2_move(self):
        """
        Method:
            Handles player 2 move
        """
        
        for event in pg.event.get():
            return self.handle_event(event)