import os
from copy import copy
from operator import attrgetter

import cv2
import matplotlib.image as mpimg # just for intermediate image saving
from PIL import Image
from skimage.filters.rank import median
from skimage.morphology import binary_dilation, disk



class Component:
    def __init__(self, _id, _txt_pixels=0, _start_zone=(0,0), _end_zone=(0,0)):
        self.id = _id
        self.txt_pixels = _txt_pixels
        self.start_zone = _start_zone
        self.end_zone = _end_zone
        self.width = self.end_zone[1] - self.start_zone[1] + 1
        self.height = self.end_zone[0] - self.start_zone[0] + 1
    
    
    def __str__(self):
        return "Component " + str(self.id) + " has " + str(self.txt_pixels) +" "+ str(self.start_zone) + "\n"


    def add(self, other_comp):
        new_comp = copy(self)
        if type(new_comp.id) != list:
            new_comp.id = [new_comp.id]
        new_comp.id.append(other_comp.id)
        new_comp.txt_pixels += other_comp.txt_pixels
        new_comp.start_zone = (min(new_comp.start_zone[0], other_comp.start_zone[0]), \
                               min(new_comp.start_zone[1], other_comp.start_zone[1]))
        new_comp.end_zone = (max(new_comp.end_zone[0], other_comp.end_zone[0]), \
                             max(new_comp.end_zone[1], other_comp.end_zone[1]))
        new_comp.width = new_comp.end_zone[1] - new_comp.start_zone[1] + 1
        new_comp.height = new_comp.end_zone[0] - new_comp.start_zone[0] + 1
        return new_comp
        
        
    
class ImageMatrix:
    def __init__(self, _matrix):
        self.img_matrix = _matrix
        self.components = []
        self.rows = len(_matrix)
        self.columns = len(_matrix[0])
        self.comp_matrix = [[0 for i in range(self.columns)] for j in range(self.rows)]
        self.all_txt_pixels = 0
        self.text_zone_component = None


    def fill(self, coord_x, coord_y, comp_no):
        queue = []
        comp_size = 0
        upper_left = (coord_x, coord_y)
        lower_right = (coord_x, coord_y)

        def add_element(x, y, comp_no):
            nonlocal comp_size, queue, upper_left, lower_right
            comp_size += 1
            queue.append((x, y))
            self.comp_matrix[x][y] = comp_no
            upper_left = (min(upper_left[0], x), upper_left[1])
            upper_left = (upper_left[0], min(upper_left[1], y))
            lower_right = (max(lower_right[0], x), lower_right[1])
            lower_right = (lower_right[0], max(lower_right[1], y))


        add_element(coord_x, coord_y, comp_no)

        while(len(queue)):
            (coord_x, coord_y) = queue.pop(0)
            if coord_x > 0 and self.img_matrix[coord_x-1][coord_y] == 1 and self.comp_matrix[coord_x-1][coord_y] == 0: 
                add_element(coord_x-1, coord_y, comp_no)
            if coord_y > 0 and self.img_matrix[coord_x][coord_y-1] == 1 and self.comp_matrix[coord_x][coord_y-1] == 0: 
                add_element(coord_x, coord_y-1, comp_no)
            if coord_x < self.rows-1 and self.img_matrix[coord_x+1][coord_y] == 1 and self.comp_matrix[coord_x+1][coord_y] == 0: 
                add_element(coord_x+1, coord_y, comp_no)
            if coord_y < self.columns-1 and self.img_matrix[coord_x][coord_y+1] == 1 and self.comp_matrix[coord_x][coord_y+1] == 0: 
                add_element(coord_x, coord_y+1, comp_no)
        
        return comp_size, upper_left, lower_right


    def make_components(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.comp_matrix[i][j] == 0 and self.img_matrix[i][j] == 1:
                    id = len(self.components) + 1
                    comp_size, upper_left, lower_right = self.fill(i, j, id)
                    self.components.append(Component(id, comp_size, upper_left, lower_right))
                    self.all_txt_pixels += comp_size

        
    def precision(self, component):
        true_positives = component.txt_pixels
        positives = component.width * component.height
        return true_positives/positives


    def recall(self, component):
        true_positives = component.txt_pixels
        return true_positives/self.all_txt_pixels


    def f1_score(self, component):
        precision = self.precision(component)
        recall = self.recall(component)
        return 2 * precision * recall / (precision + recall)


    def compute_final_text_zone(self):
        self.make_components()
        component_list = sorted(self.components, key = attrgetter('txt_pixels'), reverse = True)
        if len(component_list) == 0:
            raise Exception ('No text detected in image!')
        self.text_zone_component = copy(component_list[0])
        for comp in component_list[1:]:
            current_f1_score = self.f1_score(self.text_zone_component)
            next_comp = self.text_zone_component.add(comp)
            next_f1_score = self.f1_score(next_comp)
            if next_f1_score < current_f1_score: break
            self.text_zone_component = next_comp
        return (self.text_zone_component.start_zone, self.text_zone_component.end_zone)



class TextImage:
    def __init__(self, _img_fname):
        self.img_fname = _img_fname
        

    
    def transform_image(self):

        # impacts what edge pixels we keep
        const_low_threshold = 200  #0.09
        const_high_threshold = 300 #0.17
        # impacts 'noise' reduction rate
        const_disk_radius = 2.5
        # impacts how much we dilate the pixels
        const_dilation_steps = 20

        if not os.path.isfile(self.img_fname):
            raise 'Image with filename ' + self.img_fname + ' not found!'

        # img_idx = os.path.splitext(os.path.basename(self.img_fname))[0]
        # print(img_idx)

        img = cv2.imread(self.img_fname, 0)

        canny_img = cv2.Canny(img, const_low_threshold, const_high_threshold)
        # cv2.imwrite('edges\\'+ img_idx +'_edge_image.jpg', canny_img)
        
        median_img = median(canny_img, disk(const_disk_radius))
        # cv2.imwrite('medians\\'+ img_idx +'_median_image.jpg', median_img)
        
        dilated_img = median_img
        for j in range(const_dilation_steps):
            dilated_img = binary_dilation(dilated_img)
        # cv2.imwrite('dilations\\'+ img_idx +'_dilation_image.jpg', dilated_img*255)

        return dilated_img


    def crop_text_zone(self, output_fname):

        img_matrix = ImageMatrix(self.transform_image())

        (start, end) = img_matrix.compute_final_text_zone()

        img = cv2.imread(self.img_fname)

        img = Image.fromarray(img, 'RGB')
        
        cropped_img = img.crop((start[1], start[0], end[1], end[0]))

        cropped_img.save(output_fname)



def main():
    input_dir = 'inputs'
    fnames = [fname for fname in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, fname))]

    for fname in fnames:
        img = TextImage(os.path.join(input_dir, fname))
        img.crop_text_zone('results\\'+ os.path.splitext(fname)[0] + '_cropped.jpg')


if __name__ == '__main__':
    main()