from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules.ChartVisualization import ChartModule
from mesa.visualization.modules.PieChartVisualization import PieChartModule
from model import Room, Cell, Robot, Box

colors = {"Obstacle" : "#ff000080", "Available" : "lightgreen", "Placing" : "#ad8762", "Searching" : "darkblue"}
#colorsCharts = {"Limpia" : "lightblue", "Sucia" : "darkgreen"}
colorsSteps = {"Movimientos" : "blue"}

def agent_portrayal(cell):
    if cell is None: return
    
    portrayal = {"Shape" : "rect", "w" : 0.7, "h" : 0.7, "Filled" : "true", "Layer" : 0}

    if (isinstance(cell, Robot)):
        portrayal['Shape'] = "circle"
        portrayal['r'] = 0.7
        portrayal['Layer'] = 2
        portrayal['Color'] = colors[cell.condition]
        
    if (isinstance(cell, Box)):
        portrayal['Shape'] = "rect"
        portrayal['w'] = 0.5
        portrayal['h'] = 0.5
        portrayal['Layer'] = 1
        portrayal['Color'] = "#ad8762"
        
    if (isinstance(cell, Cell)):
        portrayal["Color"] = colors[cell.condition]

    return portrayal

model_params = {
    "height" : UserSettableParameter("choice", "Largo del cuarto", choices=[10, 25, 20, 25], value=15),
    # "height" : 25,
    "width" : UserSettableParameter("choice", "Ancho del cuarto", choices=[10, 25, 20, 25], value=25),
    # "width" : 25,
    "density" : UserSettableParameter("slider", "Box density", 0.5, 0.01, 1.0, 0.1),
    "robots" : UserSettableParameter("slider", "Robots", 3, 1, 10, 1),
    "timer" : UserSettableParameter("slider", "Time", 50, 1, 1000, 1)
}

canvas_element = CanvasGrid(agent_portrayal, 25, 25, 500, 500)

# moves_chart = ChartModule(
#     [{"Label": label, "Color": color} for (label, color) in colorsSteps.items()]
# )

server = ModularServer(
    Room, 
    [canvas_element], 
    "Robots",
    model_params
)

server.launch()