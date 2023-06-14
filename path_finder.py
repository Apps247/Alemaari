from maze import Maze

def possible_paths(maze: Maze):
    if maze.start is None or maze.end is None:
        raise Exception("Start or end point not set")
    
    if not maze.layout[maze.start[0]][maze.start[1]]:
        return False
    
    if not maze.layout[maze.end[0]][maze.end[1]]:
        return False
    
    return search(maze)


def search(maze: Maze):
    def reached(pos):
        return pos == maze.end
    
    # def grope(pos): # * Give neighboring positions Up, Right, Down, Left 


    def solve_pos(pos: tuple[int, int], path : list[tuple[int, int]], pos_wl: list[tuple[int, int]], path_wl : list[list[tuple[int, int]]], solutions : list[list[tuple[int, int]]]):
        if reached(pos):
            return solve_lopos(pos_wl, path_wl, solutions.append(path.append(pos)))
        elif pos in path:
            return solve_lopos(pos_wl, path_wl, solutions)
        else:
            next_posns = filter(is_valid, grope(pos))
            solve_lopos(pos_wl.extend(next_posns),
                        path_wl.extend([path.append(pos) for i in range(next_posns)]),
                        solutions)
    
    def solve_lopos(pos_wl: list[tuple[int, int]], path_wl : list[list[tuple[int, int]]], solutions : list[list[tuple[int, int]]]):
        if len(pos_wl) == 0:
            return solutions if len(solutions) > 0 else False
        else:
            return solve_pos(pos_wl[0], path_wl=[0], )
        
