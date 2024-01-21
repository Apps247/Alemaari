import time
import sys

from maze import Maze

sys.setrecursionlimit(3500000)

# maze = Maze.from_image('../source_images/stock_maze.jpg')
# maze = Maze.from_image('../source_images/stock_maze_2.webp')
maze = Maze.from_image('../source_images/OIP.jpeg')

# print(end - start)

maze_image = maze.render('../output/render.png')

# maze_solutions = (maze.render_possible_paths((202, 9), (202, 602), '../output/solution.png'))
# maze_solutions = (maze.render_possible_paths((50, 366), (750, 432), '../output/solution.png'))
# maze_solutions = (maze.render_possible_paths((3, 66), (347, 249), '../output/solution.png'))
maze_solutions = (maze.render_possible_paths((9, 83), (285, 225), '../output/solution.png'))
