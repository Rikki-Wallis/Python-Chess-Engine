"""
Imports
"""
import timeit
import time
import unittest
from unittest.mock import patch
from memory_profiler import memory_usage
import cProfile
import psutil
import threading

from src.bots.bot import Bot
from src.bots.nuancedEvalEngine import NuancedEngine
from src.bots.materialEvalEngine import MaterialEngine
from src.array_based_classes.array_arbiter import ArrayArbiter
from src.array_based_classes.array_board import ArrayBoard
from src.bitboard_based_classes.bit_arbiter import BitArbiter
from src.bitboard_based_classes.bitboard import BitBoard
from src.bitboard_based_classes.move_generation.move_generator import MoveGenerator
from src.constants.constColours import *

"""
Tests
"""
# To run tests: python -m unittest tests.test_performance 
class TestPerformance(unittest.TestCase):
    
    def setUp(self):
        """
        Method:
            Sets up the board, arbiter and engine to be tested
        """
        self.arrayArbiter = ArrayArbiter()
        self.arrayBoard = ArrayBoard()
        self.arrayEngine = Bot("Son of Array", WHITE, 3, self.arrayArbiter, self.arrayArbiter)
        
        self.moveGen = MoveGenerator()
        self.bitArbiter = BitArbiter(self.moveGen)
        self.bitBoard = BitBoard()
        self.nuancedEngine = NuancedEngine("Son of Nuance", WHITE, 3, self.bitArbiter, self.moveGen)
        self.materialEngine = MaterialEngine("Son of Material", WHITE, 3, self.bitArbiter, self.moveGen)
        
        # Choose which bot to test
        self.engine = self.materialEngine
        self.board = self.bitBoard
        self.arbiter = self.bitArbiter
        

    """-------------------------------------------------- Move Generation Correctness --------------------------------------------------"""
    
    
    def test_perft_with_perft(self):
        """
        Method:
            Compares move generation against
            known perft results. Uses the perft
            method in the engine so that moves
            can be found quicker
        """
        # {depth : nodes}
        perftCounts = {
            1: 20,
            2: 400,
            3: 8902,
            4: 197281,
            #5: 4865609
        }
        
        print(f'\n-----------------------------------------------------------')
        print(f'               PERFT WITH PERFT TEST RESULTS                 ')
        print(f'depth       expected        actual        time        pos/sec')
        print(f'-----------------------------------------------------------  ')
        
        total_start = time.time()
        total_nodes = 0
        
        for depth, expected_nodes in perftCounts.items():
            
            start = time.time()
            actual_nodes = self.engine.perft(self.board, depth)
            end = time.time()
            
            elapsed = end - start
            pos_per_sec = expected_nodes / elapsed if elapsed > 0 else 0
            
            # Assert correctness
            self.assertEqual(expected_nodes, actual_nodes, 
                            f"Depth {depth}: expected {expected_nodes}, got {actual_nodes}")
            
            total_nodes += actual_nodes
            
            # Print results
            print(f'{depth}           {expected_nodes:<12,} {actual_nodes:<12,} {elapsed:>6.3f}s     {pos_per_sec:>12,.0f}')
        
        total_end = time.time()
        total_elapsed = total_end - total_start
        total_pos_per_sec = total_nodes / total_elapsed if total_elapsed > 0 else 0
        
        print(f'-----------------------------------------------------------')
        print(f'Total time: {total_elapsed:.3f}s')
        print(f'Total nodes: {total_nodes:,}')
        print(f'Average: {total_pos_per_sec:,.0f} positions/second')


    def test_perft_with_search(self):
        """
        Method:
            Compares move generation against
            known perft results. Uses the 
            search function of the engine
        """
        # {depth : nodes}
        perftCounts = {
            1 : 20,
            2 : 400,
            3 : 8902,
            4 : 197281,
            5 : 4865609,
            6 : 119060324,
        }
        
        print(f'\n-----------------------------------------------------------')
        print(f'               PERFT WITH SEARCH TEST RESULTS                ')
        print(f'depth       expected        actual        time        pos/sec')
        print(f'-----------------------------------------------------------  ')
        
        count = 1
        for depth, nodes in perftCounts.items():
            self.setUp()
            with patch.object(self.engine, 'find_best_move', wraps=self.engine.find_best_move) as mock_search:
                start = time.time()
                self.engine.find_best_move(self.board, depth)
                end = time.time()
                
                #self.assertEqual(mock_search.call_count, count + nodes)
                count += nodes
                
                print()
            
            end = time.time()
            print(f'{depth}           {count:<12,}    {mock_search.call_count:<12,} {(end-start):>6.3f}s{(nodes/(end-start)):>12,.0f}')
        
        print(f'-----------------------------------------------------------')
    
    
    """-------------------------------------------------- Specific Function Performance --------------------------------------------------"""
    
    
    def test_function_performance(self):
        """
        Method:
            Runs all performance tests for specific functions
        """
        print(f'\n-----------------------------------------------------------')
        print(f'                  FUNCTION TEST RESULTS                      ')
        print(f'no. calls       time             time/call       function    ')
        print(f'-----------------------------------------------------------  ')
        noCalls = 1000
        
        # Get times for each function
        getAllMovesTime = timeit.timeit(lambda: self.engine.moveGenerator.get_all_moves(self.board), number=noCalls)
        getAllAttacksTime = timeit.timeit(lambda: self.engine.moveGenerator.get_all_attacks(self.board, self.board.get_colour()), number=noCalls)
        evaluateTime = timeit.timeit(lambda: self.engine.evaluate(self.board), number=noCalls)
        checkmateTime = timeit.timeit(lambda: self.engine.arbiter.is_in_checkmate(self.board), number=noCalls)
        stalemateTime = timeit.timeit(lambda: self.engine.arbiter.is_in_stalemate(self.board), number=noCalls)
        insufficientMaterialTime = timeit.timeit(lambda: self.engine.arbiter.is_in_insufficient_material(self.board), number=noCalls)
        fiftyMoveRuleTime = timeit.timeit(lambda: self.engine.arbiter.is_in_fifty_move_rule(self.board), number=noCalls)
        repetitionTime = timeit.timeit(lambda: self.engine.arbiter.is_in_repetition(self.board), number=noCalls)
        generateMaterialCountTime = timeit.timeit(lambda: self.engine.arbiter.generate_material_count(self.board), number=noCalls)
        
        # Add to list for easy printing
        times = [("get_all_moves", getAllMovesTime), ("get_all_attacks", getAllAttacksTime), ("evaluate", evaluateTime), ("is_in_checkmate", checkmateTime), 
                ("is_in_stalemate", stalemateTime), ("is_in_insufficient_material", insufficientMaterialTime), ("is_in_fifty_move_rule", fiftyMoveRuleTime), 
                ("is_in_repetition", repetitionTime), ("generate_material_count", generateMaterialCountTime)]
        
        for functionName, time in times:
            print(f'{noCalls}          {time:.10f}    {time/noCalls:.10f}       {functionName:15}')
        
        print(f'-----------------------------------------------------------')


    """-------------------------------------------------- System Resource Performance --------------------------------------------------""" 

    
    def test_system_resources(self):
        """
        Method:
            Tests the system resources used by the search function    
        """
        print(f'\n-----------------------------------------------------------')
        print(f'                SYSTEM RESOURCE TEST RESULTS                 ')
        print(f'resource                measurement                unit      ')
        print(f'-----------------------------------------------------------  ')

        # Grab memory usage and CPU utulisation
        memUsage = memory_usage((self.engine.find_best_move, (self.board, 3)), max_usage=True)*1.049 # Convert to MB
        cpuUsage = self.get_cpu_utulization()
        
        # Add results to list and print them
        resources = [("Memory", memUsage, "MB"), ("CPU   ", cpuUsage, "%")]
        for resource, measurement, unit in resources:
            print(f'{resource}                  {measurement:.11f}             {unit}')
        
        print(f'-----------------------------------------------------------')


    def get_cpu_utulization(self):
        """
        Method:
            Obtains the CPU utulization during a search
        """
        # Store CPU usage samples
        cpuSamples = []
        
        # Function to monitor CPU usage
        def monitor_cpu():
            process = psutil.Process()
            while monitoring:
                cpuSamples.append(process.cpu_percent(interval=0.1))
        
        # Function to run the search
        def profile_search():
            self.engine.find_best_move(self.board, depth=3)
        
        # Start monitoring
        monitoring = True
        monitorThread = threading.Thread(target=monitor_cpu)
        monitorThread.start()
        
        # Run search
        profile_search()
        
        # Stop monitoring
        monitoring = False
        monitorThread.join()
        
        # Calculate average CPU usage
        return sum(cpuSamples) / len(cpuSamples)        


    """ -------------------------------------------------- Bottleneck Analysis --------------------------------------------------"""


    def test_profiling(self):
        """
        Method:
            Profiles the search function to find bottlenecks
        """
        print(f'\n-----------------------------------------------------------')
        print(f'                  BOTTLENECK TEST RESULTS                    ')
        print(f'-----------------------------------------------------------  ')

        def profile_search():
            self.engine.find_best_move(self.board, depth=2)
        
        # Profile the callable
        profiler = cProfile.Profile()
        profiler.enable()
        profile_search()
        profiler.disable()
        
        profiler.print_stats(sort='time')
