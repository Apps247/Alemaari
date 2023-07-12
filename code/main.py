from maze import Maze
import time

start = time.time()

maze = Maze.from_image('../source_images/stock_maze_2.webp')

end = time.time()

print(end - start)

maze.render('../output/render.png')