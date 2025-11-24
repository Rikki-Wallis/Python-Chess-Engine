"""
Main entry point for the chess application.
-------------------------------------------

Terminal Helper Methods
"""
def print_spaces(n):
    """
    Method:
        Prints n spaces to the terminal
    """
    
    for _ in range(n):
        print(f' ')


"""
Main
"""
if __name__ == "__main__":
    """
    Imports
    """
    try:
        from src.bitboard_based_classes.bit_gui import BitGUI
        from src.bitboard_based_classes.bit_arbiter import BitArbiter
        from src.bitboard_based_classes.bitboard import BitBoard
        from src.bitboard_based_classes.move_generation.move_generator import MoveGenerator
        from src.bitboard_based_classes.engine_bitboard_game import EngineBitboardGame
        from src.bitboard_based_classes.bit_game import BitGame
        from src.bots.nuancedEvalEngine import NuancedEngine
        from src.bots.materialEvalEngine import MaterialEngine
        from src.constants.constColours import *
    except:
        from bitboard_based_classes.bit_gui import BitGUI
        from bitboard_based_classes.bit_arbiter import BitArbiter
        from bitboard_based_classes.bitboard import BitBoard
        from bitboard_based_classes.move_generation.move_generator import MoveGenerator
        from bitboard_based_classes.engine_bitboard_game import EngineBitboardGame
        from bitboard_based_classes.bit_game import BitGame
        from bots.nuancedEvalEngine import NuancedEngine
        from bots.materialEvalEngine import MaterialEngine
        from constants.constColours import *
    
    """
    Code
    """
    print_spaces(100)
    numOptions = 4
    print(f'* This version runs using a bitboard implemention*')
    
    while True:
        
        # Display menu and fetch input
        try:
            print()
            print(f'1. Play Against Yourself (or a Friend)')
            print(f'2. Play against Son of Anton - Nuanced Evaluation (slower but more accurate)') 
            print(f'3. Play against Son of Anton - Material Evaluation (faster but less accurate)')
            print(f'4. Exit') 
            option = int(input(f"Select option (1-{numOptions}): "))  
        
            if option not in range(1, numOptions + 1):
                print_spaces(100)
                print(f"Invalid option. Please enter a number between 1 and {numOptions}.")
                continue
        
        except ValueError:
            print_spaces(100)
            print(f"Invalid input. Please enter a number between 1 and {numOptions}.")
            continue
        
        print_spaces(100)
        if option == 1:
            moveGen = MoveGenerator()
            gui, arbiter, board = BitGUI(), BitArbiter(moveGen), BitBoard()
            player1, player2 = WHITE, BLACK
            game = BitGame(gui, arbiter, board, player1, player2)
        
        elif option == 2 or option == 3:
            
            evaluationType = option
            
            while True:
                try:
                    print(f'Select Colour to Play as')
                    print(f'1. White')
                    print(f'2. Black')
                    option = int(input(f'Option: '))
                
                    if option not in [1, 2]:
                        print_spaces(100)
                        print(f"Invalid option, please enter a valid option.")
                        continue
                    
                    print_spaces(100)
                    break
                
                except:
                    print_spaces(100)
                    print(f"Invalid option, please enter a valid option.")
                    continue
            
            moveGen = MoveGenerator()
            gui, arbiter, board = BitGUI(), BitArbiter(moveGen), BitBoard()
            
            if option == 1:
                humanColour = WHITE
                engineColour = BLACK
            else:
                humanColour = BLACK
                engineColour = WHITE
            
            if evaluationType == 2:    
                engine = NuancedEngine("Son of Anton", engineColour, 3, arbiter, moveGen)
            else:
                engine = MaterialEngine("Son of Anton", engineColour, 3, arbiter, moveGen)
            
            game = EngineBitboardGame(gui, arbiter, board, humanColour, engineColour, engine)
                
            
        elif option == numOptions:
            print("Exiting...")
            break
        
        
        print(r"""
                                      _._   +
                                  ,   ( )  ( )   ,
                        [UU] T\  (^)  / \  / \  (^)  /T [UU]
                     ()  ||  |\) / \  | |  | |  / \ (/|  ||  ()
                     {}  {}  {}  { }  { }  { }  { }  {}  {}  {}
                    {__}{__}{__}{___}{___}{___}{___}{__}{__}{__}
        """)
        print(f'-------------------------------------------------------------------------------------')
        print(f'                                    INSTRUCTIONS                                     ')
        print(f'-------------------------------------------------------------------------------------')
        print(f'- To close program press ESC')
        print(f'- Click and select or drag and drop to move')
        print(f'- Have fun :)')
        
        game.play_game()