from random import shuffle
from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation, SimultaneousActivation, StagedActivation, BaseScheduler
from mesa.datacollection import DataCollector
from boxes import Cell, Robot, Box

class Room(Model):
    def __init__(self, width, height, density, robots, timer):
        self.pile = (1,0)
        self.pile_size = 0

        # model_stages = ["stage_1", "stage_2"]
        # self.schedule = StagedActivation(self, model_stages)
        # self.schedule = RandomActivation(self)
        self.schedule = BaseScheduler(self)

        # Inicializar data colector
        self.datacollector = DataCollector(
            {
                "Movimientos": lambda m: self.count_moves(m)
            }
        )

        self.grid = MultiGrid(width, height, torus=False)
        self.running = True
        self.timer = 0
        self.timeLimit = timer
        self.steps = 0
        self.id = 0

        # Poner celdas en todo el grid
        for(contents, x, y) in self.grid.coord_iter():
            cell = Cell(self.id, self)
            self.grid.place_agent(cell, (x, y))
            self.schedule.add(cell)
            self.id += 1
        # Agregar cajas (según densidad)
        for (contents, x, y) in self.grid.coord_iter():
            if self.random.random() < density and not (x in [0, 1] and y == 0):
                new_box = Box(self.id, self)
                self.grid.place_agent(new_box, (x, y))
                self.schedule.add(new_box)
                self.id += 1
        
        # Poner cantidad necesaria de robots
        for i in range(robots):
            new_robot = Robot(self.id, self)
            self.grid.place_agent(new_robot, (self.random.randint(0, width - 1), self.random.randint(0, height - 1)))
            self.schedule.add(new_robot)
            self.id += 1
    
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
        
        # Collect data on each step
        # self.datacollector.collect(self)

    @staticmethod
    def count_moves(model):
        count = 0
        for agent in model.schedule.agents:  
            if isinstance(agent, Robot):
                count += agent.moves

        return count