from PIL import Image, ImageDraw
import numpy as np
import path_finder

class Maze:
    def __init__(self, layout : list[list[int]], start : tuple[int, int] = None, end : tuple[int, int] = None, image : Image = None):
        self.layout = layout
        self.start = start
        self.end = end
        self.image = image

    # def shortest_path(self):


    def render(self, file_path = None, show_possible_paths = False) -> None:
        colorizer = {
            1: (255, 255, 255),
            0: (0,0,0),
        }

        render = Image.fromarray(np.array([[colorizer[i] for i in j] for j in self.layout], dtype=np.uint8))
        draw = ImageDraw.Draw(render)
        
        if self.start is not None:
            draw.point((self.start[1], self.start[0]), fill="lime")
        
        if self.end is not None:
            draw.point((self.end[1], self.end[0]), fill="darkgreen")

        if show_possible_paths:
            possible_path_list = self.possible_paths()
            # print(possible_path_list)
            if not possible_path_list:
                draw.point((self.end[1], self.end[0]), fill="red")
            else:
                for path in possible_path_list:
                    for pos in path[1:-1]:
                        draw.point((pos[1], pos[0]), fill="mediumspringgreen")

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
        
    @classmethod
    def from_image(cls, file_path: str, start: tuple[int, int] = None, end: tuple[int, int] = None, color_threshold = (150, 150, 150)):
        scale_factor = 20
        image =  Image.open(file_path)
        image_resized =  image.resize((image.size[0] // scale_factor, image.size[1] // scale_factor))
        image_array = list(np.asarray(image_resized))
        def flatten(pixel):
            return int(pixel[0] > color_threshold[0] and pixel[1] > color_threshold[1] and pixel[2] > color_threshold[2])
        layout = [[flatten(pixel) for pixel in row] for row in image_array]
        # print(len(layout))
        # print(image.size)
        # print(image_resized.size)
        # print(layout)
        return cls(layout = layout, start = start, end = end, image = image)
    
    def possible_paths(self) -> list[list[tuple[int, int]]]:
        return path_finder.possible_paths(self)
        
