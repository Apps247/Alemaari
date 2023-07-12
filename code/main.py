from maze import Maze
import time

maze = Maze.from_image('../source_images/city.webp')

# print(end - start)

maze_image = maze.render('../output/render.png')

maze_solutions = (maze.render_possible_paths((3, 2), (8, 3), '../output/solution.png'))