from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation, SimultaneousActivation, StagedActivation
from mesa.datacollection import DataCollector
from numpy import show_config
from boxes import Cell, Robot, Box

class Room(Model):
    def __init__(self):
        super().__init__()
        self.pile = (1,0)