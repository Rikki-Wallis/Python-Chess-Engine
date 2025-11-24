"""
Imports
"""
try:
    from src.data_structures.stack import Stack
    from src.constants.constColours import *
except:
    from data_structures.stack import Stack
    from constants.constColours import *
    
    
"""
Classes
"""
class Board:
    
    """ ----------------------------------- Constructer ----------------------------------- """
    
    
    def __init__(self):
        # Board state variables
        self.moveStack = Stack()
        self.positionHash = {}
        self.halfMoveClock = 0
        self.currentColour = WHITE
        
        # Any additional settup
        self.additionalSettup()
    
    
    """ ----------------------------------- Abstract Methods ----------------------------------- """
    
    
    def additionalSettup(self):
        """
        Method:
            Any additional settup for the board (to be overridden by subclasses)
        """
        pass
    
    
    def set_pieces_list(self):
        """
        Method:
            Sets the pieces list (to be overridden by subclasses)
        """
    
    def get_piece(self, row, col):
        """
        Method:
            Returns the piece at a given position (to be overridden by subclasses)
        """
        pass
    
    
    def hash_position(self):
        """
        Method:
            Hashes the current position (to be overridden by subclasses)
        """
        pass
    
    
    """ ----------------------------------- Getters and Setters ----------------------------------- """
    
    
    def get_board(self):
        """
        Method:
            Returns the board (to be overridden by subclasses)
        """
        return self.board
    
    
    def get_move_stack(self):
        """
        Method:
            Returns the move stack
        """
        return self.moveStack
    
    
    def get_last_move(self):
        """
        Method:
            Returns the last moved piece
        """
        return self.moveStack.peek()
    
    
    def pop_last_move(self):
        """
        Method:
            Pops the last moved piece from the stack
        """
        return self.moveStack.pop()
    
    
    def push_move(self, piece):
        """
        Method:
            Pushes a piece onto the move stack
        """
        self.moveStack.push(piece)
        

    def get_position_hash(self):
        """
        Method:
            Returns the position hash
        """
        return self.positionHash
    
    
    def get_position_count(self, hashNumber):
        """
        Method:
            Returns the count of a given position hash
        
        Params:
            hashNumber (int)
        """
        if hashNumber not in self.positionHash:
            return 0
        else:
            return self.positionHash[hashNumber]
    
    
    def increment_position_hash(self, key=None):
        """
        Method:
            Converts the current position to a hash number and
            increments the count
        """
        # Fetch hash number
        if key:
            hashNumber = key
        else:
            hashNumber = self.hash_position()
        
        # Increment count
        if hashNumber not in self.positionHash:
            self.positionHash[hashNumber] = 1
        else:
            self.positionHash[hashNumber] += 1
    
    
    def decrement_position_hash(self, key=None):
        """
        Method:
            Converts the current position to a hash number and
            decrements the count
        """
        # Fetch hash number
        if key:
            hashNumber = key
        else:
            hashNumber = self.hash_position()
        
        # Decrement count
        if hashNumber in self.positionHash:
            self.positionHash[hashNumber] -= 1
    
    
    def get_half_move_clock(self):
        """
        Method:
            Returns the half move clock
        """
        return self.halfMoveClock

    
    def increment_half_move_clock(self):
        """
        Method:
            Increments the half move clock
        """
        self.halfMoveClock += 1
        
    
    def decrement_half_move_clock(self):
        """
        Method:
            Decrements the half move clock
        """
        if self.halfMoveClock > 0:
            self.halfMoveClock -= 1
    
    
    def reset_half_move_clock(self):
        """
        Method:
            Resets the half move clock
        """
        self.halfMoveClock = 0
    
    
    def set_half_move_clock(self, value):
        """
        Method:
            Sets the half move clock to a given value
        
        Params:
            value (int)
        """
        self.halfMoveClock = value
        
    
    def get_colour(self):
        """
        Method:
            Returns the current colour to move
        """
        return self.currentColour
    
    
    def flip_colour(self):
        """
        Method:
            Flips the current colour to move
        """
        if self.currentColour == BLACK:
            self.currentColour = WHITE
        else:
            self.currentColour = BLACK
    
    def get_king(self, colour):
        """
        Method:
            Returns the king of the given colour
        
        Params:
            colour (ENUM)
        """
        if colour == WHITE:
            return self.wKing
        else:
            return self.bKing
        
    def reset_board(self):
        """
        Method:
            Resets the board to the starting position
        """
        self.__init__()