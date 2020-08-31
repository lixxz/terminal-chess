# ANSI Escape Sequences
RESET = "\u001b[0m"
# Using cyan for white
WHITE = "\u001b[36m"
# Using red for black
BLACK = "\u001b[31m"

# Building blocks for drawing the grid
SPACE_AND_UNDERSCORE = list((" " + "_" * 5) * 8)
PIPE_AND_SPACE = list(("|" + " " * 5 + "|") + (" " * 5 + "|") * 7)
PIPE_AND_UNDERSCORE = list(("|" + "_" * 5 + "|") + ("_" * 5 + "|") * 7)

# Mapping squares(a2, h8 etc) to underlying grid coordinates
RANKS = '12345678'
FILES = 'abcdefgh'
ROWS = [23, 20, 17, 14, 11, 8, 5, 2]
COLUMNS = [3, 9, 15, 21, 27, 33, 39, 45]

GRID_CORDS = [(r, c) for c in COLUMNS for r in ROWS]
CHESS_SQUARES = [f + r for f in FILES for r in RANKS]
SQUARE_TO_CORD_MAPPING = dict(zip(CHESS_SQUARES, GRID_CORDS))

# Files for the grid
FILES_DRAW = list(46 * " ")
for i, c in enumerate(COLUMNS):
    FILES_DRAW[c] = FILES[i]

# Ranks for the grid
PIPE_AND_SPACE_8 = PIPE_AND_SPACE[:]
PIPE_AND_SPACE_8.append(" 8")
PIPE_AND_SPACE_7 = PIPE_AND_SPACE[:]
PIPE_AND_SPACE_7.append(" 7")
PIPE_AND_SPACE_6 = PIPE_AND_SPACE[:]
PIPE_AND_SPACE_6.append(" 6")
PIPE_AND_SPACE_5 = PIPE_AND_SPACE[:]
PIPE_AND_SPACE_5.append(" 5")
PIPE_AND_SPACE_4 = PIPE_AND_SPACE[:]
PIPE_AND_SPACE_4.append(" 4")
PIPE_AND_SPACE_3 = PIPE_AND_SPACE[:]
PIPE_AND_SPACE_3.append(" 3")
PIPE_AND_SPACE_2 = PIPE_AND_SPACE[:]
PIPE_AND_SPACE_2.append(" 2")
PIPE_AND_SPACE_1 = PIPE_AND_SPACE[:]
PIPE_AND_SPACE_1.append(" 1")

# Possible sides
SIDES = ['w', 'b']
