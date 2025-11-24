"""
Imports
"""
try:
    from src.constants.constPieces import *
    from src.constants.constFlags import *
    from src.constants.constColours import *
    from src.base_classes.move import Move
except:
    from constants.constPieces import *
    from constants.constFlags import *
    from constants.constColours import *
    from base_classes.move import Move

"""
Classes
"""
class ArrayMove(Move):
    
    
    def __init__(self, board, moveFrom, moveTo, flag=None):
        super().__init__(board, moveFrom, moveTo, flag)
    
    
    """ ------------------------------------ Overridden Methods ----------------------------------- """
    
    
    def additional_settup(self):
        """
        Method:
            Additional settup for class
        """
        # Set home and target piece
        self.homePiece = self.board.get_piece(self.moveFrom[0], self.moveFrom[1])
        self.targetPiece = self.board.get_piece(self.moveTo[0], self.moveTo[1])
        
        # Add necessary flags
        self.isCheck = False
        self.isCapture = False
        
        if self.targetPiece is not None and self.targetPiece.get_type() == KING:
            self.isCheck = True
        
        elif self.targetPiece is not None:
            self.isCapture = True
        
    
    
    def handle_remove_pieces(self, action):
        """
        Method:
            Handles removing pieces from the board
            
        Params:
            action (ENUM)
        """
        if action == MAKE:
            # Fetch relevant squares
            fromRow, fromCol = self.moveFrom
            toRow, toCol = self.moveTo
            
            # Remove from squares
            self.board.remove_piece(fromRow, fromCol)
            self.board.remove_piece(toRow, toCol)
        
        else:
            # Fetch relevant squares
            toRow, toCol = self.moveTo
            # Remove piece from square
            self.board.remove_piece(toRow, toCol)
        
    
    def handle_short_castle(self, action):
        """
        Method:
            Handles the moving pieces for short castling
        
        Params:
            action (ENUM)
        """
        # Initiate vars
        fromRow, fromCol = self.moveFrom
        toRow, toCol = self.moveTo
        
        if action == MAKE:
            # Place rook in correct position
            rook = self.board.remove_piece(fromRow, 7)
            self.board.add_piece(rook, fromRow, 5)
            rook.increment_times_moved()
        
        else:
            # Place rook back in original position
            rook = self.board.remove_piece(fromRow, 5)
            self.board.add_piece(rook, fromRow, 7)
            rook.decrement_times_moved()
    
    
    def handle_long_castle(self, action):
        """
        Method:
            Handles the moving pieces for long castling
        
        Params:
            action (ENUM)
        """
        # Initiate vars
        fromRow, fromCol = self.moveFrom
        toRow, toCol = self.moveTo
        
        if action == MAKE:
            rook = self.board.remove_piece(fromRow, 0)
            self.board.add_piece(rook, fromRow, 3)
            rook.increment_times_moved()
        
        else:
            rook = self.board.remove_piece(fromRow, 3)
            self.board.add_piece(rook, fromRow, 0)
            rook.decrement_times_moved()
    
    
    def handle_enpassant(self, action):
        """
        Method:
            Handles the moving pieces for enpassant
        
        Params:
            action (ENUM)
        """
        # Initiate vars
        fromRow, fromCol = self.moveFrom
        toRow, toCol = self.moveTo
        
        if action == MAKE:
            # Remove target pawn
            self.targetPiece = self.board.remove_piece(fromRow, toCol)
        
        else:
            # Place target pawn back
            direction = 1 if self.homePiece.get_colour() == WHITE else -1
            targetPieceRow = toRow + direction
            self.board.add_piece(self.targetPiece, targetPieceRow, toCol)
        
        
    def handle_promotion(self, action, promotionChoice=None):
        """
        Method:
            Handles the moving pieces for promotion
        
        Params:
            action (ENUM)
            promotionChoice (str|None)
        """
        # Initiate vars
        fromRow, fromCol = self.moveFrom
        toRow, toCol = self.moveTo
        
        if action == MAKE:
            try:
                from src.array_based_classes.pieces.queen import Queen
                from src.array_based_classes.pieces.rook import Rook
                from src.array_based_classes.pieces.bishop import Bishop
                from src.array_based_classes.pieces.knight import Knight
                from src.array_based_classes.pieces.pawn import Pawn
            except:
                from array_based_classes.pieces.queen import Queen
                from array_based_classes.pieces.rook import Rook
                from array_based_classes.pieces.bishop import Bishop
                from array_based_classes.pieces.knight import Knight
                from array_based_classes.pieces.pawn import Pawn
                
            pieces = {
                'Q' : Queen(QUEEN, self.homePiece.get_colour()),
                'R' : Rook(ROOK, self.homePiece.get_colour()),
                'B' : Bishop(BISHOP, self.homePiece.get_colour()),
                'N' : Knight(KNIGHT, self.homePiece.get_colour()),
                'P' : Pawn(PAWN, self.homePiece.get_colour())
            }
            
            piece = pieces[promotionChoice]
                
            self.board.add_piece(piece, toRow, toCol)
            
            
    def handle_placing_piece(self, action):
        """
        Method:
            Handles placing pieces on the board
        
        Params:
            action (ENUM)
        """
        # Initiate vars
        fromRow, fromCol = self.moveFrom
        toRow, toCol = self.moveTo
        
        if action == MAKE:
            # If it's a promotion, the piece has already been placed
            if self.flag != PROMOTION:
                # Place home piece to target square
                self.board.add_piece(self.homePiece, toRow, toCol)
        
        else:
            # Add home piece back to home square
            self.board.add_piece(self.homePiece, fromRow, fromCol)
            self.homePiece.decrement_times_moved()
            
            # Handle placement of enpassant piece differenty than regular pieces
            if self.flag != ENPASSANT:
                self.board.add_piece(self.targetPiece, toRow, toCol)

                
    def make_update(self, action):
        """
        Method:
            Handles updating the board state after a move
        
        Params:
            action (ENUM)
        """
        # Change colour
        self.board.flip_colour()
        
        if action == MAKE:
            # Increment times moved of home piece
            self.homePiece.increment_times_moved()
            
            # Deactivate piece if needed
            if self.isCapture:
                self.targetPiece.set_active(False)

            # Update the last move stack
            self.board.push_move(self)
            
            # Add position to viewed positions hashmap
            self.board.increment_position_hash()
            
            # Increment half-move clock if necessary
            if self.homePiece.get_type() == PAWN or self.isCapture:
                
                self.board.reset_half_move_clock()
                # Keep track of previous half move clock
                self.previousHalfMoveClock = self.board.get_half_move_clock()
                
            else:
                self.board.increment_half_move_clock()
                self.previousHalfMoveClock = None
        
        else:
            # Remove move from last move stack
            self.board.pop_last_move()
            
            # active piece if needed
            if self.isCapture:
                self.targetPiece.set_active(True)
            
            # Decrement position from viewed positions hashmap
            self.board.decrement_position_hash()
            
            # Decrement half-move clock if necessary
            if self.previousHalfMoveClock is not None:
                self.board.set_half_move_clock(self.previousHalfMoveClock)
                self.previousHalfMoveClock = None
            
            else:
                self.board.decrement_half_move_clock()


            