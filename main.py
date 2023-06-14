from maze import Maze

maze1_string = '''
1 1 1 1 1 1
0 0 1 0 0 0
0 1 1 0 1 1
1 1 0 1 1 0
0 1 1 1 0 0
0 1 0 1 0 1
'''.replace('\n', ' ')

maze1_dimensions = (6, 6) # (height, width)

maze1 = (Maze.from_string(maze1_string, maze1_dimensions, start=(0,1), end = (3,4)))
print(maze1)


    
maze1.render('new.png')