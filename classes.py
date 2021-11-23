import random
import math
import os
import pygame
from folder2048 import constants as cst
from folder2048.objects import *


class Cell:
    def __init__(self):
        self.is_playing = False
        self.value = 0
        pass


class Grid:
    def __init__(self, size):
        self.size = size
        self.cells = [[Cell() for i in range(size)] for j in range(size)]

        # img stuffs
        current_path = os.path.dirname(__file__)  # directory where the .py file is located
        self.image_path = os.path.join(current_path, 'pics')  # The image folder path
        self.grid_img = pygame.transform.scale(pygame.image.load(os.path.join(self.image_path, "grid" + ".png")), cst.SCREENSIZE)
        self.img_by_number = [pygame.image.load(os.path.join(self.image_path, str(2**i) + ".png")) for i in range(1, 10)]
        self.room_between_tiles = int(cst.SCREENSIZE[0] / 25)
        self.tile_size = int(cst.SCREENSIZE[0] / 5)
        for i in range(len(self.img_by_number)):
            self.img_by_number[i] = pygame.transform.scale(self.img_by_number[i], (self.tile_size, self.tile_size))

    def get_random_cell(self):

        cells = self.available_cells()

        if len(cells) > 0:
            return cells[math.floor(random.random() * len(cells))]

    def place_random_cell(self):
        if self.available_cells():
            value = 2 if random.random() < 0.9 else 4
            self.insert_cell(value, self.get_random_cell())

    def available_cells(self):
        cells = []
        for i in range(self.size):
            for j in range(self.size):
                if not self.cells[i][j].is_playing:
                    cells.append((i, j))
        return cells

    def cell_available(self, x, y):
        pass

    def on_grid(self, position):
        return 0 <= position[0] < self.size and 0 <= position[1] < self.size

    def insert_cell(self, value, position):
        self.cells[position[0]][position[1]].value = value
        self.cells[position[0]][position[1]].is_playing = True

    def add_start_cells(self, starting_tile_num):
        for i in range(starting_tile_num):
            self.place_random_cell()

    def draw(self):
        screen.blit(self.grid_img, (0, 0))
        for i in range(len(self.cells)):
            for j in range(len(self.cells)):
                if self.cells[i][j].is_playing:
                    img_num = int(math.log2(self.cells[i][j].value)) - 1
                    img = self.img_by_number[img_num]
                    size = (self.room_between_tiles + j * (self.room_between_tiles + self.tile_size),
                            self.room_between_tiles + i * (self.room_between_tiles + self.tile_size))
                    screen.blit(img, size)

    def print_grid(self):
        for i in range(len(self.cells)):
            print()
            for j in range(len(self.cells)):
                print(" " + str(self.cells[i][j].value), end="")

    @staticmethod
    def transpose(cells):
        new_cells = [[cells[i][j] for i in range(len(cells))] for j in range(len(cells))]
        for i in range(len(new_cells)):
            new_cells[i].reverse()
        return new_cells

    def swipe_right(self):
        for i in range(len(self.cells)):
            counter = len(self.cells) - 1
            for j in range(counter,-1,-1):
                if self.cells[i][j].is_playing:
                    # combination
                    if counter != len(self.cells)-1 and self.cells[i][counter+1].value == self.cells[i][j].value:
                        self.cells[i][counter+1].value *= 2
                        self.cells[i][j] = Cell()
                    # basic movement
                    else:
                        if self.cells[i][j].is_playing:
                            self.cells[i][counter] = self.cells[i][j]
                            if j != counter:
                                self.cells[i][j] = Cell()
                            counter -= 1

    def swipe_left(self):
        for i in range(len(self.cells)):
            counter = 0
            for j in range(len(self.cells)):
                if counter != 0 and self.cells[i][counter-1].value == self.cells[i][j].value:
                    self.cells[i][counter-1].value *= 2
                    self.cells[i][j] = Cell()
                # basic movement
                else:
                    if self.cells[i][j].is_playing:
                        self.cells[i][counter] = self.cells[i][j]
                        if j != counter:
                            self.cells[i][j] = Cell()
                        counter += 1

    def swipe_down(self):
        self.cells = self.transpose(self.cells)
        self.swipe_left()
        self.cells = self.transpose(self.cells)
        self.cells = self.transpose(self.cells)
        self.cells = self.transpose(self.cells)

    def swipe_up(self):
        self.cells = self.transpose(self.cells)
        self.swipe_right()
        self.cells = self.transpose(self.cells)
        self.cells = self.transpose(self.cells)
        self.cells = self.transpose(self.cells)
