from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder


matrix = [
    [1, 1, 1, 1, 1],
    [1, 0, 1, 1, 0],
    [1, 1, 1, 1, 1],
]

# create a grid
grid = Grid(matrix=matrix)

# create a start and end cell
start = grid.node(0, 0)
end = grid.node(4, 2)

# create a finder with a movement style
finder = AStarFinder()

# find the path
path, runs = finder.find_path(start, end, grid)

# print the result
print(path)
