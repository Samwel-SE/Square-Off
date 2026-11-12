import sys

import pygame
from pygame.locals import QUIT

# game object class, to be inherited by all other classes
class GameObject:

    def __init__(self, x, y, width, height, colour, screen):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
        self.screen = screen

    # draws the gameobject 
    def draw(self):
        pygame.draw.rect(
            self.screen, 
            self.colour, 
            pygame.Rect(self.x, self.y, self.width, self.height)
        )

    # checks for collision between game object and other objects
    def collision(self, obj2):
        if( (self.x < obj2.x + obj2.width and 
           self.x + self.width > obj2.x) and 
           (self.y + self.height > obj2.y and 
           self.y < obj2.y + obj2.height) ):
            return True