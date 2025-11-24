"""
Imports
"""
try:
    from src.base_classes.move import Move
    from src.constants.constFilesAndRanks import *
    from src.constants.constCastlingBoards import *
    from src.constants.constColours import *
    from src.constants.constPieces import *
    from src.constants.constFlags import *    
except:
    from base_classes.move import Move
    from constants.constFilesAndRanks import *
    from constants.constCastlingBoards import *
    from constants.constColours import *
    from constants.constPieces import *
    from constants.constFlags import *    


"""
Classes
"""
class BitMove(Move):
    
    def __init__(self, board, moveFrom, moveTo, flag=None):
        super().__init__(board, moveFrom, moveTo, flag)
    
    """ ------------------------------------ Overridden Methods ----------------------------------- """
    
    
    def additional_settup(self):
        """
        Method:
            Additional settup for class
        """
        # Initiate vars
        self.isCapture = False
        self.isCheck = False
        findTarget = False
        foundTarget = False
        foundHome = False
        
        # Get target piece
        enemyColour = WHITE if self.board.get_colour() == BLACK else BLACK
        enemyOccupancy = self.board.get_board()[f'{enemyColour}']
        
        # If there is a target piece handle it
        if enemyOccupancy & self.moveTo:
            findTarget = True
        
        # Iterate over all bitboards and find the home and possible target piece
        for pieceAttributes, bitstr in self.board.get_board().items():
            
            # Ignore occupancy boards
            if pieceAttributes == BLACK or pieceAttributes == WHITE:
                continue
            
            # Found the piece, set vars and break
            if findTarget and (self.moveTo & bitstr):
                pieceAttributes = pieceAttributes.split(' ')
                self.targetType = pieceAttributes[1]
                self.targetColour = pieceAttributes[0]
                
                if self.targetType == KING:
                    self.isCheck = True
                else:
                    self.isCapture = True
                
                foundTarget = True
            
            # Find piece and set attributes
            if not foundHome and (self.moveFrom & bitstr):
                pieceAttributes = pieceAttributes.split(' ')
                self.pieceType = pieceAttributes[1]
                self.pieceColour = pieceAttributes[0]
                foundHome = True
            
            # If necessary pieces found break early
            if foundHome and foundTarget or foundHome and not findTarget:
                break
                
    
    def handle_remove_pieces(self, action):
        """
        Method:
            Handles removing pieces from the board
        
        Params:
            action (ENUM)
        """
        # Don't make move if it is a "checking" move
        if self.isCheck:
            return
        
        # Initiate clear bitstring
        clearHome = self.board.get_board()[f'{self.pieceColour} {self.pieceType}'] & ~self.moveFrom
        clearHomeTarget = self.board.get_board()[f'{self.pieceColour} {self.pieceType}'] & ~self.moveTo
        if self.isCapture:
            clearTarget = self.board.get_board()[f'{self.targetColour} {self.targetType}'] & ~self.moveTo
        else:
            clearTarget = ~self.moveTo
            
        if action == MAKE:
            # Remove home piece from square
            self.board.get_board()[f'{self.pieceColour} {self.pieceType}'] &= clearHome
            
            # If there is a target piece remove it from square
            if self.isCapture:
                self.board.get_board()[f'{self.targetColour} {self.targetType}'] &= clearTarget

        else:
            # Remove home piece from target square
            self.board.get_board()[f'{self.pieceColour} {self.pieceType}'] &= clearHomeTarget
    
    
    def handle_placing_piece(self, action):
        """
        Method:
            Handles placing the pieces onto the board
        
        Params:
            action (ENUM)
        """
        if self.isCheck:
            return
        
        if action == MAKE:
            # Place piece at target square
            if not self.flag == PROMOTION:
                self.board.get_board()[f'{self.pieceColour} {self.pieceType}'] |= self.moveTo
        
        else:
            # Place piece at home square
            self.board.get_board()[f'{self.pieceColour} {self.pieceType}'] |= self.moveFrom
            
            # If it was a capture place target piece back
            if self.isCapture:
                self.board.get_board()[f'{self.targetColour} {self.targetType}'] |= self.moveTo
    
    
    def make_update(self, action):
        """
        Method:
            Updates the board state after a move is made or undone
        """
        self.board.flip_colour()
        self.board.update_occupancy()
        
        # Hash position
        zobristKey = self.board.get_current_zobrist()
        zobrist = self.board.get_zobrist()

        zobristKey ^= zobrist.pieces[self.pieceType][self.moveFrom.bit_length()-1]
        if self.isCapture:
            zobristKey ^= zobrist.pieces[self.targetType][self.moveTo.bit_length()-1]
        
        zobristKey ^= zobrist.pieces[self.pieceType][self.moveTo.bit_length()-1]
        zobristKey ^= zobrist.sideToMove
        
        self.board.set_current_zobrist(zobristKey)

        if action == MAKE:
            
            self.board.increment_position_hash(zobristKey)
            
            # Handle captured rook BEFORE moving our rook
            self.capturedRookSide = None
            if self.isCapture and self.targetType == ROOK:
                for key, bitStr in self.board.get_rook_pos().items():
                    if bitStr & self.moveTo:
                        keySplit = key.split(' ')
                        # Only process if it's the opponent's rook
                        if keySplit[0] == self.targetColour:
                            self.capturedRookSide = key
                            self.board.increment_rook_moved(keySplit[0], keySplit[1])
                            break
            
            # Increment times moved of home piece
            if self.pieceType == ROOK:
                for pieceAttributes, bitStr in self.board.get_rook_pos().items():
                    if bitStr & self.moveFrom:
                        self.board.get_rook_pos()[pieceAttributes] = self.moveTo
                        pieceAttributes = pieceAttributes.split(' ')
                        self.board.increment_rook_moved(pieceAttributes[0], pieceAttributes[1])
            
            elif self.pieceType == KING:
                self.board.increment_king_moved(self.pieceColour)
                        
            
            # Update the last move stack
            self.board.push_move(self)
            
            # Increment half-move clock if necessary
            if self.pieceType == PAWN or self.isCapture:
                self.board.reset_half_move_clock()
                self.previousHalfMoveClock = self.board.get_half_move_clock()
            else:
                self.board.increment_half_move_clock()
                self.previousHalfMoveClock = None
                
        else:
            
            self.board.decrement_position_hash(zobristKey)
            
            # Remove move from last move stack
            self.board.pop_last_move()
            
            # Decrement times moved of home piece
            if self.pieceType == ROOK:
                for pieceAttributes, bitStr in self.board.get_rook_pos().items():
                    if bitStr & self.moveTo:
                        self.board.get_rook_pos()[pieceAttributes] = self.moveFrom
                        pieceAttributes = pieceAttributes.split(' ')
                        self.board.decrement_rook_moved(pieceAttributes[0], pieceAttributes[1])
            
            elif self.pieceType == KING:
                self.board.decrement_king_moved(self.pieceColour)
            
            # Handle undoing captured rook
            if hasattr(self, 'capturedRookSide') and self.capturedRookSide is not None:
                keySplit = self.capturedRookSide.split(' ')
                self.board.decrement_rook_moved(keySplit[0], keySplit[1])

            # Decrement half-move clock if necessary
            if self.previousHalfMoveClock is not None:
                self.board.set_half_move_clock(self.previousHalfMoveClock)
                self.previousHalfMoveClock = None
            else:
                self.board.decrement_half_move_clock()
    
    def handle_short_castle(self, action):
        """
        Method:
            Handles the moving pieces for short castling
            
        Params:
            action (ENUM)
        """
        if self.pieceColour == WHITE:
            curIDX = 7
            newIDX = 5
        else:
            curIDX = 63
            newIDX = 61
        
        rookIDX = (1 << curIDX)
        newRookIDX = (1 << newIDX)
        
        if action == MAKE:
            # Remove rook from square
            self.board.get_board()[f'{self.pieceColour} {ROOK}'] &= ~rookIDX
            self.board.get_rook_pos()[f'{self.pieceColour} {SHORT}'] &= ~rookIDX
            # Add rook to new square 
            self.board.get_board()[f'{self.pieceColour} {ROOK}'] |= newRookIDX
            self.board.get_rook_pos()[f'{self.pieceColour} {SHORT}'] |= newRookIDX
            # Increment times the rook has moved
            self.board.increment_rook_moved(self.pieceColour, SHORT)
        
        else:
            # Remove rook from square
            self.board.get_board()[f'{self.pieceColour} {ROOK}'] &= ~newRookIDX
            self.board.get_rook_pos()[f'{self.pieceColour} {SHORT}'] &= ~newRookIDX
            # Add rook to new square 
            self.board.get_board()[f'{self.pieceColour} {ROOK}'] |= rookIDX
            self.board.get_rook_pos()[f'{self.pieceColour} {SHORT}'] |= rookIDX
            # Decrement times the rook has moved
            self.board.decrement_rook_moved(self.pieceColour, SHORT)
    
    
    def handle_long_castle(self, action):
        """
        Method:
            Handles the moving pieces for long castling
            
        Params:
            action (ENUM)
        """
        if self.pieceColour == WHITE:
            rookIDX = 0
            newIDX = 3
        else:
            rookIDX = 56
            newIDX = 59
        
        rookIDX = (1 << rookIDX)
        newRookIDX = (1 << newIDX)
        
        if action == MAKE:
            # Remove rook from square
            self.board.get_board()[f'{self.pieceColour} {ROOK}'] &= ~rookIDX
            self.board.get_rook_pos()[f'{self.pieceColour} {LONG}'] &= ~rookIDX
            # Add rook to new square 
            self.board.get_board()[f'{self.pieceColour} {ROOK}'] |= newRookIDX
            self.board.get_rook_pos()[f'{self.pieceColour} {LONG}'] |= newRookIDX
            # Increment times the rook has moved
            self.board.increment_rook_moved(self.pieceColour, LONG)
        
        else:
            # Remove rook from square
            self.board.get_board()[f'{self.pieceColour} {ROOK}'] &= ~newRookIDX
            self.board.get_rook_pos()[f'{self.pieceColour} {LONG}'] &= ~newRookIDX
            # Add rook to new square 
            self.board.get_board()[f'{self.pieceColour} {ROOK}'] |= rookIDX
            self.board.get_rook_pos()[f'{self.pieceColour} {LONG}'] |= rookIDX
            # Decrement times the rook has moved
            self.board.decrement_rook_moved(self.pieceColour, LONG)
    
    
    def handle_enpassant(self, action):
        """
        Method:
            Handles removing and placing the captured pawn in
            the enpassant move
            
        Params:
            action (ENUM)
        """
        
        if self.pieceColour == WHITE:
            targetMask = self.moveTo >> 8
            oColour = BLACK
        else:
            targetMask = self.moveTo << 8
            oColour = WHITE
        
        if action == MAKE:
            self.board.get_board()[f'{oColour} {PAWN}'] &= ~targetMask
        
        else:
            self.board.get_board()[f'{oColour} {PAWN}'] |= targetMask
    
    
    def handle_promotion(self, action, promotionChoice=None):
        """
        Method:
            Handles removing and placing pieces for promotion
        
        Params:
            action (ENUM)
            promotionChoice (ENUM)
        """
        
        if action == MAKE:
            self.board.get_board()[f'{self.pieceColour} {promotionChoice}'] |= self.moveTo
            self.promotionChoice = promotionChoice
        
        else:
            self.board.get_board()[f'{self.pieceColour} {self.promotionChoice}'] &= ~self.moveTo
    
    
    def bitboard_to_visual(self, bitboard):
        """
        Converts a bitboard to a visual 8x8 grid representation.
        
        Args:
            bitboard: Integer representing a bitboard where each bit represents a square.
                    Bit 0 = a1, Bit 7 = h1, Bit 56 = a8, Bit 63 = h8
            
        Returns:
            String with visual representation of the bitboard.
            'x' marks set bits (occupied squares), '.' marks empty squares.
        
        Example:
            Input: 0x10 (bit 4 set, representing e1)
            Output:
            ........
            ........
            ........
            ........
            ........
            ........
            ........
            ....x...
        """
        if bitboard == 0:
            return "........\n" * 8
        
        lines = []
        
        # Iterate from rank 8 to rank 1 (top to bottom on display)
        for rank in range(7, -1, -1):
            line = ""
            # Iterate from file a to h (left to right)
            for file in range(8):
                # Calculate bit position: rank * 8 + file
                bit_position = rank * 8 + file
                
                # Check if this bit is set in the bitboard
                if bitboard & (1 << bit_position):
                    line += "x"
                else:
                    line += "."
            
            lines.append(line)
        
        return "\n".join(lines)
    
    def get_move_notation(self):
        if self.moveFrom & RANK1:
            fromRank = "1"
        elif self.moveFrom & RANK2:
            fromRank = "2"
        elif self.moveFrom & RANK3:
            fromRank = "3"
        elif self.moveFrom & RANK4:
            fromRank = "4"
        elif self.moveFrom & RANK5:
            fromRank = "5"
        elif self.moveFrom & RANK6:
            fromRank = "6"
        elif self.moveFrom & RANK7:
            fromRank = "7"
        elif self.moveFrom & RANK8:
            fromRank = "8"
        else:
            fromRank = "error"
            
        if self.moveFrom & A_FILE:
            fromFile = "a"
        elif self.moveFrom & B_FILE:
            fromFile = "b"
        elif self.moveFrom & C_FILE:
            fromFile = "c"
        elif self.moveFrom & D_FILE:
            fromFile = "d"
        elif self.moveFrom & E_FILE:
            fromFile = "e"
        elif self.moveFrom & F_FILE:
            fromFile = "f"
        elif self.moveFrom & G_FILE:
            fromFile = "g"
        elif self.moveFrom & H_FILE:
            fromFile = "h"
        else:
            fromFile = "error"
        
        if self.moveTo & RANK1:
            toRank = "1"
        elif self.moveTo & RANK2:
            toRank = "2"
        elif self.moveTo & RANK3:
            toRank = "3"
        elif self.moveTo & RANK4:
            toRank = "4"
        elif self.moveTo & RANK5:
            toRank = "5"
        elif self.moveTo & RANK6:
            toRank = "6"
        elif self.moveTo & RANK7:
            toRank = "7"
        elif self.moveTo & RANK8:
            toRank = "8"
        else:
            toRank = "error"
            
        if self.moveTo & A_FILE:
            toFile = "a"
        elif self.moveTo & B_FILE:
            toFile = "b"
        elif self.moveTo & C_FILE:
            toFile = "c"
        elif self.moveTo & D_FILE:
            toFile = "d"
        elif self.moveTo & E_FILE:
            toFile = "e"
        elif self.moveTo & F_FILE:
            toFile = "f"
        elif self.moveTo & G_FILE:
            toFile = "g"
        elif self.moveTo & H_FILE:
            toFile = "h"
        else:
            toFile = "error"
        
        return f"{fromFile}{fromRank}{toFile}{toRank}"
    
    def get_proper_notation(self):
        """
        Returns proper chess notation for the move (e.g., Nf3, Bxe5, e8=Q, O-O, Qd1+)
        This matches standard chess notation used in test suites.
        
        Returns:
            str: Proper chess notation for the move
        """
        # Handle castling
        if self.flag == SHORT_CASTLE:
            return "O-O"
        elif self.flag == LONG_CASTLE:
            return "O-O-O"
        
        # Build the notation string
        notation = ""
        
        # Piece prefix (empty for pawns)
        piece_symbols = {
            KING: 'K',
            QUEEN: 'Q',
            ROOK: 'R',
            BISHOP: 'B',
            KNIGHT: 'N',
            PAWN: ''
        }
        notation += piece_symbols.get(self.pieceType, '')
        
        # For pawns capturing, add the file they're moving from
        if self.pieceType == PAWN and self.isCapture:
            from_file = self._get_file(self.moveFrom)
            notation += from_file
        
        # Add 'x' for captures
        if self.isCapture:
            notation += 'x'
        
        # Destination square
        to_file = self._get_file(self.moveTo)
        to_rank = self._get_rank(self.moveTo)
        notation += to_file + to_rank
        
        # Promotion
        if self.flag == PROMOTION and hasattr(self, 'promotionChoice'):
            promotion_symbols = {
                QUEEN: 'Q',
                ROOK: 'R',
                BISHOP: 'B',
                KNIGHT: 'N'
            }
            notation += '=' + promotion_symbols.get(self.promotionChoice, 'Q')
        
        # Check or checkmate (optional - would need to test resulting position)
        # For now, we can add '+' if we know it's check
        # notation += '+' or '#'
        
        return notation

    def _get_file(self, bitboard):
        """Helper to get file letter from bitboard"""
        if bitboard & A_FILE:
            return "a"
        elif bitboard & B_FILE:
            return "b"
        elif bitboard & C_FILE:
            return "c"
        elif bitboard & D_FILE:
            return "d"
        elif bitboard & E_FILE:
            return "e"
        elif bitboard & F_FILE:
            return "f"
        elif bitboard & G_FILE:
            return "g"
        elif bitboard & H_FILE:
            return "h"
        return ""

    def _get_rank(self, bitboard):
        """Helper to get rank number from bitboard"""
        if bitboard & RANK1:
            return "1"
        elif bitboard & RANK2:
            return "2"
        elif bitboard & RANK3:
            return "3"
        elif bitboard & RANK4:
            return "4"
        elif bitboard & RANK5:
            return "5"
        elif bitboard & RANK6:
            return "6"
        elif bitboard & RANK7:
            return "7"
        elif bitboard & RANK8:
            return "8"
        return ""

    
    def __str__(self):
        """
        Returns a formatted string representation of the move with visual bitboards.
        """
        
        # Build the output
        piece = f'{self.pieceColour} {self.pieceType}'
        
        # Add capture/check info
        flag_str = ""
        if self.isCheck:
            flag_str = " (CHECK - illegal!)"
        elif self.isCapture:
            flag_str = f" (captures {self.targetColour} {self.targetType})"
        elif self.flag:
            if 'PROMOTION' in str(self.flag):
                flag_str = " (promotion)"
            elif 'CASTLE' in str(self.flag):
                flag_str = " (castle)"
            elif 'EN_PASSANT' in str(self.flag):
                flag_str = " (en passant)"
        
        result = f"\n{piece:12}{flag_str}\n"
        result += "FROM:              TO:\n"
        
        from_visual = self.bitboard_to_visual(self.moveFrom)
        to_visual = self.bitboard_to_visual(self.moveTo)
        
        from_lines = from_visual.split('\n')
        to_lines = to_visual.split('\n')
        
        for from_line, to_line in zip(from_lines, to_lines):
            result += f"{from_line}        {to_line}\n"
        
        return result