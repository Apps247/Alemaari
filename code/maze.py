import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from scipy.ndimage import interpolation as inter

class Maze:
    def __init__(self, layout : list[list[int]], start : tuple[int, int] = None, end : tuple[int, int] = None, image : Image = None):
        self.layout = layout
        self.start = start
        self.end = end
        self.image = image

        # self.periphery = self.get_periphery()

    

    def render(self, file_path = None, show_possible_paths = False) -> None:
        # TODO
        pass

        
    @classmethod
    def from_image(cls, file_path: str, start: tuple[int, int] = None, end: tuple[int, int] = None):
        # image_raw =  np.asarray(Image.open(file_path))
        img =  cv2.imread(file_path)
        
        print("Size:", len(img) * len(img[0]))

        # * Denoise
        blur = cv2.GaussianBlur(img,(5,5),0)

        # * Binarize
        ret, imgf = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY, cv2.THRESH_OTSU)

        # TODO: Skew
        # def rotation_score(img, angle):
        #     img = [row/255 for row in img]
        #     data = inter.rotate(img, angle, reshape = False, order = 0)
        #     hist = np.sum(data, axis = 1)
        #     histogram = plt.hist(hist, bins=len(hist)//5)
        #     plt.savefig('../output/score.png')
        # rotation_score(imgf, 90)

        # * Thinning
        kernel = np.ones((10,10), np.uint8)
        erosion = cv2.erode(imgf, kernel, iterations=1)

        print("Size:", len(imgf))
        
        render = Image.fromarray(erosion)
        render.save('../output/render.png')


        # return cls(layout = layout, start = start, end = end, image = image)