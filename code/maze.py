import cv2
from  skimage import img_as_float
from skimage import io, color, morphology
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from scipy.ndimage import interpolation as inter

class Maze:
    def __init__(self, layout : list[list[int]], original_image : Image = None):
        self.layout = layout
        self.original_image = original_image

        # self.periphery = self.get_periphery()


    def render(self, file_path = None, show_possible_paths = False) -> None:
        # TODO
        pass

        
    @classmethod
    def from_image(cls, file_path: str, start: tuple[int, int] = None, end: tuple[int, int] = None):
        # image_raw =  np.asarray(Image.open(file_path))
        img =  io.imread(file_path)
        image = img_as_float(color.rgb2gray(img))

        print("Size:", len(img) * len(img[0]))

        # * Denoise
        blur = cv2.GaussianBlur(image,(5,5),0)

        # * Binarize
        image_binary = blur > 0.5
        # ret, imgf = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY, cv2.THRESH_OTSU)

        # TODO: Skew
        # def rotation_score(img, angle):
        #     img = [row/255 for row in img]
        #     data = inter.rotate(img, angle, reshape = False, order = 0)
        #     hist = np.sum(data, axis = 1)
        #     histogram = plt.hist(hist, bins=len(hist)//5)
        #     plt.savefig('../output/score.png')
        # rotation_score(imgf, 90)

        # * Thinning
        image_skeletonize = morphology.skeletonize(image_binary, method='lee')
        # kernel = np.ones((10,10), np.uint8)
        # erosion = cv2.erode(imgf, kernel, iterations=1)

        # * Smoothen
        image_smooth = image_skeletonize
        for i in range(len(image_skeletonize) - 1): # ! -1 is a Dirty Fix
            for j in range(len(image_skeletonize[0]) - 1): # ! -1 is a Dirty Fix
                if (i % 2 == 0 and j % 2 == 1) or 1: # TODO
                    if image_skeletonize[i,j] == 0:
                        if ((i == 0 or i == len(image_skeletonize))\
                            or (image_skeletonize[i-1, j]==255 or image_skeletonize[i+1,j]==255)) \
                            and ((j == 0 or j == len(image_skeletonize[0])) \
                                or (image_skeletonize[i, j-1]==255 or image_skeletonize[i,j+1]==255)):
                                image_smooth[i,j] = 127 # * Temporary to avoid cycle of 255
        for i in range(len(image_smooth)):
            for j in range(len(image_smooth[0])):
                if image_smooth[i,j] == 127:
                    image_smooth[i,j] = 255

                        
        
        # * Encoding
        layout = image_smooth // 255


        # return cls()

        render = Image.fromarray(layout)
        render.save('../output/render.png')


