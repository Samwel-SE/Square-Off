import sys

import pygame
from pygame.locals import QUIT

from game_object import GameObject

# Map class, generates the map and is comprised of gameobjects
class GameMap:

    def __init__(self, displayWidth, colour):
        self.screen_width = displayWidth
        self.colour = colour
        self.pieces = []

        # stores y variables of all the objects making up the map
        self.y_vars = 0
        self.piece_height = 300

    # creates map obj once y_vars stores new map sent from server
    def create_map_obj(self):
        self.pieces.clear()
        for i in range(len(self.y_vars)):
            self.pieces.append(
                GameObject(i, self.y_vars[i], 1, self.piece_height, self.colour)
            )

    # iterates through and draws all the gameobjects making up the map
    def draw(self):
        for i in range(len(self.y_vars)):
            self.pieces[i].draw()