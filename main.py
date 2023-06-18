from maze import Maze

import sys
sys.setrecursionlimit(3500000)

import gc

# maze1_string = '''
# 1 0 0 0 0
# 1 0 1 1 0
# 1 0 0 1 0
# 1 1 1 1 1
# 0 1 0 0 1
# '''.replace('\n', ' ')

maze1_dimensions = (5, 5) # (height, width)

maze1 = (Maze.from_image('stock_maze_2.webp',start=(3,18), end = (35,21)))
    
maze1.render('maze.png')
maze1.render('solution.png', show_possible_paths=True)

# for path in maze1.possible_paths():
    # print(path)
#

gc.collect()