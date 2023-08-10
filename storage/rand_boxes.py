import random
from functools import reduce
from time import time

import numpy as np
        
sizes_exp = [*range(400, 600, 100)]
TIMEOUT = 5
        
class Box:
    
    def __init__(self, WHD, seed):
        self.width = WHD[0]
        self.height = WHD[1]
        self.depth = WHD[2]
        self.gen_new_position(seed)
        
    def __repr__(self):
        return f'(pos: {self.x}, {self.y}, {self.z}; sizes: {self.width}, {self.height}, {self.depth})'
    
    @property
    def volume(self):
        return self.width * self.height * self.depth
        
    def gen_new_position(self, randstop):
        self.x = random.randint(0, randstop)
        self.y = random.randint(0, randstop)
        self.z = random.randint(0, randstop)
        
class Cell:
    
    def __init__(self, WHD):
        self.width = WHD[0]
        self.height = WHD[1]
        self.depth = WHD[2]
        self.boxes = []
        self.time_start = 0
        self.time_end = 1
        
    def __repr__(self):
        return f'{self.boxes}'
        
    @property
    def volume(self):
        return self.width * self.height * self.depth
    
    @property
    def vol_left(self):
        return self.volume - reduce(lambda i, j: i + j, map(lambda box: box.volume, self.boxes))
        
    def generate_boxes(self, num, sizes, seed):
        self.time_start = time()
        counter = 0
        while len(self.boxes) < num and self.time_end - self.time_start < TIMEOUT:
            self.time_end = time()
            self.add_box(Box(
                (
                    random.choice(sizes),
                    random.choice(sizes),
                    random.choice(sizes)
                ),
                seed
            ))
        
    def add_boxes_from_list(self, box_list: list[Box]):
        counter = 0
        copy_box_list = box_list.copy()
        while counter < len(copy_box_list):
            state = self.add_box(copy_box_list[counter])
            if state:
                counter += 1
            else:
                copy_box_list[counter].gen_new_position(3000)
        
    def add_box(self, box: Box):
    
        if not self.check_intercept(box):
            return False
        
        print(f'Generated: {len(self.boxes)}')
        self.time_start = time()
        self.boxes.append(box)
        return True
    
    def check_intercept(self, new_box: Box):
        w = new_box.width
        h = new_box.height
        d = new_box.depth
        x = new_box.x
        y = new_box.y
        z = new_box.z
        
        for box in self.boxes:
            if (box.x <= x + w <= box.x + box.width or
                box.y <= y + h <= box.y + box.height or
                box.z <= z + d <= box.z + box.depth):
                return False
        
        if (x + w <= self.width and
            x + w <= self.height and
            x + w <= self.depth):
            return True
        
        return False
            
if __name__ == '__main__':
    cell = Cell((3000, 3000, 2000))
    cell.generate_boxes(20, sizes_exp, 3000)
    print(cell.boxes)
    print(len(cell.boxes), cell.vol_left)