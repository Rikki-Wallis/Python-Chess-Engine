"""
Imports
"""
import unittest

from src.array_based_classes.pieces.rook import Rook
from src.base_classes.board import Board
from src.constants.constPieces import *
from src.constants.constColours import *

"""
Classes
"""
class TestBoard(unittest.TestCase):
    def setUp(self):
        """
        Method:
            Allow all tests to access a freshly initiated
            board.
        """
        self.board = Board()
        self.piece = Rook(ROOK, WHITE)
    
    
    def test_init(self):
        """
        Method:
            Test the initialisation of the board.
            All 64 tiles should be empty.
        """
        # Set counter to check if 64 tiles
        counter = 0 
        
        # Iterate through squares and check if it is empty
        for rank in self.board.get_board():
            for tile in rank:
                self.assertIsNone(tile)
                counter += 1
                
        # Check if counter = 64
        self.assertEqual(counter, 64)
    
    
    def test_add_piece(self):
        """
        Method:
            Check if pieces can be successfully added to the board.
            If out of bounds of board, function should create error.
        """
        # Create mock variables
        mockRank = 3
        mockFile = 2
        
        # Add piece and retrieve board
        self.board.add_piece(self.piece, mockRank, mockFile)
        board = self.board.get_board()
        
        # Test in right position
        self.assertEqual(self.piece, self.board.get_piece(mockRank, mockFile))
        
        # Test updated position of piece
        self.assertEqual((mockRank, mockFile), self.piece.get_position())
        
        # Case out of bounds
        self.assertRaises(ValueError, self.board.add_piece, self.piece, 10, 10)
        
        
        
    def test_remove_piece(self):
        """
        Method:
            Check if remove piece function works.
            Function should return the piece that is
            on the given tile
        """
        # Add piece to board
        self.board.add_piece(self.piece, 2, 3)
        
        # Can it remove piece
        self.assertEqual(self.board.remove_piece(2, 3), self.piece)
        
        # Must return None if no piece is on tile
        self.assertIsNone(self.board.remove_piece(0,0))
        
        # Check if it produces an error with out of bounds
        self.assertRaises(ValueError, self.board.remove_piece, 10, 10)
        
        
        
        
        