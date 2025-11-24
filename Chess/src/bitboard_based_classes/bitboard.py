"""
Imports
"""
try:
    from src.base_classes.board import Board
    from src.bitboard_based_classes.precomputation.zobrist import Zobrist
    from src.constants.constPieces import *
    from src.constants.constColours import *
    from src.constants.constFlags import *
except:
    from base_classes.board import Board
    from bitboard_based_classes.precomputation.zobrist import Zobrist
    from constants.constPieces import *
    from constants.constColours import *
    from constants.constFlags import *

"""
Classes
"""
class BitBoard(Board):
    
    """ ------------------------------------------------- Constructer ----------------------------------------------------"""
    
    
    def __init__(self):
        super().__init__()
    
    
    """ -------------------------------------------- Overridden Methods ------------------------------------------------------"""
    
    
    def additionalSettup(self):
        """
        Method:
            Any additional settup for the board
        """
        
        # Bitboards for each piece
        self.wPawns =   0b0000000000000000000000000000000000000000000000001111111100000000  
        self.wRooks =   0b0000000000000000000000000000000000000000000000000000000010000001  
        self.wKnights = 0b0000000000000000000000000000000000000000000000000000000001000010  
        self.wBishops = 0b0000000000000000000000000000000000000000000000000000000000100100  
        self.wQueen =   0b0000000000000000000000000000000000000000000000000000000000001000   
        self.wKing =    0b0000000000000000000000000000000000000000000000000000000000010000  

        self.bPawns =   0b0000000011111111000000000000000000000000000000000000000000000000 
        self.bRooks =   0b1000000100000000000000000000000000000000000000000000000000000000  
        self.bKnights = 0b0100001000000000000000000000000000000000000000000000000000000000  
        self.bBishops = 0b0010010000000000000000000000000000000000000000000000000000000000  
        self.bQueen =   0b0000100000000000000000000000000000000000000000000000000000000000  
        self.bKing =    0b0001000000000000000000000000000000000000000000000000000000000000  
            
        self.board = {
            (f'{WHITE} {PAWN}') : self.wPawns,
            (f'{WHITE} {KNIGHT}') : self.wKnights,
            (f'{WHITE} {ROOK}') : self.wRooks,
            (f'{WHITE} {BISHOP}') : self.wBishops,
            (f'{WHITE} {QUEEN}') : self.wQueen,
            (f'{WHITE} {KING}') : self.wKing,
            (f'{BLACK} {PAWN}') : self.bPawns,
            (f'{BLACK} {KNIGHT}') : self.bKnights,
            (f'{BLACK} {ROOK}') : self.bRooks,
            (f'{BLACK} {BISHOP}') : self.bBishops,
            (f'{BLACK} {QUEEN}') : self.bQueen,
            (f'{BLACK} {KING}') : self.bKing,
            (f'{BLACK}') : self.bPawns | self.bKnights | self.bRooks | self.bBishops | self.bQueen | self.bKing,
            (f'{WHITE}') : self.wPawns | self.wKnights | self.wRooks | self.wBishops | self.wQueen | self.wKing
        }
        
        self.wShortRook =  0b0000000000000000000000000000000000000000000000000000000010000000 
        self.wLongRook =   0b0000000000000000000000000000000000000000000000000000000000000001
        self.bShortRook =  0b1000000000000000000000000000000000000000000000000000000000000000
        self.bLongRook =   0b0000000100000000000000000000000000000000000000000000000000000000
        self.rooks = {
            f'{WHITE} {SHORT}' : self.wShortRook,
            f'{WHITE} {LONG}' : self.wLongRook,
            f'{BLACK} {SHORT}' : self.bShortRook,
            f'{BLACK} {LONG}' : self.bLongRook
        }
        
        # Move flags
        self.bKingMoved = 0
        self.wKingMoved = 0
        self.bShortRookMoved = 0
        self.bLongRookMoved = 0
        self.wShortRookMoved = 0
        self.wLongRookMoved = 0
        
        # Hash Helper
        self.pieceChar = {
            (f'{WHITE} {PAWN}') : 'P',
            (f'{WHITE} {KNIGHT}') : 'N',
            (f'{WHITE} {ROOK}') : 'R',
            (f'{WHITE} {BISHOP}') : 'B',
            (f'{WHITE} {QUEEN}') : 'Q',
            (f'{WHITE} {KING}') : 'K',
            (f'{BLACK} {PAWN}') : 'p',
            (f'{BLACK} {KNIGHT}') : 'n',
            (f'{BLACK} {ROOK}') : 'r',
            (f'{BLACK} {BISHOP}') : 'b',
            (f'{BLACK} {QUEEN}') : 'q',
            (f'{BLACK} {KING}') : 'k',
        }
        
        # Add zobrist
        self.zobrist = Zobrist()
        self.currentZobristKey = self.zobrist.calculate_zobrist_key(self)
        self.positionHash[self.currentZobristKey] = 1


    def get_piece(self, row, col):
        """
        Method:
            Returns the piece at a given position
        
        Params:
            row (int) - the row of the piece
            col (int) - the column of the piece
        """
        # Get index
        index = (row * 8) + col 
        
        # Find piece at given index
        for pieceAttributes, bitboard in self.board.items():
            
            # Ignore non important items
            if pieceAttributes == BLACK or pieceAttributes == WHITE:
                continue
            
            # Create bit mask and check if a piece exists there
            bitstring = 1 << index

            if bitstring & bitboard:
                # Fetch attributes
                pieceAttributes = pieceAttributes.split()
                type = pieceAttributes[1]
                colour = pieceAttributes[0]
                
                return (type, colour, bitstring)
        
        return None
    

    def hash_position(self):
        """
        Method:
            Returns a string hash of the current board position
        """
        
        

    """ -------------------------------------------------------------- Helper Methods -------------------------------------------------------------- """
    
    
    def get_occupied_squares(self):
        """
        Method:
            Returns a bitboard representing all occupied squares on the board.
        """
        return self.board[f'{WHITE}'] | self.board[f'{BLACK}']
    
    
    def update_occupancy(self):
        """
        Method:
            Updates the occupancy bitboards for both colours.
        """
        whiteOccupancy = 0
        blackOccupancy = 0
        
        # Iterate over all pieces and update occupancy
        for pieceAttributes, bitstr in self.board.items():
            # Ignore occupancy masks
            if pieceAttributes == BLACK or pieceAttributes == WHITE:
                continue
            
            if pieceAttributes.startswith(WHITE):
                whiteOccupancy |= bitstr
            else:
                blackOccupancy |= bitstr
        
        self.board[f'{BLACK}'] = blackOccupancy
        self.board[f'{WHITE}'] = whiteOccupancy

    
    def get_king_moved(self, colour):
        """
        Method:
            Returns whether the king has moved for the given colour
            
        Params:
            colour (str) - the colour of the king (WHITE or BLACK)
        """
        if colour == WHITE:
            return self.wKingMoved
        else:
            return self.bKingMoved
    
    
    def get_rook_moved(self, colour, side):
        """
        Method:
            Returns whether the rook has moved for the given colour and side
            
        Params:
            colour (str) - the colour of the rook (WHITE or BLACK)
            side (str) - the side of the rook (SHORT or LONG)
        """
        if colour == WHITE and side == SHORT:
            return self.wShortRookMoved
        elif colour == WHITE and side == LONG:
            return self.wLongRookMoved 
        elif colour == BLACK and side == SHORT:
            return self.bShortRookMoved
        else:
            return self.bLongRookMoved
    
    
    def increment_king_moved(self, colour):
        """
        Method:
            Increments the king moved flag for the given colour
            
        Params:
            colour (str) - the colour of the king (WHITE or BLACK)
        """
        if colour == WHITE:
            self.wKingMoved += 1
        else:
            self.bKingMoved += 1
    
    
    def decrement_king_moved(self, colour):
        """
        Method:
            Decrements the king moved flag for the given colour
        
        Params:
            colour (str) - the colour of the king (WHITE or BLACK)
        """
        if colour == WHITE:
            self.wKingMoved -= 1
        else:
            self.bKingMoved -= 1
    
    
    def increment_rook_moved(self, colour, side):
        """
        Method:
            Increments the rook moved flag for the given colour and side
        
        Params:
            colour (str) - the colour of the rook (WHITE or BLACK)
            side (str) - the side of the rook (SHORT or LONG)
        """
        if colour == WHITE and side == LONG:
            self.wLongRookMoved += 1
        elif colour == WHITE and side == SHORT:
            self.wShortRookMoved += 1 
        elif colour == BLACK and side == LONG:
            self.bLongRookMoved += 1
        elif colour == BLACK and side == SHORT:
            self.bShortRookMoved += 1
    
    
    def decrement_rook_moved(self, colour, side):
        """
        Method:
            Decrements the rook moved flag for the given colour and side
            
        Params:
            colour (str) - the colour of the rook (WHITE or BLACK)
            side (str) - the side of the rook (SHORT or LONG)
        """
        if colour == WHITE and side == SHORT:
            self.wShortRookMoved -= 1
        elif colour == WHITE and side == LONG:
            self.wLongRookMoved -= 1 
        elif colour == BLACK and side == SHORT:
            self.bShortRookMoved -= 1
        else:
            self.bLongRookMoved -= 1
    
    
    def get_rook_pos(self):
        """
        Method:
            Returns the self.rooks dictionary
            which keeps track of the rooks movement
        """
        return self.rooks
    
    
    def get_zobrist(self):
        """
        Method:
            Returns the zobrist object
        """
        return self.zobrist
    
    def get_current_zobrist(self):
        """
        Method:
            Returns the current zobrist key of the board
        """
        return self.currentZobristKey
    
    
    def set_current_zobrist(self, newKey):
        """
        Method:
            Sets the current zobrist key
            
        Params:
            newKey(int)
        """
        self.currentZobristKey = newKey
        
        
    def increment_position_hash(self, zobristKey):
        # Increment count
        if zobristKey not in self.positionHash:
            self.positionHash[zobristKey] = 1
        else:
            self.positionHash[zobristKey] += 1
            
    
    def decrement_position_hash(self, zobristKey):
        # Decrement count
        if zobristKey not in self.positionHash:
            return
        else:
            self.positionHash[zobristKey] -= 1
            
    
    def setup_kiwipete(self):
        """
        Method:
            Sets Up the kiwipete position for perft debugging.
            Particularly useful for finding castling and enpassant
            errors as starting position takes more than 6 moves to
            do so
        """
        
        self.wPawns =   0b0000000000000000000000000000100000010000000000001110011100000000
        self.wRooks =   0b0000000000000000000000000000000000000000000000000000000010000001 
        self.wKnights = 0b0000000000000000000000000001000000000000000001000000000000000000  
        self.wBishops = 0b0000000000000000000000000000000000000000000000000001100000000000  
        self.wQueen =   0b0000000000000000000000000000000000000000001000000000000000000000  
        self.wKing =    0b0000000000000000000000000000000000000000000000000000000000010000 

        self.bPawns =   0b0000000000101101010100000000000000000010100000000000000000000000
        self.bRooks =   0b1000000100000000000000000000000000000000000000000000000000000000  
        self.bKnights = 0b0000000000000000001000100000000000000000000000000000000000000000  
        self.bBishops = 0b0000000001000000000000010000000000000000000000000000000000000000  
        self.bQueen =   0b0000000000010000000000000000000000000000000000000000000000000000  
        self.bKing =    0b0001000000000000000000000000000000000000000000000000000000000000
        
        self.board = {
            (f'{WHITE} {PAWN}') : self.wPawns,
            (f'{WHITE} {KNIGHT}') : self.wKnights,
            (f'{WHITE} {ROOK}') : self.wRooks,
            (f'{WHITE} {BISHOP}') : self.wBishops,
            (f'{WHITE} {QUEEN}') : self.wQueen,
            (f'{WHITE} {KING}') : self.wKing,
            (f'{BLACK} {PAWN}') : self.bPawns,
            (f'{BLACK} {KNIGHT}') : self.bKnights,
            (f'{BLACK} {ROOK}') : self.bRooks,
            (f'{BLACK} {BISHOP}') : self.bBishops,
            (f'{BLACK} {QUEEN}') : self.bQueen,
            (f'{BLACK} {KING}') : self.bKing,
            (f'{BLACK}') : self.bPawns | self.bKnights | self.bRooks | self.bBishops | self.bQueen | self.bKing,
            (f'{WHITE}') : self.wPawns | self.wKnights | self.wRooks | self.wBishops | self.wQueen | self.wKing
        }

        
    def load_fen(self, fen):
        """
        Method:
            Loads a FEN (Forsyth-Edwards Notation) string and sets up the board.
            
        Params:
            fen (str) - FEN string representing the position
            
        FEN Format: "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        Parts:
            1. Piece placement (rank 8 to rank 1)
            2. Active color (w/b)
            3. Castling rights (KQkq or -)
            4. En passant target square (e3 or -)
            5. Halfmove clock
            6. Fullmove number
        """
        parts = fen.split()
        
        if len(parts) < 4:
            raise ValueError("Invalid FEN string - must have at least 4 parts")
        
        piece_placement = parts[0]
        active_color = parts[1]
        castling_rights = parts[2]
        en_passant = parts[3]
        halfmove_clock = int(parts[4]) if len(parts) > 4 else 0
        fullmove_number = int(parts[5]) if len(parts) > 5 else 1
        
        # Reset all bitboards
        self.wPawns = 0
        self.wRooks = 0
        self.wKnights = 0
        self.wBishops = 0
        self.wQueen = 0
        self.wKing = 0
        self.bPawns = 0
        self.bRooks = 0
        self.bKnights = 0
        self.bBishops = 0
        self.bQueen = 0
        self.bKing = 0
        
        # Parse piece placement
        ranks = piece_placement.split('/')
        
        for rank_idx, rank in enumerate(ranks):
            file_idx = 0
            
            for char in rank:
                if char.isdigit():
                    # Empty squares
                    file_idx += int(char)
                else:
                    # Calculate bit position (rank 8 is index 7, rank 1 is index 0)
                    bit_position = (7 - rank_idx) * 8 + file_idx
                    bit = 1 << bit_position
                    
                    # Place piece on appropriate bitboard
                    if char == 'P':
                        self.wPawns |= bit
                    elif char == 'N':
                        self.wKnights |= bit
                    elif char == 'B':
                        self.wBishops |= bit
                    elif char == 'R':
                        self.wRooks |= bit
                    elif char == 'Q':
                        self.wQueen |= bit
                    elif char == 'K':
                        self.wKing |= bit
                    elif char == 'p':
                        self.bPawns |= bit
                    elif char == 'n':
                        self.bKnights |= bit
                    elif char == 'b':
                        self.bBishops |= bit
                    elif char == 'r':
                        self.bRooks |= bit
                    elif char == 'q':
                        self.bQueen |= bit
                    elif char == 'k':
                        self.bKing |= bit
                    
                    file_idx += 1
        
        # Update board dictionary
        self.board = {
            (f'{WHITE} {PAWN}'): self.wPawns,
            (f'{WHITE} {KNIGHT}'): self.wKnights,
            (f'{WHITE} {ROOK}'): self.wRooks,
            (f'{WHITE} {BISHOP}'): self.wBishops,
            (f'{WHITE} {QUEEN}'): self.wQueen,
            (f'{WHITE} {KING}'): self.wKing,
            (f'{BLACK} {PAWN}'): self.bPawns,
            (f'{BLACK} {KNIGHT}'): self.bKnights,
            (f'{BLACK} {ROOK}'): self.bRooks,
            (f'{BLACK} {BISHOP}'): self.bBishops,
            (f'{BLACK} {QUEEN}'): self.bQueen,
            (f'{BLACK} {KING}'): self.bKing,
            (f'{BLACK}'): self.bPawns | self.bKnights | self.bRooks | self.bBishops | self.bQueen | self.bKing,
            (f'{WHITE}'): self.wPawns | self.wKnights | self.wRooks | self.wBishops | self.wQueen | self.wKing
        }
        
        # Set active color
        if active_color == 'w':
            self.colour = WHITE
        else:
            self.colour = BLACK
        
        # Parse castling rights and set up rook tracking
        self.wKingMoved = 0 if 'K' in castling_rights or 'Q' in castling_rights else 1
        self.bKingMoved = 0 if 'k' in castling_rights or 'q' in castling_rights else 1
        
        # Find actual rook positions and set up rook tracking
        self.wShortRook = 0
        self.wLongRook = 0
        self.bShortRook = 0
        self.bLongRook = 0
        
        self.wShortRookMoved = 0
        self.wLongRookMoved = 0
        self.bShortRookMoved = 0
        self.bLongRookMoved = 0
        
        # White kingside rook (h1 = bit 7)
        if 'K' in castling_rights and (self.wRooks & (1 << 7)):
            self.wShortRook = 1 << 7
            self.wShortRookMoved = 0
        else:
            # Find rightmost white rook on rank 1 if any
            for bit_pos in range(7, -1, -1):
                if self.wRooks & (1 << bit_pos):
                    self.wShortRook = 1 << bit_pos
                    break
            self.wShortRookMoved = 1
        
        # White queenside rook (a1 = bit 0)
        if 'Q' in castling_rights and (self.wRooks & (1 << 0)):
            self.wLongRook = 1 << 0
            self.wLongRookMoved = 0
        else:
            # Find leftmost white rook on rank 1 if any
            for bit_pos in range(0, 8):
                if self.wRooks & (1 << bit_pos) and not (self.wShortRook & (1 << bit_pos)):
                    self.wLongRook = 1 << bit_pos
                    break
            self.wLongRookMoved = 1
        
        # Black kingside rook (h8 = bit 63)
        if 'k' in castling_rights and (self.bRooks & (1 << 63)):
            self.bShortRook = 1 << 63
            self.bShortRookMoved = 0
        else:
            # Find rightmost black rook on rank 8 if any
            for bit_pos in range(63, 55, -1):
                if self.bRooks & (1 << bit_pos):
                    self.bShortRook = 1 << bit_pos
                    break
            self.bShortRookMoved = 1
        
        # Black queenside rook (a8 = bit 56)
        if 'q' in castling_rights and (self.bRooks & (1 << 56)):
            self.bLongRook = 1 << 56
            self.bLongRookMoved = 0
        else:
            # Find leftmost black rook on rank 8 if any
            for bit_pos in range(56, 64):
                if self.bRooks & (1 << bit_pos) and not (self.bShortRook & (1 << bit_pos)):
                    self.bLongRook = 1 << bit_pos
                    break
            self.bLongRookMoved = 1
        
        self.rooks = {
            f'{WHITE} {SHORT}': self.wShortRook,
            f'{WHITE} {LONG}': self.wLongRook,
            f'{BLACK} {SHORT}': self.bShortRook,
            f'{BLACK} {LONG}': self.bLongRook
        }
        
        # Set en passant target
        if en_passant != '-':
            file = ord(en_passant[0]) - ord('a')
            rank = int(en_passant[1]) - 1
            self.enpassantTarget = 1 << (rank * 8 + file)
        else:
            self.enpassantTarget = None
        
        # Set clocks
        self.halfMoveClock = halfmove_clock
        self.fullMoveNumber = fullmove_number
        
        # Reset zobrist and position hash
        self.positionHash = {}
        self.currentZobristKey = self.zobrist.calculate_zobrist_key(self)
        self.positionHash[self.currentZobristKey] = 1
        
        # Reset move stack
        self.lastMoves = []
