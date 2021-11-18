from mesa import Agent

class Cell(Agent):
    
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        # Conditions = Unvisited, visited
        self.state = "Unvisited"


class Box(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        # Conditions = Unplaced, Moving, Piled
        self.condition = "Unplaced"

    def step(self):
        pass

leftTurns = {
    0: 1, 
    1: 3, 
    2: 0, 
    3: 2
}

rightTurns = {
    0: 2, 
    2: 3, 
    3: 1, 
    1: 0
}

class Robot(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        # Conditions = Searching, Placing, Starting
        self.condition = "Starting"
        self.box = -1
        # Direction: N=0, W=1, E=2, S=3
        self.direction = 0
        
    def move(self):
        # Almacenar cuál sería la siguiente posición
        neighbors = self.getNeighbors()
        # Guardar acá la nueva dirección
        newDir = self.direction

        # Returns [Bool, Agent]
        def isNeighborObstacle(direction):
            cell = neighbors[direction]
            # Regresar true si es out of bounds
            if self.model.grid.out_of_bounds(cell):
                return (True, None)
            # Obtener agentes en cell
            cellAgents = self.model.grid[cell[0]][cell[1]]
            # Si el tamaño es uno, la celda está vacía
            if len(cellAgents) == 1:
                return (False, cellAgents[0])
            # Checar si alguna celda es obstáculo
            ans = ()
            for agent in cellAgents:
                # Siempre: Otro robot
                if isinstance(agent, Robot):
                    return (True, agent)
                # Caja
                if isinstance(agent, Box):
                    ans = (True, agent)
                
            return ans

        newDir = self.random.randint(0,3)
        obs = isNeighborObstacle(newDir)
        if obs[0]:
            if self.condition == "Searching" and obs[1].condition == "Unplaced":
                self.model.grid.move_agent(self, neighbors[newDir])
                self.box = obs[1]
                self.condition = "Placing"

        else:
            self.model.grid.move_agent(self, neighbors[newDir])
        


        # FIjarnos en la celda de adelante (neighbor[self.direction])
        # cAmbiar direccion cuando choca con pared (empezar a marcar visitadas)
        if not self.model.grid.out_of_bounds(neighbors[0]):
            if self.condition == "Starting":
                self.condition = "Searching"
                if not self.model.grid.out_of_bounds(neighbors[2]) or :
                
        
        
        # (intentar ir siempre a su izquierda, seguir derecho o derecha)            
        # si celda a su izquierda está disponible -> newDir = leftTurns[self.direction]
        # Si estas buscando y esa celda es una caja, agarrar y seguir con misma direccion


        def tryTurnLeft():
            # Intentar izquierda
            leftCell = neighbors[leftTurns[self.direction]]
            if not self.model.grid.out_of_bounds(leftCell):
                leftCellAgents = self.model.grid[leftCell[0]][leftCell[1]]
                for agent in leftCellAgents:
                    if self.condition == "Searching" and agent.condition == "Unplaced":
                        self.model.grid.move_agent(self, leftCell)
                        return
                    elif self.condition == "Searching" and agent.condition == "Unvisited":
                        self.model.grid.move_agent(self, leftCell)
                        return
                    elif self.condition == "Placing" and len(leftCellAgents) == 1:
                        self.model.grid.move_agent(self, leftCell)
                        return
                    
                          
            # Si izquierda no se puede, intentar seguir misma dirección
            frontCell = neighbors[self.direction]
            if not self.model.grid.out_of_bounds(frontCell):
                frontCellAgents = self.model.grid[frontCell[0]][frontCell[1]]
                for agent in frontCellAgents:
                    return
            # Si misma dirección no se puede intentar derecha
            rightCell = neighbors[self.direction]
            if not self. model.grid.out_of_bounds(rightCell):
                rightCellAgents = self.model.grid[rightCell[0]][rightCell[1]]
                for agent in rightCellAgents:
                    return
            # Si ninguna se puede (f) no moverse hasta el siguiente paso
            return

        

    def getNeighbors(self):
        # Obtener coordenadas de vecinos
        north_cell = self.pos[0], self.pos[1] + 1
        west_cell = self.pos[0] - 1, self.pos[1]
        east_cell = self.pos[0] + 1, self.pos[1]
        south_cell = self.pos[0], self.pos[1] - 1
        
        return [north_cell, west_cell, east_cell, south_cell]

    def step(self):
        # Mover en dirección 
        # Si está buscando
        if self.condition == "Searching":
            # Obtener agentes que estén en la misma posición

