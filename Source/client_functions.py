
# cleans data to be sent to server
def convertClientDataToString(client_data):
    return (
        str(client_data[0]) + "," + 
        str(client_data[1]) + "," + 
        str(client_data[2]) + "," + 
        str(client_data[3]) + "," + 
        str(client_data[4])
    )


#cleans map data from server
def convertRecvMapDataToInt(decodedString):
    
    mapPieceYCoords = []
    decodedList = decodedString.split(",")
    
    for i in decodedList:

        #ignores empty i's
        if not(i):
            pass
        
        else:
            mapPieceYCoords.append(int(i))

    return mapPieceYCoords



