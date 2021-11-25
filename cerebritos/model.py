from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from agent import *
import json

class RandomModel(Model):
    """ 
    Creates a new model with random agents.
    Args:
        N: Number of agents in the simulation
        height, width: The size of the grid to model
    """
    def __init__(self, N):

        dataDictionary = json.load(open("mapDictionary.txt"))

        with open('base.txt') as baseFile:
            lines = baseFile.readlines()
            self.width = len(lines[0])-1
            self.height = len(lines)

            self.grid = MultiGrid(self.width, self.height,torus = False) 
            self.schedule = RandomActivation(self)

            destinations = []

            for r, row in enumerate(lines):
                for c, col in enumerate(row):
                    if col in ["v", "^", ">", "<", "≤", "⋜", "≥", "⋝"]:
                        agent = Road(f"r{r*self.width+c}", self, dataDictionary[col])
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                    elif col in ["ú", "ù", "Û", "Ǔ"]:
                        agent = Traffic_Light(f"tl{r*self.width+c}", self, "Red" if col == "S" else "Green")
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.schedule.add(agent)
                    elif col == "#":
                        agent = Obstacle(f"ob{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                    elif col == "D":
                        agent = Destination(f"d{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        destinations.append((c, self.height - r - 1))

        # Add cars with their destinations
        for i in range(N):
            agent_amt = 3

            while agent_amt > 1:
                x = self.random.randint(0, self.width)
                y = self.random.randint(0, self.height)
                agent_amt = self.grid[x][y]
            
            agent = Car(f"c{i}", self, self.random.choice(destinations))
            self.grid.place_agent(agent, (x,y))
        

        self.running = True 

    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()

        # Change stoplights every ten steps
        if self.schedule.steps % 10 == 0:
            for agent in self.schedule.agents:
                if isinstance(agent, Traffic_Light):
                    # Change reds to green
                    if agent.state == "Red":
                        agent.state = "Green"
                    # Change yellows to red
                    else:
                        agent.state = "Red"

        # Change green lights to yellow
        elif self.schedule.steps % 10 == 9:
            for agent in self.schedule.agents:
                if isinstance(agent, Traffic_Light):
                    if agent.state == "Green":
                        agent.state = "Yellow"