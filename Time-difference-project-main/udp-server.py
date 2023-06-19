# udp-server.py

from socket import *
import datetime
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(("", serverPort))
print('The server is ready to receive')

def stringToList(string):
    lister = list(string.split(" "))
    return lister
    
def splitList(lister, value):
    new_list = list()
    for i in range(0, len(lister), value):
        new_list.append(lister[i:i+value])
    
    return new_list 

def listToString(list):
    
    string = ""
    for element in list:
        string = string + element
    
    return string          
    
while True:
    
    #received from client
    message, clientAddress = serverSocket.recvfrom(2048) 
    
    #decodes the message
    messager = message.decode()
    
    #convert string messager to list
    new_message = stringToList(messager)
    
    #splits the list into smaller lists
    m = splitList(new_message, 5)
    
    #reading of server_time difference.txt
    file = open("server_time_difference.txt", "r")
    kara = ""
    l = file.readline()
    while(l != ''): 
        info = l.split(",")
        kara = kara + listToString(info) + " "
        l = file.readline(); 
         
       
 
    #convert to list    
    k = stringToList(kara)
    
    #remove empty strings
    new_list = [x for x in k if x != '']
    
    #convert to smaller lists
    _kara = splitList(new_list, 2)
    
    #split into city and time_diff
    _city = []
    _time_diff = []
    for list in _kara:
        _city.append(list[0])
        _time_diff.append(list[1])
        
    
    
    #remove last element('') from list
    m[-1].remove('')
    new = [x for x in m if x]
    date = []
    city = []
    time = []
    topic = []
    platform = []
    for list in new:
        date.append(list[0])
        city.append(list[1])
        time.append(list[2])
        topic.append(list[3])
        platform.append(list[4])
    
    #replace the - with , in order for the time function to work
    time = [p.replace("-", ",") for p in time]
    
    #remove "\n" from _time_diff
    time_diff = []
    for sub in _time_diff:
        time_diff.append(sub.replace("\n", "")) 
        
    time_diffe = [p.replace("-", "") for p in time_diff] 
    time_diffe = [p.replace("+", "") for p in time_diff]   
    
    
    #time_diffe = list without + or - needed to calculate time difference
    #time_diff = list including the + and - to check if the time should be added or minused
    
    c = 0
    final = ""
    while c < len(city):
        index = _city.index(city[c])
        
        #get time difference of that city to SA
        time_difference = time_diffe[index]
        timeInCity = time[index]
        
        
        #using datetime module, we calculate the difference in time
        _time = datetime.timedelta()
        (h, m) = (time_diffe[index]).split(':')
        (x, y) = (time[index]).split(':')
        time_difference = datetime.timedelta(hours = (int)(h), minutes = int(m))
        timeInCity = datetime.timedelta(hours = (int)(x), minutes = int(y))

        
        
        _time = timeInCity + time_difference 
        _time = str(_time)   
        
        #insert time difference into string and send back home
        #string format: [Date, City, Time(_time), Topic, Platform]
        
        final = final + (date[c] + " " + city[c] + " " + _time + " " + topic[c] + " " + platform[c])
        c += 1
    
    
    #message is uppercased and sent back to client
    final = final.upper()
    

    #sent to client
    serverSocket.sendto(final.encode(),clientAddress)
