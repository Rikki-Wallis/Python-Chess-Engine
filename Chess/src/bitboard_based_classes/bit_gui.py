"""
Imports
"""
import pygame as pg

try:
    from src.base_classes.gui import GUI
    from src.constants.constUI import *
    from src.constants.constColours import *
    from src.constants.constFlags import *
    from src.constants.constPieces import *
except:
    from base_classes.gui import GUI
    from constants.constUI import *
    from constants.constColours import *
    from constants.constFlags import *
    from constants.constPieces import *
"""
Classes
"""
class BitGUI(GUI):
    
    """---------------------------------------------------------- Super Methods ----------------------------------------------------------"""
    
    
    def __init__(self):
        super().__init__()
    
    
    """---------------------------------------------------------- Changed Methods ----------------------------------------------------------"""
    
    
    def draw_pieces(self, bitboard):
        """
        Method:
            Draws pieces on the board (for bitboard implementation)
        
        Params:
            bitboard (BitBoard)
        """
        # Initiate variables
        pieceBitboards = bitboard.get_board()
        squareSize = self.get_square_size()
        rookPositions = bitboard.get_rook_pos()
        
        for pieceAttributes, bitboard_data in pieceBitboards.items():
            
            # Skip non important items
            if pieceAttributes == BLACK or pieceAttributes == WHITE:
                continue
            
            # Get piece type and colour
            pieceAttributes_split = pieceAttributes.split()
            type = pieceAttributes_split[1]
            colour = pieceAttributes_split[0]
            
            # Draw piece on board
            for index in range(64):
                if (bitboard_data >> index) & 1:
                    row = index // 8
                    col = index % 8
                    
                    asset = self.assetDict[f'{colour} {type}']
                    width, height = asset.get_size()
                    
                    leftx = col * squareSize
                    lefty = row * squareSize
                    
                    centeredX = leftx + (squareSize - width) / 2
                    centeredY = lefty + (squareSize - height) / 2
                    
                    self.screen.blit(asset, (centeredX, centeredY))
                    
        pg.display.update()
        
        
    def draw_moves(self, moves):
        """
        Method:
            Draws a highlight on squares to show possible moves (for bitboard implementation)
        
        Params:
            moves (list): List of Move objects
        """
        squareSize = self.get_square_size()
                
        for move in moves:
            # Create transparent tile
            tSurface = self.draw_transparent_rectangle(RED_30_PERCENT_ALPHA)
            
            # Calculate position
            moveTo = move.get_move_to()
            index = moveTo.bit_length() - 1
                        
            row = index // 8
            col = index % 8
                        
            leftx = col * squareSize
            lefty = row * squareSize
            
            # Draw the overlay
            self.screen.blit(tSurface, (leftx, lefty))
        
        pg.display.update()

