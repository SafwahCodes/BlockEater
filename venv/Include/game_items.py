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

class Shape(BaseItem):

    def __init__(self, x, y, width_height):
        self.x = x
        self.y = y
        self.width_height = width_height
        self.coords = []
        self.rect_list = []
        self.generate_random_shape()
        self.rad = math.radians(90)

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
        for coord in self.coords.value:
            self.rect_list.append(pygame.Rect(self.x + (coord[0] * self.width_height), self.y + (coord[1] * self.width_height), self.width_height, self.width_height))

    def rotate(self):
        for rect in self.rect_list:
            rect.x -= self.x
            rect.y = self.y
            x_new = rect.x * math.cos(self.rad) - rect.y * main.sin(self.rad)
            y_new = rect.x * math.sin(self.rad) + rect.y * math.cos(self.rad)
            rect.x = x_new + self.x
            rect.y = y_new +self.y

    def draw(self, surface):
        for rect in self.rect_list:
            pygame.draw.rect(surface, self.rgb1, rect) # rect fill
            pygame.draw.rect(surface, self.rgb2, rect, 2) # rect outline

    def update(self):
        self.y += self.width_height
        for rect in self.rect_list:
            rect.move_ip(0, self.width_height)

class shape_coords(Enum):

    i = [[-(1), 0], [0, 0], [1, 0], [2, 0]]

    o = [[-(1), 0], [-(1), 1], [0, 0], [0, 1]]

    t = [[-(1), 0], [0, 0], [0, 1], [1, 0]]

    s = [[-(1), 1], [0, 0], [0, 1], [1, 0]]

    z = [[-(1), 0], [0, 0], [0, 1], [1, 1]]

    j = [[-(1), 0], [0, 0], [1, 0], [1, 1]]

    l = [[-(1), 0], [-(1), 1], [0, 0], [1, 0]]