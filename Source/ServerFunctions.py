
# returns map data in string form
def convertMapDataToString(y_list):
    encoded_string = ""

    for i in y_list: 
        encoded_string = encoded_string + str(i) + ","
    
    #ignores final comma at the end of string
    encoded_string = encoded_string[:-1]
    
    return encoded_string


# function for sending map data as a string to clients to be decoded
def convertRoundStartDataToString(client_id, client_data, map_data):
    return (
        str(client_id) + "," + 
        convertClientPositionDataToString(client_data) + "," + 
        convertMapDataToString(map_data)
    )



# encodes the data into string form to send to the clients
def convertClientPositionDataToString(client_data):
    stringified_data = []

    for i in [0,2]:
        if len(str(client_data[i])) < 4:
            stringified_data.append("0" + str(client_data[i]))

        else:
            stringified_data.append(str(client_data[i]))


    return (stringified_data[0] + "," + 
            str(client_data[1]) + "," + 
            stringified_data[1] + "," + 
            str(client_data[3]) + "," + 
            str(client_data[4])
    )



