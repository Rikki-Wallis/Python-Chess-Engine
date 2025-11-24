"""
Imports
"""
import time
import pygame as pg

try:
    from src.constants.constPieces import *
    from src.constants.constColours import *
    from src.ui_elements.box import *
except:
    from constants.constPieces import *
    from constants.constColours import *
    from ui_elements.box import *


"""
Classes
"""
class Game:
    
    def __init__(self, gui, arbiter, board, player1, player2):
        self.gui = gui
        self.arbiter = arbiter
        self.board = board
        self.running = True
        self.selectedPiece = None
        self.player1 = player1
        self.player2 = player2
        self.inputBox = InputBox(self.gui.get_square_size()*8 + 50, 50, 140, 32, " ")

    """---------------------------------------------------------- Abstract Methods ----------------------------------------------------------"""
    
    
    def get_user_input(self):
        pass
    
    def handle_click_down(self, row, col):
        pass
    
    def handle_click_up(self, row, col):
        pass
    
    def player_1_move(self):
        pass
    
    def player_2_move(self):
        pass
    
    
    """---------------------------------------------------------- Helper Methods ----------------------------------------------------------"""
    
    
    def check_conditions(self):
        """
        Method:
            Checks the current game conditions
            (check, checkmate, stalemate)
        
        Params:
            arbiter (Arbiter)
        """ 
        
        if self.arbiter.is_in_checkmate(self.board):
            oColour = BLACK if self.board.get_colour() == WHITE else WHITE
            text = f"{oColour} CHECKMATED!"
        
        elif self.arbiter.is_in_stalemate(self.board):
            text = "STALEMATE!"
        
        elif self.arbiter.is_in_insufficient_material(self.board):
            text = "DRAW BY INSUFFICIENT MATERIAL!"
        
        elif self.arbiter.is_in_repetition(self.board):
            text = "DRAW BY REPETITION!"
            
        elif self.arbiter.is_in_fifty_move_rule(self.board):
            text = "DRAW BY 50-MOVE RULE!"
        
        else:
            return
        
        self.gui.draw_text(f'{text} Closing App', pg.Color('white'), self.gui.get_square_size()*8+50, self.gui.get_square_size()*8-40)
        time.sleep(10)
        self.running = False
        pg.quit()
        quit()
    
    
    def handle_event(self, event):
        """
        Method:
            Handles pygame events
        
        Params:
            event (pygame.event)
        """
        
        # Handle exiting game
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            self.running = False
            pg.quit()
            exit()

        # Handle mouse clicked down
        if event.type == pg.MOUSEBUTTONDOWN:
            # Get mouse location at current point
            x, y = pg.mouse.get_pos()
            squareSize = self.gui.get_square_size()
            row, col = y // squareSize, x // squareSize
            
            # Check if out of bounds
            if row < 0 or row > 7 or col < 0 or col > 7:
                return
            
            # Handle click down for given row and col
            self.handle_click_down(row, col)
        
        # Handle mouse released
        if event.type == pg.MOUSEBUTTONUP:
            
            # If nothing selected, ignore
            if self.selectedPiece is None:
                return
        
            # Get current mouse location
            x, y = pg.mouse.get_pos()
            squareSize = self.gui.get_square_size()
            row, col = y // squareSize, x // squareSize
            
            # Check if out of bounds
            if row < 0 or row > 7 or col < 0 or col > 7:
                return
            
            # Handle click release
            self.handle_click_up(row, col)


    def handle_promotion(self):
        """
        Method:
            Handles pawn promotion
        """
        # Initiate variables
        promoting = True
        
        # Configure input box
        self.inputBox.active = True
        self.inputBox.color = pg.Color('dodgerblue2')
        self.inputBox.text = ''
        self.inputBox.txt_surface = pg.font.SysFont("Arial", 30).render("", True, self.inputBox.color) 
        self.gui.draw_text("Promote to (Q, R, B, N): ", pg.Color('white'), self.gui.get_square_size()*8 + 50, 10)
        
        # Loop until valid input
        while promoting:
            
            # Update input box each frame
            self.inputBox.update()
            self.inputBox.draw(self.gui.screen)
            pg.display.flip()
            
            # Handle different events
            for event in pg.event.get():
                
                # Handle input box events
                self.inputBox.handle_event(event)
                
                # Check if a input has been entered
                if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                    
                    choice = self.inputBox.get_return_text().upper().strip()
                    
                    # Valid choice
                    if choice in ['Q', 'R', 'B', 'N']:
                        
                        pieces = {
                            'Q' : QUEEN,
                            'R' : ROOK,
                            'B' : BISHOP,
                            'N' : KNIGHT
                        }
                        
                        choice = pieces[choice]
                        
                        # Exit loop and reset input box
                        promoting = False
                        self.inputBox.active = False
                        self.inputBox.color = pg.Color('lightskyblue3')
                        self.inputBox.text = ''
                        self.inputBox.txt_surface = pg.font.SysFont("Arial", 30).render("", True, self.inputBox.color) 
                        
                        self.gui.clear_screen()
                        self.gui.draw_text(f'Press esc to quit', pg.Color('grey'), self.gui.get_square_size()*8+350, 10)
                        self.gui.draw_board()
                        self.gui.draw_pieces(self.board)
                        
                        return choice
            
                # Handle input box updates
                if event.type == pg.K_BACKSPACE:
                    self.inputBox.handle(event)
                    self.inputBox.draw(self.gui.screen)                        
    
    
    """---------------------------------------------------------- Main Game Loop ----------------------------------------------------------"""
    
    
    def play_game(self):
        """
        Method:
            Main game loop
        """
        self.gui.draw_board()
        self.gui.draw_pieces(self.board)
        self.gui.draw_text(f'Press esc to quit', pg.Color('grey'), self.gui.get_square_size()*8+350, 10)
        
        while self.running:
            
            moved = False
            
            if self.board.get_colour() == self.player1:
                moved = self.player_1_move()

            else:
                moved = self.player_2_move()
                
            if moved:
                self.check_conditions()
            
            
            

            