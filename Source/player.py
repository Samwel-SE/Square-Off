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
from bomb import Bomb

from check_server_full import *

# player class inherits gameobject class
class Player(GameObject):
    
    def __init__(self, x, y, width, height, colour, screen, ui_x_coord):
        super().__init__(x, y, width, height, colour, screen)

        # user interface x coordinate
        self.ui_x_coord = ui_x_coord

        # use bools so can tell when keys are held down 
        self.move_right = False
        self.move_left = False

        #cursor position
        self.cursor_pos = [0,0]

        # jumping is true when player is not touching the ground
        self.jumping = False
        self.jump_vel = 12
        self.jump_height = 12

        # bombs object array
        self.bombs = []
        self.state_checker = 0

        # bullet direction x and y
        self.bomb_dx = 0
        self.bomb_dy = 0
        
        # Number of lives player has
        self.lives = 3
        
    

    # gets keys currently pressed so player character can move
    def inputs(self, event):

        # movement inputs
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                self.move_right = True
            if event.key == pygame.K_a:
                self.move_left = True
            if event.key == pygame.K_w and self.jumping == False:
                self.jumping = True
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                self.move_right = False
            if event.key == pygame.K_a:
                self.move_left = False

        # Once the left mouse button is pressed and there are no other bombs on screen will create a bomb object,
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            if (pygame.mouse.get_pressed(3) and
                (len(self.bombs) == 0) and 
                (self.state_checker != 9)
                ):
                    self.state_checker = 1

    # player jump
    def jump(self):
        if self.jumping:
            # jump_vel goes from positive to negative during jump function allowing player to fall back down to the ground.
            self.y -= self.jump_vel
            self.jump_vel -= 1

        # while player has not pressed jump key they will constantly move downwards as to not break game
        else:
            self.y += 5


    # upates the position of the player
    def update(self, pieces):
        
        # collision between parts of terrain that are too high for the player to climb or the edge of the screen
        if (self.y > pieces[self.x -3].y +2) or self.x <= 10:
            self.move_left = False 
                    
        elif (self.y > pieces[self.x +3].y +2) or self.x >= self.screen.get_width() -10:
            self.move_right = False

        # jump command for player 
        self.jump()
        
        # moves player left and right
        if self.move_right:
            self.x += 3
        if self.move_left:
            self.x -= 3

        # collision so that player does not fall through the map
        if (
            self.collision(pieces[self.x]) or 
            self.collision(pieces[self.x + self.width])
            ):
                self.y = pieces[self.x].y - 5
                self.jumping = False
                self.jump_vel = self.jump_height

        # then gets the coords of the players cursor
        self.get_cursor(pygame.mouse.get_pos())


    # gets coordinates of line making up player cursor
    def get_cursor(self, mouse_tuple):

        # stores the difference in x & y between cursor pos and mouse pos
        diff = {"x": abs(mouse_tuple[0] -self.x) *0.04, 
                "y": abs(mouse_tuple[1] -self.y) *0.04
            }
        
        if mouse_tuple[0] >= (self.x + 2): 
           self.bomb_dx = diff["x"]
        else: 
            self.bomb_dx = -diff["x"]

        if mouse_tuple[1] <= (self.y + 2): 
            self.bomb_dy = -diff["y"]
        else: 
            self.bomb_dy = diff["y"]
        
        # rounds the bomb dx and dy to the nearest integer
        self.bomb_dx = round(self.bomb_dx) 
        self.bomb_dy = round(self.bomb_dy)
        
        # then sets the coordinates of the cursor
        self.cursor_pos = [self.bomb_dx +self.x+2 , self.bomb_dy +self.y+2]

        # and returns it
        return self.cursor_pos



    # checks whether bomb needs to be created
    def check_bomb_creation(self, bomb_creation_on_1):
        
        # if clients bomb_init equals 1 it will append a 
        # bomb object to other_players bomb list so it is drawn on the screen
        if bomb_creation_on_1 == 1:
            
            # calculates dx and dy of player bomb from cursor_position
            self.bomb_dx = self.cursor_pos[0] -self.x-2
            self.bomb_dy = self.cursor_pos[1] -self.y-2
            

            self.bombs.append(
                Bomb(
                    self.x + 2,
                    self.y + 2, 
                    3, 
                    3, 
                    (255, 255, 0), 
                    self.screen,
                    self.bomb_dx, 
                    self.bomb_dy
                )
            )

    

    # function is used to control the client player in host players game
    def set_player_data(self, client_data):
        
        # coords 
        self.x = client_data[0]
        self.y = client_data[1]

        # cursor coords
        self.cursor_pos = [client_data[2], client_data[3]]
        
        # state checker
        self.state_checker = client_data[4]



    # adds drawing player cursor, life count and currently equipped weapon
    def draw(self):
        super().draw()

        # draws players cursor
        pygame.draw.line(self.screen, self.colour, (self.x + 2, self.y + 2), self.cursor_pos,1)

        #draws player live count
        for i in range(self.lives):
            
            xCoordOfRect = self.lives +i*10 +self.ui_x_coord
            
            pygame.draw.rect(
                self.screen, 
                self.colour, 
                pygame.Rect(xCoordOfRect, 0, 5, 10)
            )