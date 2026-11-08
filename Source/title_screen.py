import sys

import pygame
from pygame.locals import QUIT

from colours import *
from button import Button
from game_object import GameObject
from join_server_function import *

# Title screen object
class Title_Screen:

    def __init__(self, displaySurface, text):
        
        self.displaySurface = displaySurface

        self.text = text

        # x coord of text so its alligned with center of screen
        self.x_pos = self.displaySurface.get_width()//2 - 100

        self.join_server_1_button = Button(self.x_pos, 200, 220, 30, WHITE, self.displaySurface, self.text)

        self.join_server_2_button = Button(self.x_pos, 300, 220, 30, WHITE, self.displaySurface, self.text)

        self.quit_game_button = Button(self.x_pos, 400, 220, 30, WHITE, self.displaySurface, self.text)

        self.open = True


    # to be called in the pygame event loop
    def handle_button_presses(self, event):
        
        if self.join_server_1_button.on_click(event):
            
            # you join the server 
            if join_server(5555):
                self.open = False

            # you dont join the server as its full so error text shown
            else:
                self.join_server_1_button.error_text_on = True    

        if self.join_server_2_button.on_click(event): 
            
            # you join the server
            if join_server(6666):
                self.open = False
            
            # you dont join the server as its full so error text shown
            else:
                self.join_server_2_button.error_text_on = True

        if self.quit_game_button.on_click(event):
            quit()



    # draws the title screen
    def draw(self):

        # draws game title 
        self.displaySurface.blit(
            self.text.render("SQUARE OFF", False, WHITE), (self.x_pos, 100)
        )
        
        # draws join_server 1 button
        self.displaySurface.blit(
            self.text.render("Join Server 1", False, WHITE), (self.x_pos, 200)
        )

        self.join_server_1_button.draw()

        # draws join_server 2 button
        self.displaySurface.blit(
            self.text.render("Join Server 2", False, WHITE), (self.x_pos, 300)
        )

        self.join_server_2_button.draw()


        # draws quit game button
        self.displaySurface.blit(
            self.text.render("Quit Game", False, WHITE), (self.x_pos, 400)
        )

        self.quit_game_button.draw()