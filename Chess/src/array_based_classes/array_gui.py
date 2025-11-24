"""
Imports
"""
import pygame as pg
import math

try:
    from src.constants.constUI import *
    from src.base_classes.gui import GUI
except:
    from constants.constUI import *
    from base_classes.gui import GUI


"""
Classes
"""
class ArrayGUI(GUI):
    
    """ ---------------------------------------------------------- Super Methods ----------------------------------------------------"""
    
    
    def __init__(self):
        super().__init__()
    
    
    """ ---------------------------------------------------------- Overriden Methods ----------------------------------------------------"""
    
    
    def draw_pieces(self, board):
        """
        Method:
            Draws pieces to the pygame window
            
        Params:
            board (Board)
        """                
        
        squareSize = math.floor(self.screen.get_size()[1]/8)

        for rowIDX, row in enumerate(board.get_board()):
            for colIDX, item in enumerate(row):
                
                if item != None:
                    topLeftx = colIDX * squareSize
                    topLefty = rowIDX * squareSize
                    
                    asset = self.assetDict[f"{item.get_colour()} {item.get_type()}"]
                    pieceWidth, pieceHeight = asset.get_size()
                    
                    centeredX = topLeftx + (squareSize - pieceWidth)/2
                    centeredY = topLefty + (squareSize - pieceHeight)/2
                    
                    # Draw piece to screen
                    self.screen.blit(asset, (centeredX, centeredY))
        
        pg.display.update()
        

    def draw_moves(self, moves):
        """
        Method:
            Draws provided moves to screen
            
        Params:
            moves (List[Move])
        """
        squareSize = math.floor(self.screen.get_size()[1]/8)
        
        for move in moves:
            transparentSurface = self.draw_transparent_rectangle(RED_30_PERCENT_ALPHA)
            x, y = move.get_move_to()[1]*squareSize, move.get_move_to()[0]*squareSize
            self.screen.blit(transparentSurface, (x, y))
        
        pg.display.update()