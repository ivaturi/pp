# Rules of Conway's game of life:
# 1. If a cell is ON and has fewer than 2 ON neighbors, it turns OFF
# 2. If a cell is ON and has 2 or 3 ON neighbors, it remains ON
# 3. If a cell is ON and has >3 ON neighbors, it turns OFF
# 4. If a cell is OFF and has 3 ON neighbors, it turns ON

# import necessary modules
import numpy as np
import matplotlib.pyplot as plot
import matplotlib.animation as anim

# setup values
ON = 255
OFF = 0
states = [ON, OFF]


def randomGrid(n):
    """
    Returns a grid of n x n random values
    """
    values = np.random.choice(states, n*n, p=[0.2, 0.8])
    return values.reshape(n, n)

# We're setting up a pattern here that we can insert at a
# specified row and column, so we can define an initial
# condition to match a pattern
# (instead of filling the grid with a random set of values)
def addGlider(col, row, grid):
    """
    Adds a glider with top left at (row, col)
    (A glider patter preserves its shape as it moves steadily
    across the grid)
    """
    # define the glider pattern
    glider = np.array([[0, 0, 255],
                       [255, 0, 255],
                       [0, 0, 255]])
    # Assign the glider a position in the grid
    # according to the requested (col, row)
    grid[col:col+3, row:row+3] = glider
