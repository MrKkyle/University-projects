# udp-client.py

from socket import *
serverName = "127.1.1.0"
serverPort = 12000
clientSocket = socket(AF_INET,SOCK_DGRAM)

def listToString(list):
    
    string = ""
    for element in list:
        string = string + element
    
    return string 

#import information from the .txt file and send it to server
#has format [Date, City, Time, Topic, Platform]
file = open("client_path.txt", "r")
line = file.readline()
message = ""

while(line != ''): 
    
    information = line.split(',')
    #message sent to server
    message = message + listToString(information) + " "
    line = file.readline(); 


#sends message to server
clientSocket.sendto(message.encode(),(serverName, serverPort))

#once it recieves the server's message on the shortest path, it saves it in the txt file
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

#writes message to .txt file

file = open("client_shortest_paths.txt", "w")
file.write(modifiedMessage.decode())
file.close()
clientSocket.close()
