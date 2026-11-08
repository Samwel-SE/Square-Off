
# cleans data from server
def convertRecvClientDataToInt(str):
    str = str.split(",")
    
    return (int(str[0]), 
            int(str[1]), 
            int(str[2]), 
            int(str[3]), 
            int(str[4])
    )