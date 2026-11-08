import sys

import pygame
from pygame.locals import QUIT
import time

from colours import *
from game_object import GameObject


# button class is used in the title screen
class Button(GameObject):

    def __init__(self, x, y, width, height, colour, displaySurface, text):
        super().__init__(x, y, width, height, colour)

        self.error_text_on = False
        self.displaySurface = displaySurface
        self.text = text

    #overrides draw so text is visible
    def draw(self):
        
        pygame.draw.rect(
            self.displaySurface, 
            self.colour, 
            pygame.Rect(self.x, self.y, self.width, self.height), 
            1
        )

        if self.error_text_on:
            displaySurface.blit(
                self.text.render("Server Full. Try Join another server", False, RED), 
                (self.x, self.y + 50)
            )


    # runs certain code once the button has been pressed
    def on_click(self, event):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if(
                pygame.mouse.get_pressed(3) and 
                (mouse_x > self.x and mouse_x < self.x +self.width) and 
                (mouse_y > self.y and mouse_y < self.y + self.height)
            ):
                return True