import pygame
from random import randint
from enum import Enum
import math

class BaseItem(object):

    def __init__(self):
        pass

    def draw(self, surface):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

class Grid(BaseItem): # 2d list of colors (maybe)

    def __init__(self):
        pass

    def draw(self, surface):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

class Wall(BaseItem):

    def __init__(self, left, top, width, height, background_color):
        self.rect = pygame.Rect(left, top, width, height)
        self.color = background_color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def update(self):
        pass

class Shape(BaseItem):

    def __init__(self, x, y, width_height):
        self.x = x
        self.y = y
        self.width_height = width_height
        self.rect_list = []
        self.rad = math.radians(90)
        self.coords = []
        self.generate_random_shape()

    def generate_random_shape(self):
        rand = randint(0, 7)
        if rand == 0:
            self.coords = shape_coords.i
            self.rgb1 = (0, 255, 255)
            self.rgb2 = (0, 128, 128)
        elif rand == 1:
            self.coords = shape_coords.o
            self.rgb1 = (255, 255, 0)
            self.rgb2 = (128, 128, 0)
        elif rand == 2:
            self.coords = shape_coords.t
            self.rgb1 = (255, 0, 255)
            self.rgb2 = (128, 0, 128)
        elif rand == 3:
            self.coords = shape_coords.s
            self.rgb1 = (0, 255, 0)
            self.rgb2 = (0, 128, 0)
        elif rand == 4:
            self.coords = shape_coords.z
            self.rgb1 = (255, 0, 0)
            self.rgb2 = (128, 0, 0)
        elif rand == 5:
            self.coords = shape_coords.j
            self.rgb1 = (0, 0, 255)
            self.rgb2 = (0, 0, 128)
        else:
            self.coords = shape_coords.l
            self.rgb1 = (255, 165, 0)
            self.rgb2 = (128, 38, 0)
        self.setup_shape()

    def setup_shape(self):
        for coord in self.coords.value:
            self.rect_list.append(pygame.Rect(self.x + (coord[0] * self.width_height), self.y + (coord[1] * self.width_height), self.width_height, self.width_height))

    def reset_coordinates(self, x, y):
        self.x = x
        self.y = y
        self.rect_list = []
        self.setup_shape()

    def rotate(self):
        for rect in self.rect_list:
            rect.x -= self.x
            rect.y -= self.y
            x_new = rect.x * math.cos(self.rad) - rect.y * math.sin(self.rad)
            y_new = rect.x * math.sin(self.rad) + rect.y * math.cos(self.rad)
            rect.x = x_new + self.x
            rect.y = y_new + self.y

    def has_collide_wall(self, other_rect):
        if other_rect.rect.collidelist(self.rect_list) is not -1:
            return True
        return False

    def has_collide_fixed(self, fixed_rect_list):
        for rect in self.rect_list:
            if rect.collidelist(fixed_rect_list) is not -1:
                return True
        return False

    def move_left(self):
        self.x -= self.width_height
        for rect in self.rect_list:
            rect.move_ip(-(self.width_height), 0)

    def move_right(self):
        self.x += self.width_height
        for rect in self.rect_list:
            rect.move_ip(self.width_height, 0)

    def move_up(self):
        self.y -= self.width_height
        for rect in self.rect_list:
            rect.move_ip(0, -(self.width_height))

    def move_down(self):
        self.y += self.width_height
        for rect in self.rect_list:
            rect.move_ip(0, self.width_height)

    def reset(self, x, y):
        #for rect in
        pass

    def draw(self, surface):
        for rect in self.rect_list:
            pygame.draw.rect(surface, self.rgb1, rect) # rect fill
            pygame.draw.rect(surface, self.rgb2, rect, 2) # rect outline

    def update(self):
        self.move_down()

class shape_coords(Enum):

    i = [[-(1), 0], [0, 0], [1, 0], [2, 0]]

    o = [[-(1), 0], [-(1), 1], [0, 0], [0, 1]]

    t = [[-(1), 0], [0, 0], [0, 1], [1, 0]]

    s = [[-(1), 1], [0, 0], [0, 1], [1, 0]]

    z = [[-(1), 0], [0, 0], [0, 1], [1, 1]]

    j = [[-(1), 0], [0, 0], [1, 0], [1, 1]]

    l = [[-(1), 0], [-(1), 1], [0, 0], [1, 0]]