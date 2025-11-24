"""
Imports
"""
import unittest
import time

from src.bitboard_based_classes.move_generation.move_generator import MoveGenerator
from src.bitboard_based_classes.bit_arbiter import BitArbiter
from src.bitboard_based_classes.bitboard import BitBoard
from src.bots.materialEvalEngine import MaterialEngine
from src.bots.nuancedEvalEngine import NuancedEngine
from src.constants.constColours import *
from src.constants.constFlags import *
from src.constants.constPieces import *
from tests.test_performance.fen_positions import *

"""
Classes
"""
class TestEvaluation(unittest.TestCase):
    def setUp(self):
        self.moveGenerator = MoveGenerator()
        self.arbiter = BitArbiter(self.moveGenerator)
        self.board = BitBoard()
        self.nuancedEngine = NuancedEngine("Nuanced Engine", WHITE, 3, self.arbiter, self.moveGenerator)
        self.materialEngine = MaterialEngine("Material Engine", BLACK, 3, self.arbiter, self.moveGenerator)
        

    def test_tactical_accuracy(self):
        print("----------------------------------------------------------------------------------------------")
        print("                                       TACTICAL ACCURACY                                      ")
        print(f"Depth   Position ID    Best Move    Alternate    Avoid    Nuanced    Time    Material    Time")
        print(f"---------------------------------------------------------------------------------------------")
        # Iterate over each test position
        for depth in [1,2,3,4,5,6]:
            
            total = 0
            nuancedCorrect = 0
            materialCorrect = 0
            
            for suite in [KAUFMAN_TEST_SUITE, BRATKO_KOPEC_TEST_SUITE]:
                for position in suite:
                    
                    self.board.load_fen(position['fen'])
                    
                    startNuanced = time.time()
                    nuancedMove = self.newEngine.find_best_move(self.board, depth=depth)
                    endNuanced = time.time()
                    materialMove = self.oldEngine.find_best_move(self.board, depth=depth)
                    endMaterial = time.time()
                    
                    nuancedNotation = nuancedMove.get_proper_notation()
                    materialNotation = materialMove.get_proper_notation()
                    
                    expected = None
                    alternate = None
                    avoid = None
                    if "best_move" in position:
                        expected = position["best_move"]
                    if "alternate_move" in position:
                        alternate = position["alternate_move"]
                    if "avoid_move" in position:
                        avoid = position["avoid_move"]
                    
                    if expected and nuancedNotation == expected:
                        newerCorrect += 1
                    if alternate and nuancedNotation== alternate:
                        newerCorrect += 1
                    if avoid and nuancedNotation == avoid:
                        newerCorrect -= 1
                    
                    if expected and materialNotation == expected:
                        olderCorrect += 1
                    if alternate and materialNotation== alternate:
                        olderCorrect += 1
                    if avoid and materialNotation == avoid:
                        olderCorrect -= 1
                    
                    timeNew = endNuanced - startNuanced
                    timeOld = endMaterial - endNuanced
                    total += 1
                    
                    expected = expected if expected else "-"
                    alternate = alternate if alternate else "-"
                    avoid = avoid if avoid else "-"
                    
                    print(f"{depth:<7} {position['id']:<14} {expected:<12} {alternate:<12} {avoid:<8} {nuancedNotation:<10} {timeNew:<10.3f} {materialNotation:<7} {timeOld:<10.3f}")
                    
            newAccuracy = (newerCorrect/total) * 100
            oldAccuracy = (olderCorrect/total) * 100
            
            print(f"Tactical Accuracy For New Engine: {newerCorrect}/{total} ({newAccuracy:.1f}%)")
            print(f"Tactical Accuracy For Old Engine: {olderCorrect}/{total} ({oldAccuracy:.1f}%)")

    def test_playing_strength(self):
        
        # Setup results tracking
        nuanced_results = {
            "expected_wins" : 0,
            "expected_losses" : 0,
            "expected_draws" : 0,
            "unexpected_wins" : 0,
            "unexpected_losses" : 0,
            "unexpected_draws" : 0,
        }
        material_results = {
            "expected_wins" : 0,
            "expected_losses" : 0,
            "expected_draws" : 0,
            "unexpected_wins" : 0,
            "unexpected_losses" : 0,
            "unexpected_draws" : 0,
        }
        results = {
            self.nuancedEngine.name : nuanced_results,
            self.materialEngine.name : material_results
        }
        
        # Initiate vars
        games = 0
        nuancedName = self.nuancedEngine.name
        materialName = self.materialEngine.name

        print("-----------------------------------------------------------------------------------------------")
        print("                                       TACTICAL ACCURACY                                       ")
        print(f"Position ID    Expected Result    Colour : Nuanced Result    Colour : Material Result    Moves")
        print(f"----------------------------------------------------------------------------------------------")
        
        # Iterate over each test suite
        for suite in [KAUFMAN_TEST_SUITE, BRATKO_KOPEC_TEST_SUITE]:
            # Iterate over each position
            for position in suite:
                
                if position['id'] in ["K.01", "K.02", "K.03", "K.04", "K.05", "K.06", "K.07", "K.08", "K.09", "K.10",
                                      "K.11", "K.12", "K.13", "K.14", "K.15", "K.16", "K.17", "K.18", "K.19", "K.20",
                                      "K.21", "K.22", "K.23", "K.24", "K.25",
                                      "BK.01", "BK.02", "BK.03", "BK.04", "BK.05", "BK.06", "BK.07", "BK.08", "BK.09",
                                      "BK.10"]:
                    continue
                
                # Let engines play as both colours
                for (nuancedEngineColour, materialEngineColour) in [(BLACK, WHITE), (WHITE, BLACK)]:
                    
                    # Set engine variables
                    self.nuancedEngine.colour = nuancedEngineColour
                    self.materialEngine.colour = materialEngineColour
                    
                    # Increment and set variables
                    games += 1
                    move_num = 0
                    expectedResult = position["evaluation_favours"]
                    
                    # Load position onto board
                    self.board.load_fen(position["fen"])
                    
                    # Start game loop
                    while True:
                        
                        # Check terminal conditions
                        if self.arbiter.is_in_checkmate(self.board):
                            
                            if self.board.get_colour() == nuancedEngineColour:
                                
                                if nuancedEngineColour == expectedResult:
                                    results[nuancedName]["expected_wins"] += 1
                                    results[materialName]["expected_losses"] += 1
                                    
                                else:
                                    results[nuancedName]["unexpected_wins"] += 1
                                    results[materialName]["unexpected_losses"] += 1
                                    
                                nuancedResult = "win"
                                materialResult = "loss"
                                
                            else:
                                
                                if materialEngineColour == expectedResult:
                                    results[materialName]["expected_wins"] += 1
                                    results[nuancedName]["expected_losses"] += 1
                                else:
                                    results[materialName]["unexpected_wins"] += 1
                                    results[nuancedName]["unexpected_losses"] += 1

                                nuancedResult = "loss"
                                materialResult = "win"
                            
                            break
                        
                        elif self.arbiter.is_in_fifty_move_rule(self.board) or self.arbiter.is_in_insufficient_material(self.board) or self.arbiter.is_in_repetition(self.board) or self.arbiter.is_in_stalemate(self.board):

                            if expectedResult == BOTH:
                                results[materialName]["expected_draws"] += 1
                                results[nuancedName]["expected_draws"] += 1
                            else:
                                results[materialName]["unexpected_draws"] += 1
                                results[nuancedName]["unexpected_draws"] += 1
                        
                            nuancedResult = "draw"
                            materialResult = "draw"
                            
                            break
                        
                        try:
                            # Fetch and make move
                            if self.board.get_colour() == nuancedEngineColour:
                                move = self.nuancedEngine.find_best_move(self.board, 3)
                            else:
                                move = self.materialEngine.find_best_move(self.board, 3)
                        except:
                            continue
                        
                        if move.get_flag() == PROMOTION:
                            move.make_move(QUEEN)
                        else:
                            move.make_move()
                        
                        move_num += 1
                        
                        # Sometimes, bots cannot checkmate even up material, reach conclusion then
                        if move_num >= 1000:
                            materialEval = self.materialEngine.evaluate(self.board)
                            
                            if materialEval < 0 and self.nuancedEngine.colour == BLACK:

                                if nuancedEngineColour == expectedResult:
                                    results[nuancedName]["expected_wins"] += 1
                                    results[materialName]["expected_losses"] += 1
                                else:
                                    results[nuancedName]["unexpected_wins"] += 1
                                    results[materialName]["unexpected_losses"] += 1

                                nuancedResult = "win"
                                materialResult = "loss"
                            
                            elif materialEval > 0 and self.nuancedEngine.colour == WHITE:
                                
                                if nuancedEngineColour == expectedResult:
                                    results[nuancedName]["expected_wins"] += 1
                                    results[materialName]["expected_losses"] += 1
                                else:
                                    results[nuancedName]["unexpected_wins"] += 1
                                    results[materialName]["unexpected_losses"] += 1
                                
                                nuancedResult = "win"
                                materialResult = "loss"
                                
                            elif materialEval < 0 and self.nuancedEngine.colour == BLACK:
                                
                                if materialEngineColour == expectedResult:
                                    results[materialName]["expected_wins"] += 1
                                    results[nuancedName]["expected_losses"] += 1
                                else:
                                    results[materialName]["unexpected_wins"] += 1
                                    results[nuancedName]["unexpected_losses"] += 1
                                
                                nuancedResult = "loss"
                                materialResult = "win"
                                
                            elif materialEval > 0 and self.nuancedEngine.colour == WHITE:
                                
                                if materialEngineColour == expectedResult:
                                    results[materialName]["expected_wins"] += 1
                                    results[nuancedName]["expected_losses"] += 1
                                else:
                                    results[materialName]["unexpected_wins"] += 1
                                    results[nuancedName]["unexpected_losses"] += 1

                                nuancedResult = "loss"
                                materialResult = "win"
                                
                            else:
                                
                                if expectedResult == BOTH:
                                    results[materialName]["expected_draws"] += 1
                                    results[nuancedName]["expected_draws"] += 1
                                else:
                                    results[materialName]["unexpected_draws"] += 1
                                    results[nuancedName]["unexpected_draws"] += 1
                                    
                                nuancedResult = "draw"
                                materialResult = "draw"
                            
                            break
                    
                    print(f"{position['id']:<14} {expectedResult:<18} {nuancedEngineColour}  : {nuancedResult:<18} {materialEngineColour} : {materialResult:<18} {move_num}")
        
        print("-----------------------------------------------------------------------------------------------")
        print(f"Nuanced engine won {results[nuancedName]["expected_wins"]} + {results[nuancedName]["unexpected_wins"]} games, lost {results[nuancedName]["expected_losses"]} + {results[nuancedName]["unexpected_losses"]}, and drew {results[nuancedName]["expected_draws"]} + {results[nuancedName]["unexpected_draws"]}")
        print(f"---Expected---")
        print(f"wins: {results[nuancedName]["expected_wins"]}")
        print(f"losses: {results[nuancedName]["expected_losses"]}")
        print(f"draws: {results[nuancedName]["expected_draws"]}")
        print(f" ")
        print(f"---Unexpected---")
        print(f"wins: {results[nuancedName]["unexpected_wins"]}")
        print(f"losses: {results[nuancedName]["unexpected_losses"]}")
        print(f"draws: {results[nuancedName]["unexpected_draws"]}")
        print(f" ")
        print(f" ")
        print(f"Material engine won {results[materialName]["expected_wins"]} + {results[materialName]["unexpected_wins"]} games, lost {results[materialName]["expected_losses"]} + {results[materialName]["unexpected_losses"]}, and drew {results[materialName]["expected_draws"]} + {results[materialName]["unexpected_draws"]}")
        print(f"---Expected---")
        print(f"wins: {results[materialName]["expected_wins"]}")
        print(f"losses: {results[materialName]["expected_losses"]}")
        print(f"draws: {results[materialName]["expected_draws"]}")
        print(f" ")
        print(f"---Unexpected---")
        print(f"wins: {results[materialName]["unexpected_wins"]}")
        print(f"losses: {results[materialName]["unexpected_losses"]}")
        print(f"draws: {results[materialName]["unexpected_draws"]}")
