# dimensions
WIDTH = 600  
HEIGHT = 600  
ROWS = 20
SQUARE_SIZE = WIDTH // ROWS
GAP_SIZE = 4 

# colors
SURFACE_COLOR = ('grey17')
GRID_COLOR = ('royalblue1')
SNAKE_COLOR = ('palevioletred')
APPLE_COLOR = ('green3')
HEAD_COLOR = ('deeppink')
VIRTUAL_SNAKE_COLOR = ('orangered1')

# game settings
INITIAL_SNAKE_LENGTH = 2
WAIT_SECONDS_AFTER_WIN = 5  
MAX_MOVES_WITHOUT_EATING = ROWS * ROWS * ROWS * 0  # maximum number of moves allowed without eating an apple
SNAKE_MAX_LENGTH = ROWS * ROWS - INITIAL_SNAKE_LENGTH  

# create a list of all possible positions in the grid
GRID = [[i, j] for i in range(ROWS) for j in range(ROWS)]

#helper functions
def get_neighbors(position):
    # define the four possible neighboring positions (up, down, left, right)
    neighbors = [[position[0] + 1, position[1]],
                 [position[0] - 1, position[1]],
                 [position[0], position[1] + 1],
                 [position[0], position[1] - 1]]
    in_grid_neighbors = []
    for pos in neighbors:
        if pos in GRID:
            in_grid_neighbors.append(pos)
    return in_grid_neighbors

# calculate the manhattan distance between two positions
def distance(pos1, pos2):
    x1, x2 = pos1[0], pos2[0]
    y1, y2 = pos1[1], pos2[1]
    return abs(x2 - x1) + abs(y2 - y1)

# create a dictionary mapping each position to its valid neighbors within the grid
ADJACENCY_DICT = {tuple(pos): get_neighbors(pos) for pos in GRID}
