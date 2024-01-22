import numpy as np

def find_paths(maze, start: tuple[int, int], end: tuple[int, int]):

    if start is None or end is None:
        raise Exception("Start or end point not set")
    
    if (not maze.layout[start]) or (not maze.layout[end]):
        return False

    def reached(pos):
        return pos == end
    
    def grope(pos, prev_pos): # * Give neighboring positions Up, Right, Down, Left 
        targeted_next_posns = []        

        vector_to_end = np.subtract(end, pos)
        vector_to_end_x = vector_to_end[1]
        vector_to_end_y = vector_to_end[0]

        direction_to_end = np.sign(vector_to_end)
        direction_to_end_x = (0, direction_to_end[1])
        direction_to_end_y = (direction_to_end[0], 0)

        if abs(vector_to_end_y) >= abs(vector_to_end_x):
            targeted_next_posns.extend([
                tuple(np.add(pos, direction_to_end_y)),
                tuple(np.add(pos, direction_to_end_x)),
            ])
        else:
            targeted_next_posns.extend([
                tuple(np.add(pos, direction_to_end_x)),
                tuple(np.add(pos, direction_to_end_y)),
            ])

        if prev_pos is not None:
            targeted_next_posns.append(tuple((np.add(pos, np.subtract(pos, prev_pos)))))

        if abs(vector_to_end_y) >= abs(vector_to_end_x):
            targeted_next_posns.extend([
                tuple(np.subtract(pos, direction_to_end_x)),
                tuple(np.subtract(pos, direction_to_end_y)),
            ])
        else:
            targeted_next_posns.extend([
                tuple(np.subtract(pos, direction_to_end_y)),
                tuple(np.subtract(pos, direction_to_end_x)),
            ])


        general_next_posns =  [ # * Only present for edge cases
            (pos[0] - 1, pos[1]),
            (pos[0] + 1, pos[1]),
            (pos[0], pos[1] + 1),
            (pos[0], pos[1] - 1),
        ]

        result = []

        for p in [*targeted_next_posns, *general_next_posns]:
            if p not in result and p != pos:
                result.append(p)

        return result
    
    def is_valid(pos: tuple[int, int]):
        if pos[0] < 0 or pos[1] < 0:
            return False
        if pos[0] >= len(maze.layout):
            return False
        if pos[1] >= len(maze.layout[0]):
            return False
        if not maze.layout[pos]:
            return False
        
        return True
    
    limit = 10 # * Stop searching after these many paths have been found
    depth_switch_limit = 10000 # * Switch to next unexplored junction, give up on this one, at this recursion depth

    from PIL import Image, ImageDraw
    image = Image.fromarray(np.array(maze.original_image)) # * Double function to copy image value
    draw = ImageDraw.Draw(image)

    def solve_pos(pos: tuple[int, int], path : list[tuple[int, int]], pos_wl: list[tuple[int, int]], path_wl : list[list[tuple[int, int]]], solutions : list[list[tuple[int, int]]] = [], current_depth = 0, main_depth = 0):
        if reached(pos):
            # print(path[-2:], pos, '|', pos_wl[:3])
            if len([*solutions, [*path, pos]]) >= limit:
                print(f"{limit} solutions found")
                return [*solutions, [*path, pos]]
            else:
                return solve_lopos(pos_wl[:], path_wl[:], [*solutions, [*path, pos]], 0, main_depth) # ? [1:] stops previous issue of all solutions being same 
        # elif pos in path:
        #     return solve_lopos(pos_wl, path_wl, solutions, depth)
        elif current_depth >= depth_switch_limit:
            return solve_lopos(pos_wl[:], path_wl[:], solutions, 0, main_depth)
        else:
            draw.point((pos[1], pos[0]), fill="blue") # * For debugging
            next_posns = list(filter(lambda p: p not in path, filter(is_valid, grope(pos, (path[-1] if len(path) > 0 else None)))))
            # if depth >= 3400:
            #     print("path:", path[-5:])
            #     print("next:", next_posns)
            if main_depth >= 20000 : # * Terminate depth limit
                print("Depth Exceeded")
                # print(path)
                print(pos)
                print([*next_posns])
                for pos in [*next_posns, *pos_wl]:
                    if pos not in path:
                        draw.point((pos[1], pos[0]), fill="pink")
                image.save('../output/debug_solve_progress.png')
                print(len(solutions), "solutions found")
                # raise Exception("BREAK")
                return solutions[:] if len(solutions) > 0 else False
            
            return solve_lopos([*next_posns, *pos_wl],
                        [*[[*path, pos] for i in range(len(next_posns))], *path_wl],
                        solutions[:], current_depth, main_depth)
    
    def solve_lopos(pos_wl: list[tuple[int, int]], path_wl : list[list[tuple[int, int]]], solutions : list[list[tuple[int, int]]], current_depth, main_depth):
        if len(pos_wl) == 0:
            print("Len: ", len(solutions))
            return solutions[:] if len(solutions) > 0 else False
        else:
            # print(pos_wl)
            return solve_pos(pos_wl[0], path_wl[0], pos_wl[1:], path_wl[1:], solutions[:], current_depth+1, main_depth+1)
        
    return solve_pos(start, [], [], [])