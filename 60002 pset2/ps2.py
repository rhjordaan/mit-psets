# 6.0002 Problem Set 2 Spring 2020
# Graph Optimization
# Name: Richter Jordaan
# Collaborators: None
# Time: 2:00

#
# Finding shortest paths to drive from home to work on a road network
#


import unittest
from graph import DirectedRoad, Node, RoadMap


# PROBLEM 2: Building the Road Network
#
# PROBLEM 2a: Designing your Graph
#
# What do the graph's nodes represent in this problem? What
# do the graph's edges represent? Where are the times
# represented?
#
# ANSWER:
#The nodes are the intersections/street places where roads collide, like the places where you have a choice
#about what road to take from there.
# The edges are the roads themselves. The times represented is how long it takes to drive through that road
#and the times are represented as the weight of the edges of the graph.


# PROBLEM 2b: Implementing load_map
def load_map(map_filename):
    """
    Parses the map file and constructs a road map (graph).

    Parameters:
    map_filename - name of the map file

    Assumes:
    Each entry in the map file consists of the following format, separated by tabs:
        From To TotalTime  RoadType
        e.g.
            N0	N1	15	interstate
    This entry would become an edge from 'N0' to 'N1' on an interstate highway with 
    a weight of 15. There should also be another edge from 'N1' to 'N0' on an interstate
    using the same weight.

    Returns:
    a directed road map representing the inputted map
    """
    file = open(map_filename) #open file
    road_map = RoadMap() #create roadmap object
    for line in file: #for every line in file, add line's info to roadmap
        lineinfo = line.split(" ")
        src = Node(lineinfo[0])
        dest = Node(lineinfo[1])
        time = int(lineinfo[2])
        roadtype = lineinfo[3]
        #use try except blocks to add to road_map, but not stopping altogether if ValueError is encountered
        try:
            road_map.add_node(src)            
        except ValueError:
            pass
        
        try:
            road_map.add_node(dest) 
        except ValueError:
            pass
        #add road both ways
        road = DirectedRoad(src,dest,time,roadtype.rstrip())
        road2 = DirectedRoad(dest,src,time,roadtype.rstrip())
        
        road_map.add_road(road)
        road_map.add_road(road2)
        
    return road_map

#print(load_map("test_load_map.txt"))
# PROBLEM 2c: Testing load_map
# Line to test load map: 77


# PROBLEM 3: Finding the Shortest Path using Optimized Search Method
#
# PROBLEM 3a: Objective function
#
# What is the objective function for this problem? What are the constraints?
#
# ANSWER: The objective function is finding a valud path from start to end that minimizes the 
# sum of the edge weights (minutes) from start to end. This means finding a route from start
    #to end with the smallest total time travelled. The constraint is that the best must 
    #be valid (a road/edge must exist between all nodes in path) and it cannot include roads that are 
    #restricted. We also have to take traffic into consideration.


# PROBLEM 3b: Implement get_optimal_path
def get_optimal_path(roadmap, start, end, restricted_roads, in_traffic=False):
    """
    Finds the shortest path between nodes subject to constraints.

    Parameters:
    roadmap - RoadMap
        The graph on which to carry out the search
    start - Node
        node at which to start
    end - Node
        node at which to end
    restricted_roads - list[strings]
        Road Types not allowed on path
    in_traffic - boolean
        flag to indicate whether to get shortest path during heavy or normal traffic 

    Returns:
    A tuple of the form (best_path, best_time).
        The first item is the shortest-path from start to end, represented by
        a list of nodes (Nodes).
        The second item is an integer, the length (time traveled)
        of the best path.

    If there exists no path that satisfies constraints, then return None.
    """
    nodes = roadmap.get_all_nodes() #all nodes
    unvisited = roadmap.get_all_nodes() #all unvisited nodes
    distanceTo = {node:float('inf') for node in roadmap.get_all_nodes()} #dict from node -> distanceTo from start
    predecessor = {node:None for node in roadmap.get_all_nodes()}#dict from node -> predecessor
    distanceTo[start] = 0
    
    if not start in nodes or not end in nodes: 
        return None
    
    if start == end: #if already done, return path and 0
        return ([start],0)
    
    while unvisited: #while there are still unvisited nodes, loop continues
        
        #choose node with smallest distance from start as current
        current_node = min(unvisited, key=lambda node:distanceTo[node])
        
        #if all are infinitely away, path is not possible
        if distanceTo[current_node]=='inf':
            return None
        #search through roads from current node
        for road in roadmap.get_roads_for_node(current_node,restricted_roads):
            #update alt path time
            altPathTime = distanceTo[current_node] + road.get_total_time(in_traffic)
            
            #if alt path time is better than neighbor's current path time, update
            if altPathTime < distanceTo[road.get_destination()]:
                distanceTo[road.get_destination()] = altPathTime
                predecessor[road.get_destination()] = current_node
         #remove current node from unvisited       
        unvisited.remove(current_node)
    
    #now that all nodes have been visited and all optimal path times have been found, find path
    path = []
    current=end
    while predecessor[current]!=None:
        path.insert(0,current)
        current=predecessor[current]
    if path != []: #insert start into index 0
        path.insert(0,current)
    else:
        return None
    return (path,distanceTo[end])

# PROBLEM 4a: Implement optimal_path_no_traffic
def optimal_path_no_traffic(filename, start, end):
    """
    Finds the shortest path from start to end during ideal traffic conditions.

    You must use get_optimal_path and load_map.

    Parameters:
    filename - name of the map file that contains the graph
    start - Node, node object at which to start
    end - Node, node object at which to end
    
    Returns:
    list of Node objects, the shortest path from start to end in normal traffic.
    If there exists no path, then return None.
    """
    return get_optimal_path(load_map(filename),start,end,[])[0]

# PROBLEM 4b: Implement optimal_path_restricted
def optimal_path_restricted(filename, start, end):
    """
    Finds the shortest path from start to end when local roads cannot be used.
    Assume there is NO traffic.

    You must use get_optimal_path and load_map.

    Parameters:
    filename - name of the map file that contains the graph
    start - Node, node object at which to start
    end - Node, node object at which to end
    
    Returns:
    list of Node objects, the shortest path from start to end given the aforementioned conditions,
    If there exists no path that satisfies constraints, then return None.
    """
    return get_optimal_path(load_map(filename),start,end,["local"])[0]

# PROBLEM 4c: Implement optimal_path_heavy_traffic
def optimal_path_heavy_traffic(filename, start, end):
    """
    Finds the shortest path from start to end in heavy traffic,
    i.e. when local roads take twice as long. 

    You must use get_optimal_path and load_map.

    Parameters:
    filename - name of the map file that contains the graph
    start - Node, node object at which to start
    end - Node, node object at which to end; you may assume that start != end
    
    Returns:
    The shortest path from start to end given the aforementioned conditions, 
    represented by a list of nodes (Nodes).

    If there exists no path that satisfies the constraints, then return None.
    """
    return get_optimal_path(load_map(filename),start,end,[],True)[0]

def __main__():
    pass

     # do not delete or comment out this pass statement
    
    # UNCOMMENT THE FOLLOWING LINES TO DEBUG
    

    #rmap = load_map('road_map.txt')
    #start = Node('N0')
   # end = Node('N9')
   # restricted_roads = ['']
    #
   # print(get_optimal_path(rmap, start, end, restricted_roads))