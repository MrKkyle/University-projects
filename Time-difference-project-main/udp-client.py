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
file = open("client_meetings.txt", "r")
line = file.readline()
message = ""

while(line != ''): 
    
    information = line.split(',')
    #message sent to server
    message = message + listToString(information) + " "
    line = file.readline();    

#message is sent to server 
clientSocket.sendto(message.encode(),(serverName, serverPort))

modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

#modified message is printed
print (modifiedMessage.decode())
clientSocket.close()
   