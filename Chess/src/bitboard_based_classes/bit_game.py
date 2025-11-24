"""
Imports
"""
import pygame as pg

try:
    from src.base_classes.game import Game
    from src.bitboard_based_classes.move_generation.move_generator import MoveGenerator
    from src.constants.constFlags import *
except:
    from base_classes.game import Game
    from bitboard_based_classes.move_generation.move_generator import MoveGenerator
    from constants.constFlags import *

"""
Classes
"""
class BitGame(Game):
    
    """ ---------------------------------------------------------- Constructor ----------------------------------------------------------"""
    
    
    def __init__(self, gui, arbiter, board, player1, player2):
        super().__init__(gui, arbiter, board, player1, player2)
        self.moveGen = MoveGenerator()
    
    
    """ ---------------------------------------------------------- Overridden Methods ------------------------------------------------------"""
    
    
    def handle_click_down(self, row, col):
        """
        Method:
            Handles mouse click down events
        
        Params:
            row (int)
            col (int)
        """
        # Fetch piece at square
        pieceAttributes = self.board.get_piece(row, col)

        # If a there is no piece at the square return early
        if pieceAttributes is None:
            return
        
        type, colour, mask = pieceAttributes

        # If a piece is clicked and is the right colour
        if colour == self.board.get_colour():
            # Update display
            self.gui.draw_board()
            self.gui.draw_pieces(self.board)
            
            # Update variables
            self.selectedPiece = True
            self.selectedType = type
            self.selectedColour = colour
            self.selectedMask = mask
            
            # Draw moves to screen
            moves = self.moveGen.get_moves(self.board, colour, type, mask)
            self.selectedMoves = self.arbiter.filter_moves(self.board, moves, colour)
            self.gui.draw_moves(self.selectedMoves)
    
    
    def handle_click_up(self, row, col):
        """
        Method:
            Handles mouse click up events
        
        Params:
            row (int)
            col (int)
        """
        # If piece is not selected, ignore
        if self.selectedPiece is None:
            return
        
        moveToMasks = [move.get_move_to() for move in self.selectedMoves]
        targetIndex = (row * 8) + col
        targetMask = 1 << targetIndex
        
        # If legal move handle
        if targetMask in moveToMasks:

            # Get move and handle
            move = self.selectedMoves[moveToMasks.index(targetMask)]
            
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
            self.selectedType = None
            self.selectedColour = None
            self.selectedMask = None
            
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