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
from title_screen import Title_Screen
from button import Button
from player import Player
from bomb import Bomb



#all objects are controlled through the game object
class Game:

    def __init__(self, player, other_player, map):
        
        #player objects
        self.player = player
        self.other_player = other_player

        #map object
        self.map = map

        # for if game is in the lobby area
        self.lobby_open = True

        self.screen_width = self.map.screen_width

        self.text = "INTERIM ROUND ... WEAPONS DISABLED TILL OTHER PLAYER JOINS"

        
        

    # gets the player inputs
    def getInputs(self): 
        # only checks for player inputs when the game isn't paused
        self.player.inputs()


    # transfers clients data and map data
    def transfer_data(self):
    
        return n.transfer( 
            convertClientDataToString(
                    (
                        self.player.x,               
                        self.player.y,               
                        self.player.cursor_pos[0],   
                        self.player.cursor_pos[1],
                        self.player.state_checker
                )                        
            )
        )
    
    # updates the objects in the game
    def update(self):
        

        # updates player position
        self.player.update(self.map.pieces)


        # checks whether bombs are created for the players
        self.player.check_bomb_creation(self.player.state_checker)
        self.other_player.check_bomb_creation(self.other_player.state_checker)


        # updates bomb 
        for p in [self.player, self.other_player]:
            
            for bomb in p.bombs:
                bomb.update(self.map.pieces)
    
                for player in [self.player, self.other_player]:

                    # for when a player is hit by bomb
                    if bomb.state == "exploded" and bomb.exp_collision(player):
                        
                        #ends interim round
                        if self.lobby_open:
                            self.lobby_open = False

                        else:    
                            player.lives -= 1
                        
                        self.endOfRoundChecks(player.lives)

        # transfers player data and updates the enemy clients player on your screen
        try: 
            self.other_player.set_player_data(
                convertRecvClientDataToInt(self.transfer_data())
            ) 

            # resets state checker back to 0 at the end of every update loop so that only bomb object is created
            self.player.state_checker = 0

        except:
            print("The client has disconnected from the server")

    def draw(self):
        
        #draws player objects and map
        self.map.draw()
        self.player.draw()
        self.other_player.draw()
    
        #draws bomb objects
        for player in [self.player, self.other_player]:
            for bomb in player.bombs:
                bomb.draw()
                
                # deletes the bomb after explosion
                if bomb.state == "exploded":
                    player.bombs.pop()
        
            DISPLAYSURF.blit(text.render(self.text, False, WHITE), (100, 200))


    def start_round(self):
        # sets state checker to "2" to tell server to send next map
        self.player.state_checker = 2

        # then sends data to server which sends back new map as game is going into next round
        self.transfer_data()
        
        # gets the map data 
        map_data = n.getMap()

        # sets state checker back to 0 so server doesn't update map again
        self.player.state_checker = 0

        # creates the new map object for the game
        self.map.y_vars = convertRecvMapDataToInt(map_data)
        self.map.create_map_obj()
        
        # sets the player client back to its starting position and sets the player clients state checker to 0
        player_data = convertRecvClientDataToInt(n.getPos())
        self.player.set_player_data(player_data)

        # player will fall fast downwards onto next map
        self.player.jumping = True

        # removes all getInputs events from queue so no bomb objects 
        pygame.event.clear()

    
    # pauses the game for 5 seconds and renders end round / game text
    def pause_game(self):
        
        for i in range(5):
            
            # adds the time length left of timer to the end round text
            self.text = self.text + " " + str(5-i)
            DISPLAYSURF.fill(BLACK)

            self.draw()
            pygame.display.flip()
            time.sleep(1)


    def endOfRoundChecks(self, lives):
        
        if lives == 0:
            self.end_game()
        
        else:
            self.end_round()


    def end_round(self):
        
        self.text = f"A player has lost the round. Next Round starting in "
        self.pause_game()
            
        # then sets the text back to nothing so text is not drawn whilst game is running and starts the next round
        self.player.jumping = False
        self.other_player.jumping = False
        self.text = ""
        self.start_round()


    # called once the game ends to reset to manage connections and re open main menu
    def end_game(self):
        
        #sets the text to the end game text
        self.text = "A player has lost the game. You will be returned to Main Menu in "

        # starts a 5 second count down for end of game 
        self.pause_game()
        
        #means that the network object no longer communicates with the server
        n.leave_server()

        global main_menu
        main_menu.open = True

        self.text = "INTERIM ROUND ... WEAPONS DISABLED TILL OTHER PLAYER JOINS"
        self.player.lives = self.other_player.lives = 3
        self.lobby_open = True
        
        # turns the mouse back on so player can interact with the title screen
        pygame.mouse.set_visible(True)

  

# checks whether or not the other player has joined
def check_server_full():
    if (player2.x -1000 == 0) and (player2.y -100 == 0):
        return False
    return True


# pygame initialisation
pygame.init()

# INITIALISING DISPLAY SURFACE
DISPLAYSURF = pygame.display.set_mode((800, 600))
DISPLAYSURF.fill(BLACK)

pygame.display.set_caption('SQUARE OFF')




# player objects
player1 = Player(0, 0, 5, 5, RED, 0)
player2 = Player(0, 0, 5, 5, RED, 0)


# terr is the map object
terr = GameMap(DISPLAYSURF.get_width(), DARK_GREEN)
terr.y_vars = [0]



# initialises the font to be used
pygame.font.init()
text = pygame.font.SysFont("Arial", 20)

# creates the title screen for the game where the user chooses to host, join or quit
main_menu = Title_Screen(DISPLAYSURF, text)


# initialises game object with 
game = Game(player1, player2, terr)


Clock = pygame.time.Clock()

# quits the game when the user presses the RED cross
def Quitting_Game(trigger):
    if trigger.type == QUIT:
        pygame.quit()
        sys.exit()



# MAIN GAME LOOP 

while True:
    # fills the screen BLACK again so sprties actually move
    DISPLAYSURF.fill(BLACK)


    # runs whilst the menu is open
    if main_menu.open:
        
        for event in pygame.event.get():
            #quits the game
            Quitting_Game(event)
            main_menu.handle_button_presses(event)
        
        # draws the title screen
        main_menu.draw()
        pygame.display.flip()

        
        # tick rate is set to 60: screen is updated 60 times a second
        Clock.tick(60)
    

    else:
        # gets key preses and button presses
        for event in pygame.event.get():
            Quitting_Game(event)
            game.getInputs()


        game.update()
        game.draw()

        #updates pygame display
        pygame.display.flip()
      
        # screen is updated 60 times a second
        Clock.tick(60)
