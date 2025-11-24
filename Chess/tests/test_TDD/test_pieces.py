"""
Imports
"""
import unittest

from src.base_classes.piece import Piece
from src.array_based_classes.pieces.rook import Rook
from src.array_based_classes.pieces.queen import Queen
from src.array_based_classes.pieces.bishop import Bishop
from src.array_based_classes.pieces.knight import Knight
from src.array_based_classes.pieces.king import King
from src.array_based_classes.pieces.pawn import Pawn
from src.base_classes.board import Board
from src.constants.constPieces import *
from src.constants.constColours import *
from src.constants.constFlags import *

"""
Classes
"""
class TestPiece(unittest.TestCase):
    def test_init(self): 
        """
        Method:
            Test if initial piece values are what they should be
        """
        # Create the piece
        piece = Piece(PAWN, WHITE)
        
        # Has he moved yet?
        self.assertEqual(0, piece.get_times_moved())
        # Is it a Rook
        self.assertEqual(PAWN, piece.get_type())
        # Is it a white or black rook
        self.assertEqual(WHITE, piece.get_colour())
        # What is its current position
        self.assertEqual(None, piece.get_position())

class TestRook(unittest.TestCase):
    def setUp(self):
        """
        Method:
            Initialise new board each test
        """
        self.board = Board()
        self.rook = Rook(ROOK, WHITE)
        
        
    def test_get_moves_empty_board(self):
        """
        Method:
            Tests whether move generation is correct
            for an empty board with just a single rook
        """
        # Create rook and add to the board
        self.board.add_piece(self.rook, 2, 3)
        
        expectedMoves = [(1,3), (0,3),   # Up 
                         (2,4), (2,5), (2,6), (2,7), # Right
                         (3,3), (4,3), (5,3), (6,3), (7,3), # Down
                         (2,2), (2,1), (2,0)  # Left
                        ] 
        
        moves = self.rook.get_moves(self.board)
        output = [move.moveTo for move in moves]
        
        # Do moves align with expected moves?
        self.assertEqual(expectedMoves, output, f'expected list: {expectedMoves}, output: {self.rook.get_moves(self.board)}')
    
    
    def test_get_moves_with_captures(self):
        """
        Method:
            Tests whetehr move generation is valid when
            captures and same coloured pieces are present.
        """
        # Create pieces
        pawnRight = Pawn(PAWN, BLACK)
        pawnUp = Pawn(PAWN, BLACK)
        pawnDown = Pawn(PAWN, WHITE)
        pawnLeft = Pawn(PAWN, WHITE)
        
        # Add pieces to the board
        self.board.add_piece(self.rook, 3, 3)
        self.board.add_piece(pawnUp, 0, 3)
        self.board.add_piece(pawnRight, 3, 6)
        self.board.add_piece(pawnDown, 6, 3)
        self.board.add_piece(pawnLeft, 3, 1)
        
        expectedMoves = [(2,3), (1,3), (0,3),  # Up
                         (3,4), (3,5), (3, 6), # Right
                         (4,3), (5,3), # Down
                         (3,2) # Left
                        ]
        
        moves = self.rook.get_moves(self.board)
        output = [move.moveTo for move in moves]

        self.assertEqual(expectedMoves, output, f'expected list: {expectedMoves}, output: {self.rook.get_moves(self.board)}')
        
    def test_get_moves_boundaries(self):
        """
        Method:
            Tests if get_moves works as expected at boundaries
        """
        # Test top left
        self.board.add_piece(self.rook, 0, 0)
        
        expectedMoves = [(0,1), (0,2), (0,3), (0,4), (0,5), (0,6), (0,7),# Right
                         (1,0), (2,0), (3,0), (4,0), (5,0), (6,0), (7,0) # Down
                        ]
        
        moves = self.rook.get_moves(self.board)
        output = [move.moveTo for move in moves]
        
        self.assertEqual(expectedMoves, output, f'top left, expected: {expectedMoves}, output: {self.rook.get_moves(self.board)}')
        
        # Test top right
        self.setUp()
        self.board.add_piece(self.rook, 0, 7)
        
        expectedMoves = [(1,7), (2,7), (3,7), (4,7), (5,7), (6,7), (7,7), # Down
                         (0,6), (0,5), (0,4), (0,3), (0,2), (0,1), (0,0)# Left
                        ]
        
        moves = self.rook.get_moves(self.board)
        output = [move.moveTo for move in moves]

        self.assertEqual(expectedMoves, output, f'top right, expected: {expectedMoves}, output: {self.rook.get_moves(self.board)}')
        
        # Test bottom left
        self.setUp()
        self.board.add_piece(self.rook, 7, 0)
        
        expectedMoves = [(6,0), (5,0), (4,0), (3,0), (2,0), (1,0), (0,0), # Up
                         (7,1), (7,2), (7,3), (7,4), (7,5), (7,6), (7,7)  # Right
                        ]
        
        moves = self.rook.get_moves(self.board)
        output = [move.moveTo for move in moves]
        
        self.assertEqual(expectedMoves, output, f'bottom left, expected: {expectedMoves}, output: {self.rook.get_moves(self.board)}')
        
        # Test bottom right
        self.setUp()
        self.board.add_piece(self.rook, 7, 7)
        
        expectedMoves = [(6,7), (5,7), (4,7), (3,7), (2,7), (1,7), (0,7), # Up
                         (7,6), (7,5), (7,4), (7,3), (7,2), (7,1), (7,0),# Left
                        ]
        
        moves = self.rook.get_moves(self.board)
        output = [move.moveTo for move in moves]
        
        self.assertEqual(expectedMoves, output, f'bottom right, expected: {expectedMoves}, output: {self.rook.get_moves(self.board)}')

        
class TestBishop(unittest.TestCase):
    def setUp(self):
        """
        Method:
            Initialise new board each test
        """
        self.board = Board()
        self.bishop = Bishop(BISHOP, WHITE)
        
        
    def test_get_moves_empty_board(self):
        """
        Method:
            Tests whether move generation is correct
            for an empty board with just a single bishop
        """
        #  and add to the board
        self.board.add_piece(self.bishop, 3, 3)
        
        expectedMoves = [(2, 2), (1, 1), (0, 0), # top-left
                         (2, 4), (1, 5), (0, 6), # top-right
                         (4, 4), (5, 5), (6, 6), (7, 7), # bottom-right
                         (4, 2), (5, 1), (6, 0) # bottom-left
                        ] 
        
        moves = self.bishop.get_moves(self.board)
        output = [move.moveTo for move in moves]
        
        # Do moves align with expected moves?
        self.assertEqual(expectedMoves, output, f'expected list: {expectedMoves}, output: {self.bishop.get_moves(self.board)}')
    
    
    def test_get_moves_with_captures(self):
        """
        Method:
            Tests whetehr move generation is valid when
            captures and same coloured pieces are present.
        """
        # Create pieces
        pawnTopRight = Pawn(PAWN, BLACK)
        pawnTopLeft = Pawn(PAWN, BLACK)
        pawnBottomRight = Pawn(PAWN, WHITE)
        pawnBottomLeft = Pawn(PAWN, WHITE)
        
        # Add pieces to the board
        self.board.add_piece(self.bishop, 3, 3)
        self.board.add_piece(pawnTopRight, 1, 5)
        self.board.add_piece(pawnTopLeft, 1, 1)
        self.board.add_piece(pawnBottomRight, 6, 6)
        self.board.add_piece(pawnBottomLeft, 6, 0)
        
        expectedMoves = [(2, 2), (1, 1), # top-left
                         (2, 4), (1, 5), # top-right
                         (4, 4), (5, 5), # bottom-right
                         (4, 2), (5, 1) # bottom-left
                        ] 
        
        moves = self.bishop.get_moves(self.board)
        output = [move.moveTo for move in moves]
        
        self.assertEqual(expectedMoves, output, f'expected list: {expectedMoves}, output: {self.bishop.get_moves(self.board)}')
        
    def test_get_moves_boundaries(self):
        """
        Method:
            Tests if get_moves works as expected at boundaries
        """
        # Test top left
        self.board.add_piece(self.bishop, 0, 0)
        
        expectedMoves = [ (1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7) ]
        
        moves = self.bishop.get_moves(self.board)
        output = [move.moveTo for move in moves]
        
        self.assertEqual(expectedMoves, output, f'top left, expected: {expectedMoves}, output: {self.bishop.get_moves(self.board)}')
        
        # Test top right
        self.setUp()
        self.board.add_piece(self.bishop, 0, 7)
        
        expectedMoves = [(1,6), (2,5), (3,4), (4,3), (5,2), (6,1), (7,0)]
        
        moves = self.bishop.get_moves(self.board)
        output = [move.moveTo for move in moves]

        self.assertEqual(expectedMoves, output, f'top right, expected: {expectedMoves}, output: {self.bishop.get_moves(self.board)}')
        
        # Test bottom left
        self.setUp()
        self.board.add_piece(self.bishop, 7, 0)
        
        expectedMoves = [(6,1), (5,2), (4,3), (3,4), (2,5), (1,6), (0,7)]
        
        moves = self.bishop.get_moves(self.board)
        output = [move.moveTo for move in moves]
        
        self.assertEqual(expectedMoves, output, f'bottom left, expected: {expectedMoves}, output: {self.bishop.get_moves(self.board)}')
        
        # Test bottom right
        self.setUp()
        self.board.add_piece(self.bishop, 7, 7)
        
        expectedMoves = [(6,6), (5,5), (4,4), (3,3), (2,2), (1,1), (0,0)]
        
        moves = self.bishop.get_moves(self.board)
        output = [move.moveTo for move in moves]
        
        self.assertEqual(expectedMoves, output, f'bottom right, expected: {expectedMoves}, output: {self.bishop.get_moves(self.board)}')

        
class TestKnight(unittest.TestCase):
    def setUp(self):
        """
        Method:
            Initialise new board each test
        """
        self.board = Board()
        self.knight = Knight(KNIGHT, WHITE)
        
        
    def test_get_moves_empty_board(self):
        """
        Method:
            Tests whether move generation is correct
            for an empty board with just a single knight
        """
        #  and add to the board
        self.board.add_piece(self.knight, 3, 3)
        
        expectedMoves = [(1, 2), (1, 4), # up
                         (2, 5), (4, 5), # right
                         (5, 4), (5, 2), # down
                         (4, 1), (2, 1)  # left
                        ] 
        
        moves = self.knight.get_moves(self.board)
        output = [move.moveTo for move in moves]
        
        # Do moves align with expected moves?
        self.assertEqual(expectedMoves, output, f'expected list: {expectedMoves}, output: {self.knight.get_moves(self.board)}')
    
    
    def test_get_moves_with_captures(self):
        """
        Method:
            Tests whetehr move generation is valid when
            captures and same coloured pieces are present.
        """

        # Add pieces to the board
        self.board.add_piece(self.knight, 3, 3)
        self.board.add_piece(Pawn(PAWN, WHITE), 1, 2)
        self.board.add_piece(Pawn(PAWN, WHITE), 2, 5)
        self.board.add_piece(Pawn(PAWN, WHITE), 5, 4)
        self.board.add_piece(Pawn(PAWN, WHITE), 4, 1)
        
        self.board.add_piece(Pawn(PAWN, BLACK), 1, 4)
        self.board.add_piece(Pawn(PAWN, BLACK), 4, 5)
        self.board.add_piece(Pawn(PAWN, BLACK), 5, 2)
        self.board.add_piece(Pawn(PAWN, BLACK), 2, 1)
        
        expectedMoves = [(1, 4), # up
                         (4, 5), # right
                         (5, 2), # down
                         (2, 1)  # left
                        ]
        
        moves = self.knight.get_moves(self.board)
        output = [move.moveTo for move in moves]
        
        self.assertEqual(expectedMoves, output, f'expected list: {expectedMoves}, output: {self.knight.get_moves(self.board)}')
        
    def test_get_moves_boundaries(self):
        """
        Method:
            Tests if get_moves works as expected at boundaries
        """
        # Test top left
        self.board.add_piece(self.knight, 0, 0)
        
        expectedMoves = [(1, 2), (2, 1)]
        
        moves = self.knight.get_moves(self.board)
        output = [move.moveTo for move in moves]
        
        self.assertEqual(expectedMoves, output, f'top left, expected: {expectedMoves}, output: {self.knight.get_moves(self.board)}')
        
        # Test top right
        self.setUp()
        self.board.add_piece(self.knight, 0, 7)
        
        expectedMoves = [(2,6), (1,5)]

        moves = self.knight.get_moves(self.board)
        output = [move.moveTo for move in moves]
        
        self.assertEqual(expectedMoves, output, f'top right, expected: {expectedMoves}, output: {self.knight.get_moves(self.board)}')
        
        # Test bottom left
        self.setUp()
        self.board.add_piece(self.knight, 7, 0)
        
        expectedMoves = [(5,1), (6,2)]
        
        moves = self.knight.get_moves(self.board)
        output = [move.moveTo for move in moves]
        
        self.assertEqual(expectedMoves, output, f'bottom left, expected: {expectedMoves}, output: {self.knight.get_moves(self.board)}')
        
        # Test bottom right
        self.setUp()
        self.board.add_piece(self.knight, 7, 7)
        
        expectedMoves = [(5,6), (6,5)]
        
        moves = self.knight.get_moves(self.board)
        output = [move.moveTo for move in moves]
        
        self.assertEqual(expectedMoves, output, f'bottom right, expected: {expectedMoves}, output: {self.knight.get_moves(self.board)}')

class TestKing(unittest.TestCase):
    def setUp(self):
        """
        Method:
            Initialise new board each test
        """
        self.board = Board()
        self.king = King(KING, WHITE)
        
        
    def test_get_moves_empty_board(self):
        """
        Method:
            Tests whether move generation is correct
            for an empty board with just a single king
        """
        #  and add to the board
        self.board.add_piece(self.king, 3, 3)
        
        expectedMoves = [(2,2), (2,3), (2,4), # up
                         (3,4), # right
                         (4,4), (4,3), (4,2), # down
                         (3,2) #left
                         ]
        
        moves = self.king.get_moves(self.board)
        output = [move.moveTo for move in moves]
        
        # Do moves align with expected moves?
        self.assertEqual(expectedMoves, output, f'expected list: {expectedMoves}, output: {self.king.get_moves(self.board)}')
    
    
    def test_get_moves_with_captures(self):
        """
        Method:
            Tests whetehr move generation is valid when
            captures and same coloured pieces are present.
        """

        # Add pieces to the board
        self.board.add_piece(self.king, 3, 3)
        
        self.board.add_piece(Pawn(PAWN, WHITE), 2, 3)
        self.board.add_piece(Pawn(PAWN, WHITE), 2, 4)
        self.board.add_piece(Pawn(PAWN, WHITE), 2, 2)
        self.board.add_piece(Pawn(PAWN, WHITE), 3, 4)
        
        self.board.add_piece(Pawn(PAWN, BLACK), 3, 2)
        self.board.add_piece(Pawn(PAWN, BLACK), 4, 3)
        self.board.add_piece(Pawn(PAWN, BLACK), 4, 4)
        self.board.add_piece(Pawn(PAWN, BLACK), 4, 2)
        
        expectedMoves = [(4,4), (4,3), (4,2), (3,2) ]
        
        moves = self.king.get_moves(self.board)
        output = [move.moveTo for move in moves]
        
        self.assertEqual(expectedMoves, output, f'expected list: {expectedMoves}, output: {self.king.get_moves(self.board)}')
        
    def test_get_moves_boundaries(self):
        """
        Method:
            Tests if get_moves works as expected at boundaries
        """
        # Test top left
        self.board.add_piece(self.king, 0, 0)
        
        expectedMoves = [(0,1), (1,1), (1,0)]
        
        moves = self.king.get_moves(self.board)
        output = [move.moveTo for move in moves]

        self.assertEqual(expectedMoves, output, f'top left, expected: {expectedMoves}, output: {self.king.get_moves(self.board)}')
        
        # Test top right
        self.setUp()
        self.board.add_piece(self.king, 0, 7)
        
        expectedMoves = [(1,7), (1,6), (0,6)]

        moves = self.king.get_moves(self.board)
        output = [move.moveTo for move in moves]
        
        self.assertEqual(expectedMoves, output, f'top right, expected: {expectedMoves}, output: {self.king.get_moves(self.board)}')
        
        # Test bottom left
        self.setUp()
        self.board.add_piece(self.king, 7, 0)
        
        expectedMoves = [(6,0), (6,1), (7,1)]
        
        moves = self.king.get_moves(self.board)
        output = [move.moveTo for move in moves]
        
        self.assertEqual(expectedMoves, output, f'bottom left, expected: {expectedMoves}, output: {self.king.get_moves(self.board)}')
        
        # Test bottom right
        self.setUp()
        self.board.add_piece(self.king, 7, 7)
        
        expectedMoves = [(6,6), (6,7), (7,6)]
        
        moves = self.king.get_moves(self.board)
        output = [move.moveTo for move in moves]
        
        self.assertEqual(expectedMoves, output, f'bottom right, expected: {expectedMoves}, output: {self.king.get_moves(self.board)}')

    def test_generates_short_castle(self):
        """
        Method:
            Tests if move generation correctly generates castling 
            for both colours.
        """
        # White pieces
        self.board.add_piece(self.king, 7, 4)
        self.board.add_piece(Rook(ROOK, WHITE), 7, 7)
        
        moves = self.king.get_moves(self.board)
        output = [move.flag for move in moves]

        self.assertTrue(SHORT_CASTLE in output)
        
        # Black pieces
        self.setUp()
        king = King(KING, BLACK)
        self.board.add_piece(king, 0, 4)
        self.board.add_piece(Rook(ROOK, BLACK), 0, 7)
        
        moves = king.get_moves(self.board)
        output = [move.flag for move in moves]

        self.assertTrue(SHORT_CASTLE in output)
        
    def test_generates_long_castle(self):
        """
        Method:
            Tests if move generation correctly generates long castling 
            for both colours.
        """
        # White pieces
        self.board.add_piece(self.king, 7, 4)
        self.board.add_piece(Rook(ROOK, WHITE), 7, 0)
        
        moves = self.king.get_moves(self.board)
        output = [move.flag for move in moves]

        self.assertTrue(LONG_CASTLE in output)
        
        # Black pieces
        self.setUp()
        king = King(KING, BLACK)
        self.board.add_piece(king, 0, 4)
        self.board.add_piece(Rook(ROOK, BLACK), 0, 0)
        
        moves = king.get_moves(self.board)
        output = [move.flag for move in moves]

        self.assertTrue(LONG_CASTLE in output)

class TestQueen(unittest.TestCase):
    def setUp(self):
        """
        Method:
            Initialise new board each test
        """
        self.board = Board()
        self.queen = Queen(QUEEN, WHITE)
        
        
    def test_get_moves_empty_board(self):
        """
        Method:
            Tests whether move generation is correct
            for an empty board with just a single queen
        """
        # Create queen and add to the board
        self.board.add_piece(self.queen, 3, 3)
        
        expectedMoves = [(2,3), (1,3), (0,3),   # Up 
                         (3,4), (3,5), (3,6), (3,7), # Right
                         (4,3), (5,3), (6,3), (7,3), # Down
                         (3,2), (3,1), (3,0), # Left
                         (2, 2), (1, 1), (0, 0), # top-left
                         (2, 4), (1, 5), (0, 6), # top-right
                         (4, 4), (5, 5), (6, 6), (7, 7), # bottom-right
                         (4, 2), (5, 1), (6, 0) # bottom-left
                        ] 
        
        moves = self.queen.get_moves(self.board)
        output = [move.moveTo for move in moves]
        
        # Do moves align with expected moves?
        self.assertEqual(expectedMoves, output, f'expected list: {expectedMoves}, output: {self.queen.get_moves(self.board)}')
    
    
    def test_get_moves_with_captures(self):
        """
        Method:
            Tests whetehr move generation is valid when
            captures and same coloured pieces are present.
        """        
        # Add pieces to the board
        self.board.add_piece(self.queen, 3, 3)
        self.board.add_piece(Pawn(PAWN, WHITE), 1, 3)
        self.board.add_piece(Pawn(PAWN, BLACK), 3, 5)
        self.board.add_piece(Pawn(PAWN, WHITE), 5, 3)
        self.board.add_piece(Pawn(PAWN, BLACK), 3, 0)
        self.board.add_piece(Pawn(PAWN, WHITE), 1, 1)
        self.board.add_piece(Pawn(PAWN, BLACK), 2, 4)
        self.board.add_piece(Pawn(PAWN, WHITE), 5, 5)
        self.board.add_piece(Pawn(PAWN, BLACK), 5, 1)
        
        expectedMoves = [(2,3),   
                         (3,4), (3,5), 
                         (4,3), 
                         (3,2), (3,1), (3,0), 
                         (2, 2),
                         (2, 4),
                         (4, 4),
                         (4, 2), (5, 1)
                        ] 
        
        moves = self.queen.get_moves(self.board)
        output = [move.moveTo for move in moves]
        
        self.assertEqual(expectedMoves, output, f'expected list: {expectedMoves}, output: {self.queen.get_moves(self.board)}')
        
    def test_get_moves_boundaries(self):
        """
        Method:
            Tests if get_moves works as expected at boundaries
        """
        # Test top left
        self.board.add_piece(self.queen, 0, 0)
        
        expectedMoves = [(0,1), (0,2), (0,3), (0,4), (0,5), (0,6), (0,7),
                         (1,0), (2,0), (3,0), (4,0), (5,0), (6,0), (7,0), 
                         (1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7) ]

        moves = self.queen.get_moves(self.board)
        output = [move.moveTo for move in moves]
        
        self.assertEqual(expectedMoves, output, f'top left, expected: {expectedMoves}, output: {self.queen.get_moves(self.board)}')
        
        # Test top right
        self.setUp()
        self.board.add_piece(self.queen, 0, 7)
        
        expectedMoves = [(1,7), (2,7), (3,7), (4,7), (5,7), (6,7), (7,7), 
                         (0,6), (0,5), (0,4), (0,3), (0,2), (0,1), (0,0),
                         (1,6), (2,5), (3,4), (4,3), (5,2), (6,1), (7,0) ]

        moves = self.queen.get_moves(self.board)
        output = [move.moveTo for move in moves]
        
        self.assertEqual(expectedMoves, output, f'top right, expected: {expectedMoves}, output: {self.queen.get_moves(self.board)}')
        
        # Test bottom left
        self.setUp()
        self.board.add_piece(self.queen, 7, 0)
        
        expectedMoves = [(6,0), (5,0), (4,0), (3,0), (2,0), (1,0), (0,0), 
                         (7,1), (7,2), (7,3), (7,4), (7,5), (7,6), (7,7),
                         (6,1), (5,2), (4,3), (3,4), (2,5), (1,6), (0,7) ]
        
        moves = self.queen.get_moves(self.board)
        output = [move.moveTo for move in moves]
        
        self.assertEqual(expectedMoves, output, f'bottom left, expected: {expectedMoves}, output: {self.queen.get_moves(self.board)}')
        
        # Test bottom right
        self.setUp()
        self.board.add_piece(self.queen, 7, 7)
        
        expectedMoves = [(6,7), (5,7), (4,7), (3,7), (2,7), (1,7), (0,7), 
                         (7,6), (7,5), (7,4), (7,3), (7,2), (7,1), (7,0),
                         (6,6), (5,5), (4,4), (3,3), (2,2), (1,1), (0,0) ]
        
        moves = self.queen.get_moves(self.board)
        output = [move.moveTo for move in moves]
        
        self.assertEqual(expectedMoves, output, f'bottom right, expected: {expectedMoves}, output: {self.queen.get_moves(self.board)}')
        
class TestPawn(unittest.TestCase):
    def setUp(self):
        """
        Method:
            initiates new board and pieces each test
        """
        self.board = Board()
        self.whitePawn = Pawn(PAWN, WHITE)
        self.blackPawn = Pawn(PAWN, BLACK)
        
    def test_pawn_empty_board(self):
        """
        Method:
            tests pawns moving only one square on non starting squares
        """
        self.board.add_piece(self.whitePawn, 5, 1)
        self.board.add_piece(self.blackPawn, 2, 7)
        
        whiteMoves = [(4,1)]
        blackMoves = [(3,7)]
        
        blackMoves2 = self.blackPawn.get_moves(self.board)
        whiteMoves2 = self.whitePawn.get_moves(self.board)
        blackOutput = [move.moveTo for move in blackMoves2]
        whiteOutput = [move.moveTo for move in whiteMoves2]
                
        self.assertEqual(whiteMoves, whiteOutput)
        self.assertEqual(blackMoves, blackOutput)
        
    def test_pawn_move_two_squares_empty(self):
        """
        Method:
            tests if a pawn can move two squares on their respective
            starting square without any obstructions
        """
        self.board.add_piece(self.whitePawn, 6, 1)
        self.board.add_piece(self.blackPawn, 1, 7)
        
        whiteMoves = [(5,1), (4,1)]
        blackMoves = [(2,7), (3,7)]

        blackMoves2 = self.blackPawn.get_moves(self.board)
        whiteMoves2 = self.whitePawn.get_moves(self.board)
        blackOutput = [move.moveTo for move in blackMoves2]
        whiteOutput = [move.moveTo for move in whiteMoves2]
                
        self.assertEqual(whiteMoves, whiteOutput)
        self.assertEqual(blackMoves, blackOutput)
    
    def test_pawn_move_two_squares_obstructed(self):
        """
        Method:
            tests if a pawn given there is a obstruction and it is on its starting
            square that it will only move one square
        """
        self.board.add_piece(self.whitePawn, 6, 1)
        self.board.add_piece(self.blackPawn, 1, 7)
        self.board.add_piece(Pawn(PAWN, BLACK), 4, 1)
        self.board.add_piece(Pawn(PAWN, WHITE), 3, 7)
        
        whiteMoves = [(5,1)]
        blackMoves = [(2,7)]
        
        blackMoves2 = self.blackPawn.get_moves(self.board)
        whiteMoves2 = self.whitePawn.get_moves(self.board)
        blackOutput = [move.moveTo for move in blackMoves2]
        whiteOutput = [move.moveTo for move in whiteMoves2]
                
        self.assertEqual(whiteMoves, whiteOutput)
        self.assertEqual(blackMoves, blackOutput)
    
    def test_captures(self):
        """
        Method:
            tests if the pawn is generating the correct captures
        """
        self.board.add_piece(self.whitePawn, 6, 1)
        self.board.add_piece(self.blackPawn, 1, 5)
        self.board.add_piece(Pawn(PAWN, BLACK), 5, 0)
        self.board.add_piece(Pawn(PAWN, WHITE), 5, 2)
        self.board.add_piece(Pawn(PAWN, WHITE), 2, 4)
        self.board.add_piece(Pawn(PAWN, BLACK), 2, 6)
        
        whiteMoves = [(5,1), (4,1), (5,0)]
        blackMoves = [(2,5), (3,5), (2,4)]
        
        blackMoves2 = self.blackPawn.get_moves(self.board)
        whiteMoves2 = self.whitePawn.get_moves(self.board)
        blackOutput = [move.moveTo for move in blackMoves2]
        whiteOutput = [move.moveTo for move in whiteMoves2]
        
        self.assertEqual(whiteMoves, whiteOutput)
        self.assertEqual(blackMoves, blackOutput)
        
    def test_generates_promotion(self):
        """
        Method:
            checks if the get_moves function properly
            generates promotions for both captures
            and moves
        """
        whitePawn = Pawn(PAWN, WHITE)
        blackPawn = Pawn(PAWN, BLACK)
        
        self.board.add_piece(whitePawn, 1, 0)
        self.board.add_piece(blackPawn, 0, 1)
        
        moves = whitePawn.get_moves(self.board)
        output = [move.flag for move in moves]
        flagCounter = 0
        for flag in output:
            if flag == PROMOTION:
                flagCounter += 1
                
        self.assertEqual(flagCounter, 2)
        
        self.setUp()
        whitePawn = Pawn(PAWN, WHITE)
        blackPawn = Pawn(PAWN, BLACK)
        
        self.board.add_piece(whitePawn, 7, 1)
        self.board.add_piece(blackPawn, 6, 0)
        
        moves = blackPawn.get_moves(self.board)
        output = [move.flag for move in moves]
        flagCounter = 0
        for flag in output:
            if flag == PROMOTION:
                flagCounter += 1
                
        self.assertEqual(flagCounter, 2)
    
    def test_generates_enpassent(self):
        # enpassent
        wPlacement = [(3, 3), (4, 3)]
        bPlacement = [(3, 2), (4, 4)]
        
        for i in range(2):
            self.setUp()
            whitePawn = Pawn(PAWN, WHITE)
            blackPawn = Pawn(PAWN, BLACK)
            
            pawn = [whitePawn, blackPawn]
            movedPawn = [blackPawn, whitePawn]
            
            self.board.add_piece(whitePawn, wPlacement[i][0], wPlacement[i][1])
            self.board.add_piece(blackPawn, bPlacement[i][0], bPlacement[i][1])
            
            self.board.set_last_piece_moved(movedPawn[i])

            moves = pawn[i].get_moves(self.board)
            output = [move.flag for move in moves]
            
            self.assertTrue(ENPASSANT in output)
                
            