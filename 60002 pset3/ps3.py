# -*- coding: utf-8 -*-
# Problem Set 3: Simulating robots
# Name: Richter Jordaan
# Collaborators (discussion): None
# Time: 4:00

import math
import random
import matplotlib
#matplotlib.use("TkAgg")

from ps3_visualize import *
import pylab

# === Provided class Position, do NOT change
class Position(object):
    """
    A Position represents a location in a two-dimensional room, where
    coordinates are given by floats (x, y).
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_new_position(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.get_x(), self.get_y()

        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))

        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y

        return Position(new_x, new_y)

    def __str__(self):
        return "Position: " + str(math.floor(self.x)) + ", " + str(math.floor(self.y))

# === Problem 1
class BasicRoom(object):
    """
    A BasicRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. Each tile
    has some fixed amount of dirt. The tile is considered clean only when the amount
    of dirt on this tile is 0.
    """
    def __init__(self, width, height, dirt_amount):
        """
        Initializes a rectangular room with the specified width, height, and
        dirt_amount on each tile.

        width: an integer > 0
        height: an integer > 0
        dirt_amount: a float >= 0
        """
        self.width=width
        self.height=height
        self.dirt_amounts={}
        #create dictionary to store dirt amount for each tile
        #key in dictionary is tuple, tile, and val is that tile's dirt amount
        self.dirt_amounts = {}
        for xpos in range(width):
            for ypos in range(height):
                self.dirt_amounts[(xpos,ypos)] = dirt_amount

    def get_dirt_amount(self, m, n):
        """
        Return the amount of dirt on the tile (m, n)

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer

        Returns: a float
        """
        return self.dirt_amounts[(m,n)]

    def clean_tile_at_position(self, pos, capacity):
        """
        Mark the tile under the position pos as cleaned by capacity amount of dirt.

        Assumes that pos represents a valid position inside this room.

        pos: a Position object
        capacity: an integer, the amount of dirt to be cleaned in a single time-step
                  can be negative which would mean adding dirt to the tile

        Note: The amount of dirt on each tile should be NON-NEGATIVE.
              If the capacity exceeds the amount of dirt on the tile, mark it as 0.
        """
        x = math.floor(pos.get_x())
        y = math.floor(pos.get_y())
        
        if capacity<0:#if adding dirt, add abs value of capacity
            self.dirt_amounts[(x,y)]+=abs(capacity)
        else: #if capacity > dirt amount, mark it as 0
            self.dirt_amounts[(x,y)]=max(0,self.dirt_amounts[(x,y)]-capacity)

    def is_tile_cleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer

        Returns: True if the tile (m, n) is cleaned, False otherwise

        Note: The tile is considered clean only when the amount of dirt on this
              tile is 0.
        """
        return self.dirt_amounts[(m,n)]==0

    def get_num_cleaned_tiles(self):
        """
        Returns: an integer; the total number of clean tiles in the room
        """
        clean_count = 0 #num of clean tiles
        for tile in self.dirt_amounts.keys():#check all tiles and see if it is clean
            if self.is_tile_cleaned(tile[0],tile[1]):
                clean_count+=1
        return clean_count

    def is_position_in_room(self, pos):
        """
        Determines if pos is inside the room.

        pos: a Position object.
        Returns: True if pos is in the room, False otherwise.
        """
        x = pos.get_x()
        y = pos.get_y()
        return x>=0 and y>=0 and math.floor(x)<=self.width-1 and math.floor(y)<=self.height-1

    def get_num_tiles(self):
        """
        Returns: an integer; the total number of tiles in the room
        """
        return self.width*self.height

    def get_random_position(self):
        """
        Returns: a Position object; a random position inside the room
        """
        return Position(random.random()*self.width,random.random()*self.height)


class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times, the robot has a particular position and direction in the room.
    The robot also has a fixed speed and a fixed cleaning capacity.

    Subclasses of Robot should provide movement strategies by implementing
    update_position_and_clean, which simulates a single time-step.
    """
    def __init__(self, room, speed, capacity):
        """
        Initializes a Robot with the given speed and given cleaning capacity in the
        specified room. The robot initially has a random direction and a random
        position in the room.

        room:  a BasicRoom object.
        speed: a float (speed > 0)
        capacity: a positive integer; the amount of dirt cleaned by the robot
                  in a single time-step
        """
        self.room = room
        self.speed = speed
        self.capacity = capacity
        #store pos over time, initially random
        self.pos = room.get_random_position()
        #store direction over time, initially random
        self.direction = random.random()*360

    def get_robot_position(self):
        """
        Returns: a Position object giving the robot's position in the room.
        """
        return self.pos

    def get_robot_direction(self):
        """
        Returns: a float d giving the direction of the robot as an angle in
        degrees, 0.0 <= d < 360.0.
        """
        return self.direction

    def set_robot_position(self, position):
        """
        Set the position of the robot to position.

        position: a Position object.
        """
        self.pos = position

    def set_robot_direction(self, direction):
        """
        Set the direction of the robot to direction.

        direction: float representing an angle in degrees
        """
        self.direction = direction

    def update_position_and_clean(self):
        """
        Simulates the passage of a single time-step.

        Moves robot to new position and cleans tile according to robot movement
        rules.
        """
        # do not change -- implement in subclasses
        raise NotImplementedError

# === Problem 2
class ClassicRobot(Robot):
    """
    A ClassicRobot is a Robot with the standard movement strategy.

    At each time-step, a ClassicRobot attempts to move in its current
    direction; when it would hit a wall, it *instead*
    chooses a new direction randomly.
    """
    def update_position_and_clean(self):
        """
        Simulates the passage of a single time-step.

        Calculate the next position for the robot.

        If that position is valid, move the robot to that position. Mark the
        tile it is on as having been cleaned by capacity amount.

        If the new position is invalid, do not move or clean the tile, but
        rotate once to a random new direction.
        """
        #calculate new position and see if it's valid
        new_pos =self.get_robot_position().get_new_position(self.get_robot_direction(),self.speed)
        if self.room.is_position_in_room(new_pos):
            self.set_robot_position(new_pos)#update pos
            self.room.clean_tile_at_position(new_pos,self.capacity) #clean new tile
        else: #not a valid new position
            self.set_robot_direction(random.random()*360)

# Uncomment this line to see your implementation of ClassicRobot in action!
#test_robot_movement(ClassicRobot, BasicRoom)

# === Problem 3
class MalfunctioningRobot(Robot):
    """
    A MalfunctioningRobot is a robot that may accidentally dirty a tile. A MalfunctioningRobot will
    drop some dirt on the tile it's on and pick a new, random direction for itself
    with probability p. If the robot does drop dirt, the amount of dropped dirt should be a
    decimal value between 0 and 0.5. Afterwards, the robot will behave exactly like the ClassicRobot
    by attempting to move to a new tile and clean it.
    """
    p = 0.05

    @staticmethod
    def set_dirt_probability(prob):
        """
        Sets the probability of the robot accidentally dirtying the tile equal to prob.

        prob: a float (0 <= prob <= 1)
        """
        MalfunctioningRobot.p = prob

    def dropping_dirt(self):
        """
        Answers the question: Does the robot accidentally drop dirt on the tile
        at this timestep?
        The robot drops dirt with probability p.

        returns: True if the robot drops dirt on its tile, False otherwise.
        """
        return random.random() < MalfunctioningRobot.p

    def update_position_and_clean(self):
        """
        Simulates the passage of a single time-step.

        Check if the robot accidentally releases dirt. If so, dirty the current tile
        by a random decimal value between 0 (inclusive) and 0.5 (exclusive) and change
        its direction randomly.

        Calculate the next position for the robot regardless if the robot releases dirt or not.

        If that position is valid, move the robot to that position. Mark the tile it moved to
        as having been cleaned by capacity amount.

        If it is not a valid position, the robot should change to a random direction.

        """
        #check if released dirt
        if self.dropping_dirt():
            #dirty current tile
            self.room.clean_tile_at_position(self.get_robot_position(),random.random()*-0.5)
            self.set_robot_direction(random.random()*360)
        
        #calculate new position and see if it's valid
        new_pos =self.get_robot_position().get_new_position(self.get_robot_direction(),self.speed)
        if self.room.is_position_in_room(new_pos):
            self.set_robot_position(new_pos)#update pos
            self.room.clean_tile_at_position(new_pos,self.capacity) #clean new tile
        else: #not a valid new position
            self.set_robot_direction(random.random()*360)

# Uncomment this line to see your implementation of MalfunctioningRobot in action!
#test_robot_movement(MalfunctioningRobot, BasicRoom)


# === Problem 4
class BetterRobot(Robot):
    """
    A BetterRobot is a robot that moves extra fast and can clean two tiles in one
    timestep.

    It moves in its current direction, cleans the tile it lands on, and continues
    moving in that direction and cleans the second tile it lands on, all in one
    unit of time.

    If the BetterRobot hits a wall when it attempts to move in its current direction,
    it may dirty the current tile by one unit because it moves very fast and can
    knock dust off of the wall.

    """
    p = 0.15

    @staticmethod
    def set_dirty_probability(prob):
        """
        Sets the probability of getting the tile dirty equal to PROB.

        prob: a float (0 <= prob <= 1)
        """
        BetterRobot.p = prob

    def dropping_dirt(self):
        """
        Answers the question: Does the robot accidentally drop dirt on the tile
        at this timestep?
        The robot drops dirt with probability p.

        returns: True if the robot drops dirt on its tile, False otherwise.
        """
        return random.random() < BetterRobot.p

    def update_position_and_clean(self):
        """
        Simulates the passage of a single time-step.

        Within one time step (i.e. one call to update_position_and_clean), there are
        three possible cases:

        1. The next position in the current direction at the robot's given speed is
           not a valid position in the room, so the robot stays at its current position
           without cleaning the tile. The robot then turns to a random direction.

        2. The robot successfully moves forward one position in the current direction
           at its given speed. Let's call this Position A. The robot cleans Position A.
           The next position in the current direction is not a valid position in the
           room, so it does not move to the new location. With probability p, it dirties
           Position A by 1. Regardless of whether or not the robot dirties Position A,
           the robot will turn to a random direction.

        3. The robot successfully moves forward two positions in the current direction
           at its given speed. It cleans each position that it lands on.
        """

        #calculate new position and see if it's valid
        pos_a =self.get_robot_position().get_new_position(self.get_robot_direction(),self.speed)
        
        if self.room.is_position_in_room(pos_a):#case 2 or 3
            self.set_robot_position(pos_a)#update pos
            self.room.clean_tile_at_position(pos_a,self.capacity) #clean new tile
            
            #see if position B is valid
            pos_b = self.get_robot_position().get_new_position(self.get_robot_direction(),self.speed)
            if self.room.is_position_in_room(pos_b): #case 3
                self.set_robot_position(pos_b)#update pos
                self.room.clean_tile_at_position(pos_b,self.capacity) #clean new tile
            else: #case 2
                if self.dropping_dirt():
                    self.room.clean_tile_at_position(pos_a,-1)#add dirt
                self.set_robot_direction(random.random()*360)
        else:
            self.set_robot_direction(random.random()*360) #case 1


# Uncomment this line to see your implementation of BetterRobot in action!
#test_robot_movement(BetterRobot, BasicRoom)

# === Problem 5
def run_simulation(num_robots, speed, capacity, width, height, dirt_amount, min_coverage, num_trials,
                  robot_type):
    """
    Runs num_trials trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction min_coverage of the room.

    The simulation is run with num_robots robots of type robot_type, each
    with the input speed and capacity in a room of dimensions width x height
    with the dirt dirt_amount on each tile. Each trial is run in its own BasicRoom
    with its own robots.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    capacity: an int (capacity >0)
    width: an int (width > 0)
    height: an int (height > 0)
    dirt_amount: an int
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. ClassicRobot or
                MalfunctioningRobot)
    """
    step_counts = [] #number of steps for different experiments
    for trial in range(num_trials):
        num_steps = 0#count number of steps for this trial
        room = BasicRoom(width,height,dirt_amount)#create room that all robots will operate on
        robotList =[robot_type(room,speed,capacity) for robot in range(num_robots)]#list of robots
        while (float)(room.get_num_cleaned_tiles())/room.get_num_tiles() < min_coverage:#while not clean, update and clean for all robots
            num_steps+=1#increment steps
            for robot in robotList:#update and clean for all robots
                robot.update_position_and_clean()   
        step_counts.append(num_steps)#append result of trial to stepcount list
    return (float)(sum(step_counts))/num_trials #return float version of avg steps

#print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 5, 5, 3, 1.0, 50, ClassicRobot)))
#print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 10, 10, 3, 0.8, 50, ClassicRobot)))
#print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 10, 10, 3, 0.9, 50, ClassicRobot)))
#print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 20, 20, 3, 0.5, 50, ClassicRobot)))
#print ('avg time steps: ' + str(run_simulation(3, 1.0, 1, 20, 20, 3, 0.5, 50, ClassicRobot)))

# === Problem 6
#
# ANSWER THE FOLLOWING QUESTIONS:
#
# 1)How does the performance of the three robot types compare when cleaning 80%
#       of a 20x20 room?
#The BetterRobot is the quickest, then the ClassicRobot, and then the MalfunctioningRobot.
#The Classic and Malfunctioning Robots are much closer together in average time compared to the gap
#between BetterRobot and ClassicRobot, especially when the number of robots is relatively small.
#In fact, when the number of robots is at 10, ClassicRobot and Malfunctioning Robot are almost equivalent,
#and the gap between BetterRobot and ClassicRobot is smallest. All three seem to be converging as the number
#of robots increases and increases.
#
# 2) How does the performance of the three robot types compare when two of each
#       robot cleans 80% of rooms with dimensions
#       10x30, 20x15, 25x12, and 50x6?
#The aspect ratio is defined as width/height, and the aspect ratios (1/3),(4/3),(2.08),(8.33)
#are shown on the x axis of the graph. We see that the BetterRobot is by far the quickest, followed
#by the Classic Robot and then lastly the MalfunctioningRobot is the least quick. What's different
#about this graph compared to the last is that there seems to be a linear increase in time as 
#aspect ratio increases, and also line is very flat. At first, when the aspect ratio changes from 
#1/3 to 4/3m the time decreases, but then is seems to gradually rise and rise. Once again, the difference
#in speed between the classic robot and the malfunctioning robot is much smaller than the difference
#between the malfunctioning robot and the better robot.
#

def show_plot_compare_strategies(title, x_label, y_label):
    """
    Produces a plot comparing the three robot strategies in a 20x20 room with 80%
    minimum coverage.
    """
    num_robot_range = range(1, 11)
    times1 = []
    times2 = []
    times3 = []
    for num_robots in num_robot_range:
        print ("Plotting", num_robots, "robots...")
        times1.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, ClassicRobot))
        times2.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, MalfunctioningRobot))
        times3.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, BetterRobot))
    pylab.plot(num_robot_range, times1)
    pylab.plot(num_robot_range, times2)
    pylab.plot(num_robot_range, times3)
    pylab.title(title)
    pylab.legend(('ClassicRobot', 'MalfunctioningRobot', 'BetterRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()

def show_plot_room_shape(title, x_label, y_label):
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    aspect_ratios = []
    times1 = []
    times2 = []
    times3 = []
    for width in [10, 20, 25, 50]:
        height = int(300/width)
        print ("Plotting cleaning time for a room of width:", width, "by height:", height)
        aspect_ratios.append(float(width) / height)
        times1.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, ClassicRobot))
        times2.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, MalfunctioningRobot))
        times3.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, BetterRobot))
    pylab.plot(aspect_ratios, times1, 'o-')
    pylab.plot(aspect_ratios, times2, 'o-')
    pylab.plot(aspect_ratios, times3, 'o-')
    pylab.title(title)
    pylab.legend(('ClassicRobot', 'MalfunctioningRobot', 'BetterRobot'), fancybox=True, framealpha=0.5)
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()


#show_plot_compare_strategies('Time to clean 80% of a 20x20 room, for various numbers of robots','Number of robots','Time (steps)')
#show_plot_room_shape('Time to clean 80% of a 300-tile room for various room shapes','Aspect Ratio', 'Time (steps)')