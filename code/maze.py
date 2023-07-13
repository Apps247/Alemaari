import cv2
from  skimage import img_as_float
from skimage import io, color, morphology
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import interpolation as inter

import time

import path_finder

class Maze:
    def __init__(self, layout : np.ndarray[int, int], original_image : Image = None):
        self.layout = layout
        self.original_image = original_image

        # self.periphery = self.get_periphery()


    def render(self, file_path = None) -> None:
        render = Image.fromarray(self.layout * 255)
        if file_path is not None: 
            render.save(file_path)
        return render


        
    @classmethod
    def from_image(cls, file_path: str, start: tuple[int, int] = None, end: tuple[int, int] = None):
        start = time.time()

        img =  io.imread(file_path)
        original_image = Image.fromarray(img)
        image = img_as_float(color.rgb2gray(img))

        n_rows, n_cols = image.shape
        print(f"Size: {n_rows} * {n_cols} = {n_rows * n_cols}")

        print(f"Read: {time.time() - start}")

        # * Denoise
        blur = cv2.GaussianBlur(image,(5,5),0)
        print(f"Denoise: {time.time() - start}")

        # * Binarize
        # if np.average(blur)
        image_binary = blur > 0.9
        # ret, imgf = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY, cv2.THRESH_OTSU)
        print(f"Binarize: {time.time() - start}")

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
        print(f"Skeletonize: {time.time() - start}")
        # kernel = np.ones((10,10), np.uint8)
        # erosion = cv2.erode(imgf, kernel, iterations=1)

        # * Smoothen

        image_smooth = image_skeletonize // 255

        empty_row = image_skeletonize[0] * 0
        empty_col = image_skeletonize[:, [0]] * 0

        path_is_below = np.vstack((image_skeletonize[1:, :], empty_row))
        path_is_above = np.vstack((empty_row, image_skeletonize[:-1, :])) 

        path_is_right = np.hstack((image_skeletonize[:, 1:], empty_col))
        path_is_left = np.hstack((empty_col, image_skeletonize[:, :-1]))

        # print(image_skeletonize.shape, path_is_below.shape, path_is_above.shape, path_is_right.shape, path_is_left.shape)
        
        to_fill = (path_is_right + path_is_left) * (path_is_above + path_is_below)
        
        # * Remove redundants
        to_fill[0::2] = empty_row
        # to_fill[:, 1::2] = empty_col


        image_smooth += to_fill

        image_smooth[image_smooth >= 1] = 255   
        
        print(f"Smoothen: {time.time() - start}")    
        
        # * Encoding
        layout = image_smooth // 255

        return cls(layout = layout, original_image = original_image)
    

    def possible_paths(self, start, end):
        return path_finder.find_paths(self, start, end)

    def render_possible_paths(self, start, end, filepath = None):
        paths = self.possible_paths(start, end)
        image = np.array(self.original_image)
        # render = Image.fromarray(image)
        render = Image.fromarray(self.layout * 255)

        draw = ImageDraw.Draw(render)
        draw.point(posn_to_draw_point(start), 'limegreen')
        if not paths:
            draw.point(posn_to_draw_point(end), 'red')
        else:
            draw.point(posn_to_draw_point(end), 'darkgreen')
            # for path in paths[19:]:
            #     for pt in path[1:-1]:
            #         draw.point(posn_to_draw_point(pt), fill='blue')
                    # draw.point(posn_to_draw_point(np.subtract(pt,1)), fill='blue')
                #     draw.point(posn_to_draw_point(pt), fill='blue')
                #     draw.point(posn_to_draw_point(np.add(pt,1)), fill='blue')

            # # # * Path 20
            # for pt in paths[19][1:-1]:
            #     draw.point(posn_to_draw_point(np.subtract(pt,1)), fill='red')
            #     draw.point(posn_to_draw_point(pt), fill='red')
            #     draw.point(posn_to_draw_point(np.add(pt,1)), fill='red')
            # * Path 1
            for pt in paths[0][1:-1]:
                draw.point(posn_to_draw_point(pt), fill='blue')
                draw.point(posn_to_draw_point(np.subtract(pt,1)), fill='blue')
                draw.point(posn_to_draw_point(pt), fill='blue')
                draw.point(posn_to_draw_point(np.add(pt,1)), fill='blue')

            # print(paths[0] == paths[15])
            # print("Difference:",set(paths[0]) - set(paths[19]))
            

        if filepath is not None:
            render.save(filepath)
        return render


def posn_to_draw_point(pos: tuple[int, int]):
    return (pos[1], pos[0])