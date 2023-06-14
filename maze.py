from PIL import Image, ImageDraw
import numpy as np


class Maze:
    def __init__(self, layout : list[list[int]], start : tuple[int, int] = None, end : tuple[int, int] = None):
        self.layout = layout
        self.start = (start[1], start[0]) if start is not None else None
        self.end = (end[1], end[0]) if end is not None else None

    # def shortest_path(self):


    def render(self, file_path = None) -> None:
        colorizer = {
            1: (255, 255, 255),
            0: (0,0,0)
        }

        render = Image.fromarray(np.array([[colorizer[i] for i in j] for j in self.layout], dtype=np.uint8))
        draw = ImageDraw.Draw(render)
        
        if self.start is not None:
            print(self.start)
            draw.point(self.start, fill="lime")
        
        if self.end is not None:
            draw.point(self.end, fill="darkgreen")

        if file_path is not None:
            render.save(file_path)
        else:
            render.show()


    @classmethod
    def from_string(cls, string : str, dimensions : tuple[int, int], start : tuple[int, int] = None, end : tuple[int, int] = None):
        # * String to Maze Layout
        length = len(string.strip().split(' '))
        height = dimensions[0]
        width = dimensions[1]
        if length != height * width:
            raise Exception("Input string does not match dimensions")
        else:
            layout = [list(map(int, map(lambda s: s.strip(), string.strip().split(' '))))[i*height : i*height + width]
                for i in range(length // height)]


        return cls(layout = layout, start = start, end = end)
        
