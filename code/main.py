import time
import sys

from maze import Maze

sys.setrecursionlimit(3500000)

maze = Maze.from_image('../source_images/stock_maze_2.webp')

# print(end - start)

maze_image = maze.render('../output/render.png')

# maze_solutions = (maze.render_possible_paths((50, 366), (60, 366), '../output/solution.png'))
maze_solutions = (maze.render_possible_paths((50, 366), (750, 432), '../output/solution.png'))
# maze_solutions = (maze.render_possible_paths((3, 2), (960, 1299), '../output/solution.png'))