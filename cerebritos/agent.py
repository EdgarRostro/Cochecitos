from mesa import Agent
from math import sqrt

def distanceBetweenPoints(point1, point2):
    return sqrt( pow(point1[0] - point2[0], 2) + pow(point1[1] + point2[1], 2))

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
        

    def move(self):
        """ 
        Determines if the agent can move in the direction that was chosen
        """
        cell = self.model.grid[self.pos[0]][self.pos[1]]
        # possible_steps = self.model.grid.get_neighborhood(
        #     self.pos,
        #     moore=True, # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
        #     include_center=True) 
        
        # # Checks which grid cells are empty
        # freeSpaces = list(map(self.model.grid.is_cell_empty, possible_steps))

        # next_moves = [p for p,f in zip(possible_steps, freeSpaces) if f == True]
       
        # next_move = self.random.choice(next_moves)
        # # Now move:
        # if self.random.random() < 0.1:
        #     self.model.grid.move_agent(self, next_move)
        #     self.steps_taken+=1

        # If the cell is empty, moves the agent to that cell; otherwise, it stays at the same position
        # if freeSpaces[self.direction]:
        #     self.model.grid.move_agent(self, possible_steps[self.direction])
        #     print(f"Se mueve de {self.pos} a {possible_steps[self.direction]}; direction {self.direction}")
        # else:
        #     print(f"No se puede mover de {self.pos} en esa direccion.")                

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

    def goToCoords(self, target):
        """
        Returns the coords of the cell to go to next in order to arrive at target (tuple). Ignores obstacles
        """
        # Do nothing if target == pos
        if target == self.pos:
            return
        # Get current road cell (or traffic light cell) (asume road agent is ALWAYS @0)
        currentRoadAgent = self.model.grid[self.pos[0]][self.pos[1]][0]
        # Get current road cell directions
        currentRoadAgentDirections = currentRoadAgent.directions
        # Store here coords nearest to target
        nearestCoods = None
        # Get available neighbors
        for direction in currentRoadAgentDirections:
            coords = self.getDirection(direction)
            # Check if distance is bigger than that of nearest coords
            if nearestCoods != None and distanceBetweenPoints(nearestCoods, target) < distanceBetweenPoints(coords, target):
                continue
            # Check if cell is an obstacle
            if self.isObstacle(coords):
                continue
            # If all pasaes, change nearest coords
            nearestCoods = coords
        # Return coordinates
        return nearestCoods

    def step(self):
        """ 
        Determines the new direction it will take, and then moves
        """
        # self.direction = self.random.randint(0,8)
        # print(f"Agente: {self.unique_id} movimiento {self.direction}")
        # self.move()
        pass

class Traffic_Light(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model, state = "Red"):
        super().__init__(unique_id, model)
        # Possible states: Red, Yellow, Green
        self.state = state
        self.directions = []
    def step(self):
        # if self.model.schedule.steps % self.timeToChange == 0:
        #     self.state = not self.state
        pass

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
