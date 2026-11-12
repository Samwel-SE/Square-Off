# checks whether or not the other player has joined
def check_server_full():
    if (player2.x -1000 == 0) and (player2.y -100 == 0):
        return False
    return True