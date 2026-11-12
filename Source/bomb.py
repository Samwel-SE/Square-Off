import sys

import pygame
from pygame.locals import QUIT
import time

from network import Network

# below import is used with network object and server script
from client_functions import *
from common_functions import *

from colours import *


from game_object import GameObject
from game_map import GameMap


# Bomb class, inherits Game Object Class
class Bomb(GameObject):

    def __init__(self, x, y, width, height, colour, screen, dx, dy):
        super().__init__(x, y, width, height, colour, screen)
        
        # change in x and y Ie movement speed of bomb
        self.dx = dx
        self.dy = dy
        
        # radius of bomb explosion
        self.exp_rad = 50
        
        # state of bomb: moving or exploded
        self.state = "moving"


    # movement of the bomb
    def update(self, pieces):

        # increments the bombs x coordinate
        self.x += self.dx

        # increments the bombs y coordinate
        self.y += self.dy
        self.dy += 1

        # collision for bombs and end of screen
        if self.x >= self.screen.get_width() or self.x <= 0:
            self.explode()
        

        # code below means bomb will bounce after colliding with the map
        elif self.collision(pieces[self.x]):
            self.explode()



    def draw(self):
        if self.state == "exploded":

            # rgb code used below is colour orange
            pygame.draw.circle(
                self.screen, 
                ORANGE, 
                (self.x+1, self.y+1), 
                self.exp_rad
            )

        else:

            # isn't exploded then draws the bomb as square
            super().draw()


    # draws the expxlosion of the bomb
    def explode(self):
        self.state = "exploded"

    # checks whether points of other objects overlap with explosion
    def exp_collision(self, obj2):
        
        circleBetweenTwoObjects = (
            ((self.x -1)- obj2.x) ** 2 + ((self.y +1) - obj2.y) ** 2
        )
        
        if (circleBetweenTwoObjects <= self.exp_rad**2):
            return True
        return False