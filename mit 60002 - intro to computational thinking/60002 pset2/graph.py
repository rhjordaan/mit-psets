# 6.0002 Problem Set 2 Spring 2020
# Graph Optimization
# Name: Richter Jordaan
# Collaborators: None
# Time: 2:00


# This file contains a set of data structures to represent the graphs 
# that you will be using for this pset.

class Node():
    """Represents a node in the graph"""

    def __init__(self, name):
        """ 
        Initializes  an instance of Node object.

        Parameters: 
        name - object representing the name of the node             
        """
        self.name = str(name)

    def get_name(self):
        """ 
        Returns: 
        str, representing the name of the node 
        """
        return self.name

    def __str__(self):
        """ 
        This is the function that is called when print(node) is called.

        Returns: 
        str, humanly readable reprsentation of the node
        """
        return self.name

    def __repr__(self):
        """ 
        Formal string representation of the node

        Returns: 
        str, the name of the node.
        """
        return self.name

    def __eq__(self, other):
        """ 
        This is function called when you use the "==" operator on nodes

        Parameters:
        other - Node object to compare against 

        Returns: 
        bool, True is self == other, false otherwise
        """
        if not isinstance(other, Node):
            return False
        return self.name == other.name

    def __ne__(self, other):
        """ 
        This is function called when you used the "!=" operator on nodes

        Parameters:
        other - Node object to compare against 

        Returns: 
        bool, True is self != other, false otherwise
        """
        return not self.__eq__(other)

    def __hash__(self):
        """
        Returns: 
        Hash of the node. This function is necessary so that Nodes can be 
        used as keys in a dictionary, Nodes are immutable
        """
        return self.name.__hash__()


# PROBLEM 1: Implement this class based on the given docstring.
class DirectedRoad():
    """Represents a road (edge) with an integer time (weight)"""

    def __init__(self, src, dest, total_time, road_type):
        """ 
        Initialize src, dest, total_time, and road_type for the DirectedRoad class. 
        Assume road_type is one of local, brige, interstate, arterial
        
        Parameters: 
        src: Node, representing the source node
        dest: Node, representing the destination node
        total_time: int, representing the time (in minutes) travelled between the src and dest
        road_type: str, representing the type of road of the edge. 
        """
        self.src =src
        self.dest=dest
        self.total_time=total_time
        self.road_type=road_type

    def get_source(self):
        """ 
        Getter method for DirectedRoad

        Returns: 
        Node, representing the source node 
        """
        return self.src

    def get_destination(self):
        """ 
        Getter method for DirectedRoad

        Returns: 
        Node, representing the destination node 
        """
        return self.dest

    def get_type(self):
        """ 
        Getter method for DirectedRoad

        Returns:
        str, representing the road type of the road
        """
        return self.road_type

    def get_total_time(self, in_traffic=False):
        """ 
        Gets the total_time for this road. In traffic conditions:
        - all the local roads take twice as long.
        - all other road types take the same amount of time

        Paramater:
        in_traffic - bool, True if there is traffic, False otherwise  
        
        Returns: 
        int, representing the time travelled between the source and dest nodes
        """
        return 2*self.total_time if in_traffic and self.road_type == "local" else self.total_time



    def __str__(self):
        """ 
        Function that is called when print() is called on a DirectedRoad object.
        
        Returns: 
        str, with the format 'src -> dest takes total_time minute(s) via road_type road' 
        
        Note: For the total time assume normal traffic conditions
        """
        return str(self.src.get_name()) + " -> " + str(self.dest.get_name()) + " takes " + str(self.total_time) + " minute(s) via " + str(self.road_type) + " road"

    def __hash__(self):
        return self.__str__().__hash__()

# PROBLEM 1: Implement methods of this class based on the given docstring.
# DO NOT CHANGE THE FUNCTIONS THAT HAVE BEEN IMPLEMENTED FOR YOU.
class RoadMap():
    """Represents a road map -> a directed graph of Node and DirectedRoad objects"""

    def __init__(self):
        """
        Initalizes a new instance of RoadMap.
        """
        self.nodes = set()
        self.roads = {}  # must be a dictionary of Node -> list of roads starting at that node

    def __str__(self):
        """
        Function that is called when print() is called on a RoadMap object.
        
        Returns: 
        str, representation of the RoadMap.  
        """
        road_strs = []
        for roads in self.roads.values():
            for road in roads:
                road_strs.append(str(road))
        road_strs = sorted(road_strs)  # sort alphabetically
        return '\n'.join(road_strs)  # concat road_strs with "\n"s between them

    def get_roads_for_node(self, node, restricted = []):
        ''' 
        Parameters: 
        node: Node object, 
        restricted: list of road types that are ristricted

        Returns: 
        a copy of the list of all of the roads for given node whose type 
        is not in the restricted list.empty list if the node is not in the graph. 
        '''
        #use list comprehension
        return [] if not node in self.nodes else [road for road in self.roads[node] if not road.get_type() in restricted]

    def get_all_nodes(self):
        """
        Return:
        a COPY of all nodes in the RoadMap. Does not modify self.nodes
        """
        return self.nodes.copy()

    def has_node(self, node):
        """ 
        Param: 
        node object
        
        Return: 
        True, if node is in the graph. False, otherwise.
        """
        return node in self.nodes

    def add_node(self, node):
        """ 
        Adds a Node object to the RoadMap.
        Raises a ValueError if it is already in the graph.

        Param: 
        node object
        """
        #raise ValueError if node already in set of nodes
        if self.has_node(node):
            raise ValueError
        else: #otherwise add node and create empty list as corresponding value in dict
            self.nodes.add(node)
            self.roads[node]=[]

    def add_road(self, road):
        """ 
        Adds a DirectedRoad instance to the RoadMap.
        Raises a ValueError if either of the nodes associated with the road is not in the graph.

        Param: 
        road, DirectedRoad object
        """
        if road.get_source() not in self.nodes or road.get_destination() not in self.nodes:
            raise ValueError #raise ValueError if src or dest are not in set of ndoes
        else:
            self.roads[road.get_source()].append(road) #otherwise append road to list of roads from node
            
    