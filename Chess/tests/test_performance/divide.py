"""
Imports
"""
import subprocess
import re
import os
import sys
import time

# Add the project root to the path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from src.bitboard_based_classes.bit_arbiter import BitArbiter
from src.bots.nuancedEvalEngine import NuancedEngine
from src.bitboard_based_classes.bitboard import BitBoard
from src.bitboard_based_classes.move_generation.move_generator import MoveGenerator
from src.constants.constPieces import *
from src.constants.constFlags import *
from src.constants.constColours import *
PROMOTION, BISHOP, KNIGHT, ROOK

def parse_reference_perft(input_str):
    """
    Parse reference perft output into a dictionary.
    Expected format: "e2e4: 13160"
    """
    reference = {}
    lines = input_str.strip().split('\n')
    for line in lines:
        line = line.strip()
        if ':' in line:
            move, count = line.split(':')
            reference[move.strip()] = int(count.strip())
    return reference

def divide_interactive(engine, board, depth, selectedMove=None):
    """
    Interactive divide function that lets you manually explore move trees.

    At each level:
    - Shows all root moves and their node counts.
    - Shows difference from reference perft (if provided).
    - Lets you type a move (e.g., e2e4) to dive deeper.
    - Or type 'back' to undo, 'exit' to quit.
    """
    if depth <= 0:
        print("Depth must be positive")
        return

    print(f"\n{'='*60}")
    print(f"DIVIDE (depth {depth}) - {'White' if board.get_colour() == WHITE else 'Black'} to move")
    print(f"{'='*60}\n")

    results = {}
    total_nodes = 0
    moves = engine.moveGenerator.get_all_moves(board)
    moves = engine.arbiter.filter_moves(board, moves, board.get_colour())
    pieceToChar = {
        QUEEN : 'q',
        BISHOP : 'b',
        KNIGHT : 'n',
        ROOK : 'r'
    }

    for move in moves:
        if move.isCheck:
            continue
        
        if move.get_flag() == PROMOTION:
            for piece in [BISHOP, QUEEN, KNIGHT, ROOK]:
                move.make_move(promotionChoice=piece)
                nodes = 1 if depth == 0 else engine.perft(board, depth - 1)
                move.undo_move()
                
                move_str = f"{move.get_move_notation()}{pieceToChar[piece]}"
                results[move_str] = nodes
                total_nodes += nodes
        else:
            move.make_move()
            nodes = 1 if depth == 0 else engine.perft(board, depth - 1)
            move.undo_move()
            
            move_str = move.get_move_notation()
            results[move_str] = nodes
            total_nodes += nodes

        print(f"{move.pieceType} {move_str}: {nodes}")
        #print(f"{str(move)}")
        

    print(f"\nTotal nodes: {total_nodes}")
    print(f"{'='*60}")

    # Ask if user wants to compare with reference
    compare = input("\nCompare with reference engine? (y/n): ").strip().lower()
    reference_perft = {}
    
    if compare == 'y':
        print("\nPaste reference perft output (format: 'move: count' per line).")
        print("When done, enter an empty line:\n")
        
        reference_lines = []
        while True:
            line = input()
            if line.strip() == "":
                break
            reference_lines.append(line)
        
        if reference_lines:
            reference_perft = parse_reference_perft('\n'.join(reference_lines))
            
            print(f"\n{'='*60}")
            print("COMPARISON RESULTS")
            print(f"{'='*60}\n")
            
            all_moves = set(results.keys()) | set(reference_perft.keys())
            mismatches = []
            
            for move_str in sorted(all_moves):
                my_count = results.get(move_str, 0)
                ref_count = reference_perft.get(move_str, 0)
                diff = my_count - ref_count
                
                if diff != 0:
                    status = "X MISMATCH"
                    mismatches.append(move_str)
                else:
                    status = "> correct"
                
                if move_str not in results:
                    print(f"{move_str}: MISSING in your engine (ref: {ref_count}) {status}")
                    #print(f"{str(move)}")
                elif move_str not in reference_perft:
                    print(f"{move_str}: EXTRA in your engine ({my_count}) {status}")
                    #print(f"{str(move)}")
                else:
                    print(f"{move_str}: {my_count} (ref: {ref_count}, diff: {diff:+}) {status}")
                    #print(f"{str(move)}")
                
            
            print(f"\n{'='*60}")
            print(f"Total mismatches: {len(mismatches)}")
            if mismatches:
                print(f"Problem moves: {', '.join(mismatches)}")
            print(f"{'='*60}")

    # Ask user for next step
    while True:
        choice = input("\nEnter move to drill into, 'back' to undo, or 'exit' to quit: ").strip().lower()

        if choice == 'exit':
            print("Exiting interactive divide.")
            return

        if choice == 'back':
            print("Going back one level...")
            return

        if choice not in results:
            print("Invalid move. Try again.")
            continue

        # Make the chosen move and go deeper
        selected_move = next((m for m in moves if choice.startswith(m.get_move_notation())), None)

        if not selected_move:
            print("Could not find that move.")
            continue

        selected_move.make_move()
        divide_interactive(engine, board, depth - 1)
        selected_move.undo_move()
        return



if __name__ == "__main__":
    board = BitBoard()
    board.setup_kiwipete()
    moveGenerator = MoveGenerator()
    arbiter = BitArbiter(moveGenerator)
    engine = NuancedEngine("Divide Tester", WHITE, 4, arbiter, moveGenerator)

    print("\nInteractive divide tool started.")
    divide_interactive(engine, board, depth=4)