import pygame

from network import Network

# below import is used with network object and server script
from client_functions import *
from common_functions import *
from colours import *

def join_server(server_address, DISPLAYSURF, player1, player2, terr):
    
    global n 

    n = Network()
    
    #Please put IP here
    server_ip = "0.0.0.0"

    n.assign_network_address(server_ip, server_address)
    if n.connect() == "connection success":
        n.update_data_client_side()

        #gets starting position of player from server
        startpos = convertRecvClientDataToInt(n.getPos())

        # 1st to join is the red player, UI in top left
        if n.id == "0":
            player1.colour = RED
            player2.colour = BLUE
            
            player1.ui_x_coord = 0
            player2.ui_x_coord = DISPLAYSURF.get_width() -50
        
        # 2nd to join is the blue player, UI in top right
        else:
            player1.colour = BLUE
            player2.colour = RED
            
            player1.ui_x_coord = DISPLAYSURF.get_width() -50
            player2.ui_x_coord = 0
        
        # sets the player objects up
        player1.x, player1.y = startpos[0], startpos[1]
        player2.x, player2.y = startpos[0], startpos[1]

        player1.jumping = True
        player2.jumping = True



        # sets the map object up
        terr.y_vars = convertRecvMapDataToInt(n.getMap())
        terr.create_map_obj(DISPLAYSURF)

        # stops player from seeing mouse cursor so has to use in game cursor to aim
        pygame.mouse.set_visible(False)
        return True

    #otherwise returns False
    return False