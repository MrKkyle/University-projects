# udp-server.py
import sys
from socket import *
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(("", serverPort))
print('The server is ready to receive')

#Graph class
class Graph(object):
    def __init__(self, nodes, init_graph):
        self.nodes = nodes
        self.graph = self.construct_graph(nodes, init_graph)
        
    def construct_graph(self, nodes, init_graph):
        graph = {}
        for node in nodes:
            graph[node] = {}
        
        graph.update(init_graph)
        
        for node, edges in graph.items():
            for adjacent_node, value in edges.items():
                if graph[adjacent_node].get(node, False) == False:
                    graph[adjacent_node][node] = value
                   
        return graph
    
    def get_nodes(self):
        "Returns the nodes of the graph."
        return self.nodes
    
    def get_outgoing_edges(self, node):
        "Returns the neighbors of a node."
        connections = []
        for out_node in self.nodes:
            if self.graph[node].get(out_node, False) != False:
                connections.append(out_node)
        return connections
    
    def value(self, node1, node2):
        "Returns the value of an edge between two nodes."
        return self.graph[node1][node2]
    
#Dijkstra's Algorithm    
def dijkstra_algorithm(graph, start_node):
    unvisited_nodes = list(graph.get_nodes())
   
    shortest_path = {}
    previous_nodes = {}
 
    # We'll use max_value to initialize the "infinity" value of the unvisited nodes   
    max_value = sys.maxsize
    for node in unvisited_nodes:
        shortest_path[node] = max_value
     
    shortest_path[start_node] = 0
        
    while unvisited_nodes:
        
        current_min_node = None
        for node in unvisited_nodes: # Iterate over the nodes
            if current_min_node == None:
                current_min_node = node
            elif shortest_path[node] < shortest_path[current_min_node]:
                current_min_node = node
                
        neighbors = graph.get_outgoing_edges(current_min_node)
        for neighbor in neighbors:
            tentative_value = shortest_path[current_min_node] + graph.value(current_min_node, neighbor)
            if tentative_value < shortest_path[neighbor]:
                shortest_path[neighbor] = tentative_value
                previous_nodes[neighbor] = current_min_node
 
        # After visiting its neighbors, we mark the node as "visited"
        unvisited_nodes.remove(current_min_node)
    
    return previous_nodes, shortest_path

#prints the results
def print_result(previous_nodes, shortest_path, start_node, target_node):
    path = []
    node = target_node
    
    while node != start_node:
        path.append(node)
        node = previous_nodes[node]
 
    # Add the start node manually
    path.append(start_node)
    
    #print("We found the following best path with a value of " + str(shortest_path[target_node]))
    #print(" -> ".join(reversed(path)))
    
    return("Shortest Path: " + str(shortest_path[target_node]) + "\n" + " -> ".join(reversed(path)) )

#Converts a string to list
def stringToList(string):
    lister = list(string.split(" "))
    return lister
    
#splits a larger list into smaller ones    
def splitList(lister, value):
    new_list = list()
    for i in range(0, len(lister), value):
        new_list.append(lister[i:i+value])
    
    return new_list 

#converts a List to a string
def listToString(list):
    
    string = ""
    for element in list:
        string = string + element
    
    return string

nodes = [   
            "Mitchells-Plain", "Khayelitsha", "Claremont", "Parow", "Sea-Point", "Nyanga", "Cape-town-central", "Belhar", "Goodwood", "Wynberg", 
            "Mowbray"
         ]
 
init_graph = {}
for node in nodes:
    init_graph[node] = {}
    
init_graph["Mitchells-Plain"]["Khayelitsha"] = 2
init_graph["Mitchells-Plain"]["Parow"] = 4
init_graph["Khayelitsha"]["Nyanga"] = 1
init_graph["Khayelitsha"]["Claremont"] = 3
init_graph["Claremont"]["Cape-town-central"] = 3
init_graph["Claremont"]["Belhar"] = 2
init_graph["Belhar"]["Cape-town-central"] = 1
init_graph["Sea-Point"]["Parow"] = 2
init_graph["Goodwood"]["Belhar"] = 1
init_graph["Goodwood"]["Claremont"] = 4
init_graph["Wynberg"]["Cape-town-central"] = 1
init_graph["Wynberg"]["Parow"] = 2
init_graph["Mowbray"]["Khayelitsha"] = 1
init_graph["Mowbray"]["Sea-Point"] = 3



graph = Graph(nodes, init_graph)

while True:    
    #received from client
    message, clientAddress = serverSocket.recvfrom(2048) 
    
    #decodes the message
    messager = message.decode()
    
    #convert string messager to list
    new_message = stringToList(messager)
    
    #splits the list into smaller lists
    m = splitList(new_message, 2)
    

    #remove last element('') from list
    m[-1].remove('')
    m = [x for x in m if x]
    
    #remove "\n" from m elements
    _path = []
    for sub in m:  
        temp = [item.strip() for item in sub]
        _path.append(temp)
    
    
    final = ""
    result = ""
    c = 0
    while c < len(_path):
        
        #source/destination passed into the algorithm    
        source = ""
        dest = ""
        source =_path[c][0]
        dest = _path[c][1]

        
        #This calculates the shortest path and passes it onto the 'final' string and then written to the 'client_shortest_path.txt'
        previous_nodes, shortest_path = dijkstra_algorithm(graph = graph, start_node = source)
        result = print_result(previous_nodes, shortest_path, start_node = source, target_node = dest)
        
        final = final + (source + " -> " + dest + " " + "\n" + result + "\n" + "\n")

        c += 1
    
    #sent to client
    serverSocket.sendto(final.encode(),clientAddress)
