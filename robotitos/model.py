from random import shuffle
from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from agents import Cell, Robot, Box

class Room(Model):
    def __init__(self, width, height, density, robots, timer):
        self.pile = (1,0)
        self.pile_size = 0

        self.schedule = RandomActivation(self)

        self.grid = MultiGrid(width, height, torus=False)
        self.running = True
        self.timer = 0
        self.timeLimit = timer
        # self.steps = 0
        id = 0

        # Poner celdas en todo el grid
        for(contents, x, y) in self.grid.coord_iter():
            cell = Cell(id, self)
            self.grid.place_agent(cell, (x, y))
            self.schedule.add(cell)
            id += 1
        # Agregar cajas (según densidad)
        for (contents, x, y) in self.grid.coord_iter():
            if self.random.random() < density and not (x in [0, 1] and y == 0):
                new_box = Box(id, self)
                self.grid.place_agent(new_box, (x, y))
                self.schedule.add(new_box)
                id += 1
        
        # Poner cantidad necesaria de robots
        for i in range(robots):
            new_robot = Robot(id, self)
            self.grid.place_agent(new_robot, (self.random.randint(0, width - 1), self.random.randint(0, height - 1)))
            self.schedule.add(new_robot)
            id += 1
    
    def check_pile(self):
        self.pile_size += 1
        if self.pile_size >= 5:
            new_coords = int(self.pile[0]), self.pile[1]+1
            if self.grid.out_of_bounds(new_coords):
                new_coords = self.pile[0]+1, int(0)
            self.pile = new_coords
            self.pile_size = 0
            
    def step(self):
        self.schedule.step()
        count = 0
        self.timer += 1
        if self.timer >= self.timeLimit:
            self.running = False
        for agent in self.schedule.agents:
            if agent.condition in ["Unplaced", "Moving"]:
                count += 1
        if count == 0:
            self.running = False

    @staticmethod
    def count_moves(model):
        count = 0
        for agent in model.schedule.agents:  
            if isinstance(agent, Robot):
                count += agent.moves

        return count