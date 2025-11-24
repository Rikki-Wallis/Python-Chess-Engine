"""
Imports
"""
import pygame as pg
import math

try:
    from src.constants.constPieces import *
    from src.constants.constColours import *
    from src.constants.constUI import *    
except:
    from constants.constPieces import *
    from constants.constColours import *
    from constants.constUI import *


"""
Classes
"""
class GUI:
    
    """ ---------------------------------------------------------- Constructor ----------------------------------------------------"""
    
    
    def __init__(self):
        """
        Method:
            Loads assets and initialises pygame window
        """
        # Importing Assests
        blackKing = pg.image.load('Chess\\assets\\Black King.png')
        blackQueen = pg.image.load('Chess\\assets\\Black Queen.png')
        blackBishop = pg.image.load('Chess\\assets\\Black Bishop.png')
        blackKnight = pg.image.load('Chess\\assets\\Black Knight.png')
        blackRook = pg.image.load('Chess\\assets\\Black Rook.png')
        blackPawn = pg.image.load('Chess\\assets\\Black Pawn.png')

        whiteKing = pg.image.load('Chess\\assets\\White King.png')
        whiteQueen = pg.image.load('Chess\\assets\\White Queen.png')
        whiteRook = pg.image.load('Chess\\assets\\White Rook.png')
        whiteBishop = pg.image.load('Chess\\assets\\White Bishop.png')
        whiteKnight = pg.image.load('Chess\\assets\\White Knight.png')
        whitePawn = pg.image.load('Chess\\assets\\White Pawn.png')
        
        self.bot_waiting_img = pg.image.load('Chess\\assets\\monkey cam.jpg')
        self.bot_thinking_img = pg.image.load('Chess\\assets\\Monkey thinking.jpg')
    
        # Creating a dictionary for all the assets
        self.assetDict = { 
                    f'{BLACK} {PAWN}' : blackPawn,
                    f'{BLACK} {ROOK}' : blackRook,
                    f'{BLACK} {KNIGHT}' : blackKnight,
                    f'{BLACK} {BISHOP}' : blackBishop,
                    f'{BLACK} {KING}' : blackKing,
                    f'{BLACK} {QUEEN}' : blackQueen,
                    f'{WHITE} {PAWN}' : whitePawn,
                    f'{WHITE} {ROOK}' : whiteRook,
                    f'{WHITE} {KNIGHT}' : whiteKnight,
                    f'{WHITE} {BISHOP}' : whiteBishop,
                    f'{WHITE} {KING}' : whiteKing,
                    f'{WHITE} {QUEEN}' : whiteQueen   
                    }
        
        # Initialise screen
        pg.init()
        self.font = pg.font.SysFont("Arial", 30)
        info = pg.display.Info()
        self.screenWidth, self.screenHeight = info.current_w, info.current_h
        self.screen = pg.display.set_mode((self.screenWidth, self.screenHeight))


    """ ---------------------------------------------------------- Abstract Methods ----------------------------------------------------------"""
    
    
    def draw_pieces(self, board):
        pass
    
    
    def draw_moves(self, moves):
        pass
    
    
    """ ---------------------------------------------------------- Helper Methods ----------------------------------------------------------"""
    
    
    def get_square_size(self):
        return math.floor(self.screen.get_size()[1]/8)
    
    
    def draw_board(self):
        """
        Method:
            Draws the chess board to the pygame window
        """
        
        squareSize = self.get_square_size()
        
        # Iterate over board checking if tile is even and pick colour based on result
        boardSize = 8
        for row in range(boardSize):
            for col in range(boardSize):
                colour = BIEGE if (row+col) % 2 == 0 else BROWN
                
                x = col * squareSize
                y = row * squareSize
                
                pg.draw.rect(self.screen, colour, (x, y, squareSize, squareSize))
        
        pg.display.update()
        
    
    def draw_transparent_rectangle(self, colour):
        """
        Method:
            returns a transparent rectangle
            
        Params:
            colour (tuple(int, int, int, int) )
        """
        squareSize = self.get_square_size()
        
        transparentSurface = pg.Surface((squareSize,squareSize), pg.SRCALPHA) 
        transparentSurface.fill(colour)
        
        return transparentSurface
    
    
    def draw_text(self, text, color, x, y):
        """
        Method:
            Draws text to the pygame window
            
        Params:
            text (str)
            color (tuple(int, int, int) )
            x (int)
            y (int)
        """
        textSurface = self.font.render(text, True, color)
        self.screen.blit(textSurface, (x, y))
        pg.display.update()
    
    
    def clear_screen(self):
        """
        Method:
            Clears the pygame window
        """
        self.screen.fill((0,0,0))
        pg.display.update()
    
    
    def clear_side(self):
        """
        Method:
            clears the side where 
            the chessboard isnt
        """
        
        squareSize = self.get_square_size()
        min_x = squareSize*8
        
        screen_width, screen_height = self.screen.get_size()
        
        # Calculate the rectangle covering the side area
        side_rect = (min_x, 0, screen_width - min_x, screen_height)
        
        # Fill it with black (or any background color)
        self.screen.fill((0, 0, 0), side_rect)
        
        pg.display.update(side_rect)
    
    
    def draw_thinking(self):
        """
        Method:
            Clears the side panel and shows the 'Live Bot Cam' text
            along with the bot thinking image at the bottom-right of the screen.
        """
        # Step 1: Clear the side
        self.clear_side()
        
        squareSize = self.get_square_size()
        min_x = squareSize * 8  # start of side panel
        screen_width, screen_height = self.screen.get_size()
        
        # Step 3: Draw the thinking monkey image at bottom-right of side panel
        img = self.bot_thinking_img
        
        # Scale the image (optional)
        img_width = squareSize * 2
        img_height = squareSize * 2
        img = pg.transform.scale(img, (img_width, img_height))
        
        img_x = screen_width - img_width - 10  # 10 px padding from right
        img_y = screen_height - img_height - 10  # 10 px padding from bottom
        
        text_x = img_x
        text_y = img_y - 30
        self.draw_text("Live Bot Cam", (255, 255, 255), text_x, text_y)
        
        self.screen.blit(img, (img_x, img_y))
        
        # Update only the side area for efficiency
        side_rect = (min_x, 0, screen_width - min_x, screen_height)
        pg.display.update(side_rect)


    def draw_waiting(self):
        """
        Method:
            Clears the side panel and shows the 'Live Bot Cam' text
            along with the bot waiting image (monkey not thinking) at the bottom-right.
        """
        # Step 1: Clear the side
        self.clear_side()
        
        squareSize = self.get_square_size()
        min_x = squareSize * 8  # start of side panel
        screen_width, screen_height = self.screen.get_size()
        
        # Step 3: Draw the waiting monkey image at bottom-right of side panel
        img = self.bot_waiting_img
        
        # Scale the image (optional)
        img_width = squareSize * 2
        img_height = squareSize * 2
        img = pg.transform.scale(img, (img_width, img_height))
        
        img_x = screen_width - img_width - 10  # 10 px padding from right
        img_y = screen_height - img_height - 10  # 10 px padding from bottom
        
        # Step 2: Draw text at top of side panel
        text_x = img_x
        text_y = img_y - 30
        self.draw_text("Live Bot Cam", (255, 255, 255), text_x, text_y)
        
        self.screen.blit(img, (img_x, img_y))
        
        # Update only the side area for efficiency
        side_rect = (min_x, 0, screen_width - min_x, screen_height)
        pg.display.update(side_rect)
        
    
    
    def draw_evaluation_bar(self, eval_score: float):
        """
        Draws a vertical evaluation bar next to the chessboard,
        centered at 0. Positive = White advantage (up), Negative = Black advantage (down),
        and blits the numeric evaluation above the bar.
        Bar is 20 pixels wide and padded from top and bottom.
        Does not interfere with side panel where bot images are drawn.
        
        Params:
            eval_score (float): engine evaluation
        """
        squareSize = self.get_square_size()
        min_x = squareSize * 8  # start of side panel
        screen_width, screen_height = self.screen.get_size()
        
        # Bar dimensions
        bar_width = 20  # skinnier bar
        vertical_padding = 50  # padding from top and bottom
        bar_x = min_x + 10  # padding from board
        bar_y = vertical_padding
        bar_height = squareSize * 8 - 2 * vertical_padding  # reduce height by padding
        
        # Clear previous bar area (just the bar strip)
        bar_rect = (bar_x, bar_y, bar_width, bar_height)
        self.screen.fill((50, 50, 50), bar_rect)  # dark grey background
        
        # Clamp evaluation
        max_eval = 10.0
        eval_score = max(-max_eval, min(max_eval, eval_score))
        
        # Compute bar pixels
        mid_y = bar_y + bar_height // 2
        half_height = bar_height // 2
        fill_height = int((abs(eval_score) / max_eval) * half_height)
        
        if eval_score > 0:
            # White advantage: draw upwards
            white_rect = (bar_x, mid_y - fill_height, bar_width, fill_height)
            pg.draw.rect(self.screen, (255, 255, 255), white_rect)
        elif eval_score < 0:
            # Black advantage: draw downwards
            black_rect = (bar_x, mid_y, bar_width, fill_height)
            pg.draw.rect(self.screen, (0, 0, 0), black_rect)
        
        # Draw border
        pg.draw.rect(self.screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Draw numeric evaluation above the bar
        eval_text = f"{eval_score:.2f}"
        text_x = bar_x
        text_y = bar_y - 30  # 30 pixels above top of bar
        self.draw_text(eval_text, (255, 255, 0), text_x, text_y)
        
        # Only update the bar strip, leaving the rest of the side panel untouched
        pg.display.update(bar_rect)


