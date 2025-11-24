"""
Imports
"""
import unittest

from src.array_based_classes.pieces.king import King
from src.array_based_classes.pieces.rook import Rook
from src.array_based_classes.pieces.queen import Queen
from src.array_based_classes.pieces.bishop import Bishop
from src.array_based_classes.pieces.knight import Knight
from src.array_based_classes.pieces.pawn import Pawn
from src.base_classes.board import Board
from src.base_classes.arbiter import Arbiter
from src.constants.constPieces import *
from src.constants.constColours import *

"""
Classes
"""
class TestArbiter(unittest.TestCase):
    def setUp(self):
        self.arbiter = Arbiter()
        self.board = Board()
        self.king = King(KING, WHITE)
        
    def test_is_in_check(self):
        """
        Method:
            tests if is_in_check function returns the
            correct bool
        """
        rook = Rook(ROOK, BLACK)
        
        # Rook is inline with king, there should be a check
        self.board.add_piece(self.king, 3, 3)
        self.board.add_piece(rook, 7, 3)
        self.assertTrue(self.arbiter.is_in_check(self.board, self.king))
        
        # Rook is not inline with king, shouldn't be a check
        self.board.remove_piece(7, 3)
        self.board.add_piece(rook, 6, 1)
        self.assertFalse(self.arbiter.is_in_check(self.board, self.king))
        
    
    def test_is_in_checkmate(self):
        """
        Method:
            tests whether the is_in_checkmate method
            works as expected
        """
        
        self.board.add_piece(self.king, 0, 0)
        self.board.add_piece(Queen(QUEEN, BLACK), 1, 1)
        self.board.add_piece(Bishop(BISHOP, BLACK), 2, 2)
        
        # King can't take the piece and is checkmate
        self.assertTrue(self.arbiter.is_in_checkmate(self.board, self.king))
        
        self.setUp()
        self.board.add_piece(self.king, 0, 0)
        self.board.add_piece(Queen(QUEEN, BLACK), 1, 1)
        
        # King is in check but can take the piece
        self.assertFalse(self.arbiter.is_in_checkmate(self.board, self.king))
        
        self.setUp()
        self.board.add_piece(self.king, 0, 0)
        self.board.add_piece(Queen(QUEEN, BLACK), 1, 1)
        self.board.add_piece(Bishop(BISHOP, BLACK), 2, 2)
        self.board.add_piece(Bishop(BISHOP, WHITE), 0, 2)
        
        # King is in check and can't take but bishop can take
        self.assertFalse(self.arbiter.is_in_checkmate(self.board, self.king))
        
    
    def test_is_in_stalemate(self):
        """
        Method:
            Tests whether the in_stale_mate function works correctly
        """
        
        self.board.add_piece(self.king, 0, 7)
        self.board.add_piece(Rook(ROOK, BLACK), 7, 6)
        self.board.add_piece(Rook(ROOK, BLACK), 1, 3)
        self.board.add_piece(Pawn(PAWN, WHITE), 4, 4)
        self.board.add_piece(Pawn(PAWN, BLACK), 3, 4)
        
        # No pieces can move and king, should be stalemate
        self.assertTrue(self.arbiter.is_in_stalemate(self.board, self.king))

        self.setUp()
        
        self.board.add_piece(self.king, 0, 7)
        self.board.add_piece(Rook(ROOK, BLACK), 7, 6)
        self.board.add_piece(Rook(ROOK, BLACK), 1, 3)
        self.board.add_piece(Pawn(PAWN, WHITE), 3, 4)
        self.board.add_piece(Pawn(PAWN, BLACK), 4, 4)
        
        # Pawns should be able to move, therefor no stalemate
        self.assertFalse(self.arbiter.is_in_stalemate(self.board, self.king))

    
    def test_insufficient_materials(self):
        """
        Method:
            tests if the insufficient_materials method works as
            expected. There are a few cases where this applies.
            If both sides have one of the following and are no
            pawns on the board:
                1. lone king
                2. king and bishop
                3. king and knight
        """
        # Case 1, 2 lone kings, insufficient
        self.board.add_piece(self.king, 0, 0)
        self.board.add_piece(King(KING, BLACK), 7, 7)
        self.assertTrue(self.arbiter.insufficient_material(self.board))
        
        # Case 2, 1 lone king and king and bishop, insufficient
        self.setUp()
        self.board.add_piece(self.king, 0, 0)
        self.board.add_piece(King(KING, BLACK), 7, 7)
        self.board.add_piece(Bishop(BISHOP, BLACK), 5, 6)
        self.assertTrue(self.arbiter.insufficient_material(self.board))
        
        # Case 3, 1 lone king and king and pawn, sufficient
        self.setUp()
        self.board.add_piece(self.king, 0, 0)
        self.board.add_piece(King(KING, BLACK), 7, 7)
        self.board.add_piece(Pawn(PAWN, BLACK), 5, 6)
        self.assertFalse(self.arbiter.insufficient_material(self.board))
        
        # Case 4, 1 lone king and a king and two knights, suffcient
        self.setUp()
        self.board.add_piece(self.king, 0, 0)
        self.board.add_piece(King(KING, BLACK), 7, 7)
        self.board.add_piece(Knight(KNIGHT, BLACK), 5, 6)
        self.board.add_piece(Knight(KNIGHT, BLACK), 3, 3)
        self.assertFalse(self.arbiter.insufficient_material(self.board))
    
    
    def test_50_move_rule(self):
        pass
    
    
    def test_is_in_repetition(self):
        pass
    
    
