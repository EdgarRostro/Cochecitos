from mesa import Agent
from math import sqrt

def distanceBetweenPoints(point1, point2):
    return sqrt( pow(point1[0] - point2[0], 2) + pow(point1[1] + point2[1], 2))


class Traffic_Light(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model, letter, direction):
        super().__init__(unique_id, model)
        # Possible states: Red, Yellow, Green
        # Red if uppercase, green if lowercase
        if letter.isupper():
            self.state = "Red"
        else:
            self.state = "Green"
        self.directions = direction
    
    def step(self):
        # if self.model.schedule.steps % self.timeToChange == 0:
        #     self.state = not self.state
        pass

class Car(Agent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID 
        direction: Randomly chosen direction chosen from one of eight directions
    """
    def __init__(self, unique_id, model, destination):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        super().__init__(unique_id, model)
        self.is_parked = False
        self.destination = destination
        self.directionLight = None
    
    def assignDirection(self):
        self.oldDirection = self.model.grid[self.pos[0]][self.pos[1]][0].directions[0]

    def move(self):
        """ 
        Determines if the agent can move in the direction that was chosen
        """
        # Check if car has arrived to destination
        if self.destination in self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False):
            self.model.grid.move_agent(self, self.destination)
            self.is_parked = True
            return

        currentCell = self.model.grid[self.pos[0]][self.pos[1]]
        # Next cell
        (x, y, self.newDirection) = self.goToCoords(self.destination, self.pos)
        # If traffic light is ahead and is not green, do not move...
        if isinstance(currentCell[0], Traffic_Light):
            if currentCell[0].state != "Green":
                return
        
        self.intention = (x,y)
        
    def getDirection(self, direction):
        """
        Returns coordinates in the given direction
        """
        if direction == "Left":
            return (self.pos[0]-1, self.pos[1])
        elif direction == "Right":
            return (self.pos[0]+1, self.pos[1])
        elif direction == "Up":
            return (self.pos[0], self.pos[1]+1)
        else:
            return (self.pos[0], self.pos[1]-1)
    
    def isObstacle(self, cell):
        """
        Returns true if given cell is an obstacle (unparked car, Obstacle object)
        """
        agents = self.model.grid[cell[0]][cell[1]]
        for agent in agents:
            if isinstance(agent, Car):
                if agent.is_parked:
                    return False
                else:
                    return True
            if isinstance(agent, Obstacle):
                return True
        return False

    def goToCoords(self, target, start):
        """
        Returns the coords of the cell to go to next in order to arrive at target (tuple). Ignores obstacles
        """
        if target == start:
            return (target[0], target[1], self.oldDirection)
        # Get current road cell (or traffic light cell) (asume road agent is ALWAYS @0)
        currentRoadAgent = self.model.grid[start[0]][start[1]][0]
        # Get current road cell directions
        currentRoadAgentDirections = currentRoadAgent.directions
        # Store here coords nearest to target
        nearestCoords = self.pos
        nextDirection = self.oldDirection
        # Get available neighbors
        for direction in currentRoadAgentDirections:
            coords = self.getDirection(direction)
            # Check if distance is bigger than that of nearest coords (only in intersections)
            # if len(currentRoadAgentDirections)>1 and distanceBetweenPoints(nearestCoords, target) < distanceBetweenPoints(coords, target):
            if len(currentRoadAgentDirections) < 1 and distanceBetweenPoints(nearestCoords, target) > distanceBetweenPoints(coords, target):
                continue
            # Check if cell is an obstacle
            if self.isObstacle(coords):
                continue
            # If all passes, change nearest coords
            nearestCoords = coords
            nextDirection = direction
        # Return coordinates
        print('Estoy en ('+str(self.pos)+') y voy a (' + str(self.destination) + ')')
        return (nearestCoords[0], nearestCoords[1], nextDirection)
    
    def turnOnBlinkers(self):
        """
        Compares old direction and new direction to turn on/off blinkers
        """
        if self.oldDirection == self.newDirection:
            self.directionLight = (0,0)
            return

        turns = {
            "Up" : {
                "Left" : (1, 0),
                "Right" : (0, 1)
            },
            "Down" : {
                "Right" : (1, 0),
                "Left" : (0, 1)
            },
            "Left" : {
                "Up" : (0, 1), 
                "Down": (1, 0)
            }, 
            "Right": {
                "Up" : (1, 0),
                "Down" : (0, 1)
            }
        }
        """
                up  down    left    right
        up      x   x       r       l
        down    x   x       l       r
        left    r   l       x       x
        right   l   r       x       x
        """ 
        self.directionLight = turns[self.oldDirection][self.newDirection]


    def step(self):
        """ 
        Determines the new direction it will take
        """
        # Only moves if it isn't parked
        if self.is_parked:
            return
        self.move()
    
    def advance(self):
        """
        Moves based on new direction (executes after step)
        """

        # Only moves if it isn't parked
        if self.is_parked:
            return
            
        # Checks neighbour's intentions
        neighbors = self.model.grid.get_neighbors(self.pos, include_center=False, moore=True)
        diagonalNeighbors = filter(lambda agent: agent.pos[0] != self.pos[0] and agent.pos[1] != self.pos[1], neighbors)
        shouldMove = True
        for agent in diagonalNeighbors:
            if isinstance(agent, Car) and agent.intention == self.intention:
                # Prioritise the one going straight
                if agent.oldDirection == agent.newDirection:
                    # Self should NOT move 
                    shouldMove = False
                    break
        
        if shouldMove:
            # Move to next cell and update direction
            self.model.grid.move_agent(self, self.intention)
            self.oldDirection = self.newDirection
        else:
            # Turn on blinkers
            self.turnOnBlinkers()

class Destination(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

class Obstacle(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

class Road(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model, directions=["Left"]):
        super().__init__(unique_id, model)
        # Create a set of directions to allow for multidirectional road cells
        self.directions = directions

    def step(self):
        pass
