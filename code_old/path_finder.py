# from maze import Maze
import numpy as np

def possible_paths(maze):
    if maze.start is None or maze.end is None:
        raise Exception("Start or end point not set")
    
    if not maze.layout[maze.start[0]][maze.start[1]]:
        return False
    
    if not maze.layout[maze.end[0]][maze.end[1]]:
        return False
    
    return search(maze)


def search(maze):
    def reached(pos):
        return pos == maze.end
    
    def grope(pos, prev_pos): # * Give neighboring positions Up, Right, Down, Left 
        next_posns = []        

        vector_to_end = np.subtract(maze.end, pos)
        vector_to_end_x = vector_to_end[1]
        vector_to_end_y = vector_to_end[0]

        direction_to_end = np.sign(vector_to_end)
        direction_to_end_x = (0, direction_to_end[1])
        direction_to_end_y = (direction_to_end[0], 0)

        if abs(vector_to_end_y) >= abs(vector_to_end_x):
            next_posns.extend([
                tuple(np.add(pos, direction_to_end_y)),
                tuple(np.add(pos, direction_to_end_x)),
            ])
        else:
            next_posns.extend([
                tuple(np.add(pos, direction_to_end_x)),
                tuple(np.add(pos, direction_to_end_y)),
            ])

        if prev_pos is not None:
            next_posns.append(tuple((np.add(pos, np.subtract(pos, prev_pos)))))

        if abs(vector_to_end_y) >= abs(vector_to_end_x):
            next_posns.extend([
                tuple(np.subtract(pos, direction_to_end_x)),
                tuple(np.subtract(pos, direction_to_end_y)),
            ])
        else:
            next_posns.extend([
                tuple(np.subtract(pos, direction_to_end_y)),
                tuple(np.subtract(pos, direction_to_end_x)),
            ])


        
        next_posns.extend([pos for pos in [
            (pos[0] - 1, pos[1]),
            (pos[0] + 1, pos[1]),
            (pos[0], pos[1] + 1),
            (pos[0], pos[1] - 1),
        ] if pos not in next_posns])
    
        return next_posns
    
    def is_valid(pos: tuple[int, int]):
        if pos[0] < 0 or pos[1] < 0:
            return False
        if pos[0] >= len(maze.layout):
            return False
        if pos[1] >= len(maze.layout[0]):
            return False
        if not maze.layout[pos[0]][pos[1]]:
            return False
        
        return True
    from PIL import Image, ImageDraw
    image = Image.open('stock_maze_2.webp')
    image_scaled = image.resize((image.size[0]//20, image.size[1]//20))
    draw = ImageDraw.Draw(image_scaled)
    def solve_pos(pos: tuple[int, int], path : list[tuple[int, int]] = [], pos_wl: list[tuple[int, int]] = [], path_wl : list[list[tuple[int, int]]] = [], tried : list[tuple[int, int]] =[], solutions : list[list[tuple[int, int]]] = [], depth = 0):
        #TODO: remove tried
        if reached(pos):
            # print(len([*solutions, [*path, pos]]))
            # print([*solutions, [*path, pos]])
            # return [*solutions, [*path, pos]] if len([*solutions, [*path, pos]]) > 0 else False
            return solve_lopos(pos_wl, path_wl, [], [*solutions, [*path, pos]], depth)
        # elif pos in tried:
        #     return solve_lopos(pos_wl, path_wl, solutions, tried, depth)
        elif pos in path:
            return solve_lopos(pos_wl, path_wl, [*tried, pos], solutions, depth)
        else:
            draw.point((pos[1], pos[0]), fill="pink")
            if depth > 10000 and depth % 100 == 0: 
                print('Depth:', depth)
            if depth > 30000: 
                print(pos)
                print(len(pos_wl))
                print(pos_wl)
                image_scaled.save('debug_solve_progress.png')
                print(len(solutions))
                # raise Exception("BREAK")
                return solutions if len(solutions) > 0 else False
            next_posns = list(filter(lambda pos: pos not in path, filter(is_valid, grope(pos, (path[-1] if len(path) > 0 else None)))))
            return solve_lopos([*next_posns, *pos_wl],
                        [*[[*path, pos] for i in range(len(next_posns))], *path_wl],
                        [*tried, pos],
                        solutions, depth)
    
    def solve_lopos(pos_wl: list[tuple[int, int]], path_wl : list[list[tuple[int, int]]], tried : list[tuple[int, int]], solutions : list[list[tuple[int, int]]], depth):
        if len(pos_wl) == 0:
            print("Len: ", len(solutions))
            return solutions if len(solutions) > 0 else False
        else:
            return solve_pos(pos_wl[0], path_wl[0], pos_wl[1:], path_wl[1:], tried, solutions, depth+1)
        
    return solve_pos(maze.start)
        
