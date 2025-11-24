try:
    from src.constants.constFilesAndRanks import *
except:
    from constants.constFilesAndRanks import *
    
    
# Files and Ranks
FILES = [A_FILE, B_FILE, C_FILE, D_FILE, E_FILE, F_FILE, G_FILE, H_FILE]
RANKS = [RANK1, RANK2, RANK3, RANK4, RANK5, RANK6, RANK7, RANK8]

# Central insentive
CENTER = (RANK2 | RANK3 | RANK4 | RANK5 | RANK6 | RANK7) & (C_FILE | D_FILE | E_FILE | F_FILE)