"""
Imports
"""
import unittest
from unittest import mock



from src.array_based_classes.pieces.bishop import Bishop
from src.array_based_classes.pieces.pawn import Pawn
from src.array_based_classes.pieces.king import King
from src.array_based_classes.pieces.rook import Rook
from src.base_classes.move import Move
from src.base_classes.board import Board
from src.constants.constColours import *
from src.constants.constPieces import *
from src.constants.constFlags import *

"""
Classes
"""
class TestMove(unittest.TestCase):
    def setUp(self):
        self.board = Board()
    
    def test_init(self):
        """
        Method:
            Tests that the move class initialises correctly
        """        
        bishop = Bishop(BISHOP, WHITE)
        pawn = Pawn(PAWN, BLACK)
        
        self.board.add_piece(bishop, 0, 0)
        self.board.add_piece(pawn, 6, 6)

        moveFrom = (0, 0)
        moveTo = (6, 6)
        move = Move(self.board, moveFrom, moveTo)

        self.assertEqual(move.moveTo, moveTo)
        self.assertEqual(move.moveFrom, moveFrom)
        self.assertEqual(move.homePiece, bishop)
        self.assertEqual(move.targetPiece, pawn)  
    
    def test_make_move(self):
        """
        Method:
            Tests if make_move method works as expected
            handling normal moves, castling and enpassant
        """
        # Normal case
        bishop = Bishop(BISHOP, WHITE)
        ogTimesMoved = bishop.get_times_moved()
        self.board.add_piece(bishop, 0, 0)
        move = Move(self.board, (0,0), (6,6))
        
        move.make_move()
        
        # Does the home and target square contain the right pieces
        self.assertIsNone(self.board.get_piece(0, 0))
        self.assertEqual(self.board.get_piece(6, 6), (bishop))
        # Increments move counter correctly
        self.assertEqual(bishop.get_times_moved(), ogTimesMoved+1)
        
        colours = [7, 0] # white, black
        for row in colours:
            # Short castling 
            self.setUp()
            king = King(KING, WHITE)
            rook = Rook(ROOK, WHITE)
            ogKingMove = king.get_times_moved()
            ogRookMove = rook.get_times_moved()
            self.board.add_piece(king, row, 4)
            self.board.add_piece(rook, row, 7)
            move = Move(self.board, (row, 4), (row,6), flag=SHORT_CASTLE)

            move.make_move()

            self.assertIsNone(self.board.get_piece(row, 4))
            self.assertIsNone(self.board.get_piece(row, 7))
            self.assertEqual(self.board.get_piece(row, 6), king)
            self.assertEqual(self.board.get_piece(row,5), rook)
            
            self.assertEqual(king.get_times_moved(), ogKingMove+1)
            self.assertEqual(rook.get_times_moved(), ogRookMove+1)

            # Long Castling
            self.setUp()
            king = King(KING, WHITE)
            rook = Rook(ROOK, WHITE)
            ogKingMove = king.get_times_moved()
            ogRookMove = rook.get_times_moved()
            self.board.add_piece(king, row, 4)
            self.board.add_piece(rook, row, 0)
            move = Move(self.board, (row, 4), (row,2), flag=LONG_CASTLE)
            
            move.make_move()
            
            self.assertIsNone(self.board.get_piece(row, 4))
            self.assertIsNone(self.board.get_piece(row, 0))
            self.assertEqual(self.board.get_piece(row, 2), king)
            self.assertEqual(self.board.get_piece(row, 3), rook)
            
            self.assertEqual(king.get_times_moved(), ogKingMove+1)
            self.assertEqual(rook.get_times_moved(), ogRookMove+1)

        # enpassent
        wPlacement = [(4, 6), (3, 5)]
        bPlacement = [(4, 5), (3, 4)]
        
        
        moveFrom = [(4,5), (3,5)]
        moveTo = [(5,6), (2,4)]
        
        for i in range(2):
            self.setUp()
            whitePawn = Pawn(PAWN, WHITE)
            blackPawn = Pawn(PAWN, BLACK)
            
            pawnToCheckTimesMoved = [blackPawn, whitePawn]
            
            self.board.add_piece(whitePawn, wPlacement[i][0], wPlacement[i][1])
            self.board.add_piece(blackPawn, bPlacement[i][0], bPlacement[i][1])
            ogTimesMoved = pawnToCheckTimesMoved[i].get_times_moved()
            move = Move(self.board, moveFrom[i], moveTo[i], flag=ENPASSANT)
            
            move.make_move()
            
            self.assertIsNone(self.board.get_piece(moveFrom[i][0], moveFrom[i][1]))
            self.assertEqual(self.board.get_piece(moveTo[i][0], moveTo[i][1]), pawnToCheckTimesMoved[i])
            self.assertEqual(pawnToCheckTimesMoved[i].get_times_moved(), ogTimesMoved+1)
            

    def test_revert_move(self):
        """
        Method:
            Tests if revert_move method works as expected
            for handling normal moves, castling and enpassent
        """
        # Normal case
        bishop = Bishop(BISHOP, WHITE)
        ogTimesMoved = bishop.get_times_moved()
        self.board.add_piece(bishop, 0, 0)
        move = Move(self.board, (0,0), (6,6))
        
        move.make_move()
        move.revert_move()
        
        # Does the home and target square contain the right pieces
        self.assertEqual(self.board.get_piece(0, 0), bishop)
        self.assertNotEqual(self.board.get_piece(6, 6), bishop)
        # Increments move counter correctly
        self.assertEqual(bishop.get_times_moved(), ogTimesMoved)
        
        colours = [7, 0] # white, black
        for row in colours:
            # Short castling 
            self.setUp()
            king = King(KING, WHITE)
            rook = Rook(ROOK, WHITE)
            ogKingMove = king.get_times_moved()
            ogRookMove = rook.get_times_moved()
            self.board.add_piece(king, row, 4)
            self.board.add_piece(rook, row, 7)
            move = Move(self.board, (row, 4), (row,6), flag=SHORT_CASTLE)

            move.make_move()
            move.revert_move()
            
            self.assertEqual(self.board.get_piece(row, 4), king)
            self.assertEqual(self.board.get_piece(row, 7), rook)
            self.assertNotEqual(self.board.get_piece(row, 6), king)
            self.assertNotEqual(self.board.get_piece(row,5), rook)
            
            self.assertEqual(king.get_times_moved(), ogKingMove)
            self.assertEqual(rook.get_times_moved(), ogRookMove)

            # Long Castling
            self.setUp()
            king = King(KING, WHITE)
            rook = Rook(ROOK, WHITE)
            ogKingMove = king.get_times_moved()
            ogRookMove = rook.get_times_moved()
            self.board.add_piece(king, row, 4)
            self.board.add_piece(rook, row, 0)
            move = Move(self.board, (row, 4), (row,2), flag=LONG_CASTLE)
            
            move.make_move()
            move.revert_move()
            
            self.assertEqual(self.board.get_piece(row, 4), king)
            self.assertEqual(self.board.get_piece(row, 0), rook)
            self.assertNotEqual(self.board.get_piece(row, 2), king)
            self.assertNotEqual(self.board.get_piece(row, 3), rook)
            
            self.assertEqual(king.get_times_moved(), ogKingMove)
            self.assertEqual(rook.get_times_moved(), ogRookMove)

        # enpassent
        wPlacement = [(4, 6), (3, 5)]
        bPlacement = [(4, 5), (3, 4)]
        
        
        moveFrom = [(4,5), (3,5)]
        moveTo = [(5,6), (2,4)]
        
        for i in range(2):
            self.setUp()
            whitePawn = Pawn(PAWN, WHITE)
            blackPawn = Pawn(PAWN, BLACK)
            
            pawnToCheckTimesMoved = [blackPawn, whitePawn]
            
            self.board.add_piece(whitePawn, wPlacement[i][0], wPlacement[i][1])
            self.board.add_piece(blackPawn, bPlacement[i][0], bPlacement[i][1])
            ogTimesMoved = pawnToCheckTimesMoved[i].get_times_moved()
            move = Move(self.board, moveFrom[i], moveTo[i], flag=ENPASSANT)
            
            move.make_move()
            move.revert_move()
            
            self.assertEqual(self.board.get_piece(moveFrom[i][0], moveFrom[i][1]), pawnToCheckTimesMoved[i])
            self.assertEqual(pawnToCheckTimesMoved[i].get_times_moved(), ogTimesMoved)
    