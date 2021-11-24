from mesa import Agent
import random

class Cell(Agent):
    
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        # Conditions = Available, Obstacle
        self.condition = "Available"

    def step(self):
        # Obtener vecinos (lista de coordenadas)
        neighbors = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
        # Contar vecinos con obstaculos
        count = 0
        for coords in neighbors:
            # Obtener agentes en los vecinos
            cellAgents = self.model.grid[coords[0]][coords[1]]        
            # Incrementar count cuando hay más de dos agentes (obstáculo)
            hasObstacle = False
            for agent in cellAgents:
                if agent.condition not in ["Moving", "Available", "Placing"]:
                    hasObstacle += True
            if hasObstacle:
                count+=1
        # Si hay 3+ vecinos con obstáculos, hacer celda un obstáculo
        if count >=3:
            self.condition = "Obstacle"
        else:
            self.condition = "Available"


class Box(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        # Conditions = Unplaced, Piled, Moving
        self.condition = "Unplaced"
        self.y = 0.48

    def step(self):
        pass


class Robot(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        # Conditions = Searching, Placing
        self.condition = "Searching"
        self.box = None
        # Direction: N=0, W=1, E=2, S=3
        self.direction = 0
        self.moves = 0

    # Determina si un vecino es obstáculo y lo regresa
    def isNeighborObstacle(self, cell):
        # Regresar true si es out of bounds
        if self.model.grid.out_of_bounds(cell):
            return (True, None)
        # Obtener agentes en cell
        cellAgents = self.model.grid[cell[0]][cell[1]]
        # Obtener agente celda
        if cellAgents[0].condition == "Obstacle":
            return (True, cellAgents[0])
        # Si el tamaño es uno, la celda está vacía
        if len(cellAgents) >= 6:
            return (True, cellAgents[0])
        # Checar si alguna celda es obstáculo
        ans = (False, cellAgents[0])
        for agent in cellAgents:
            # Siempre: Otro robot
            if isinstance(agent, Robot):
                return (True, agent)
            # Caja
            if isinstance(agent, Box):
                ans = (True, agent)
        return ans

    def moveToCoords(self, coords):
        # Obtener distancias por componentes
        deltaX = self.pos[0] - coords[0]
        deltaY = self.pos[1] - coords[1]
        # Obtener direccion (-1, o 1)
        dirX = 1 if deltaX < 0 else -1
        dirY = 1 if deltaY < 0 else -1
        # Almacenar nuevas coordenadas
        newCoords = self.pos
        if deltaX == 0:
            newCoords = (self.pos[0], self.pos[1] + dirY)
        elif deltaY == 0:
            newCoords = (self.pos[0] + dirX, self.pos[1])
        elif abs(deltaX) > abs(deltaY):
            newCoords = (self.pos[0] + dirX, self.pos[1])
        elif abs(deltaX) < abs(deltaY):
            newCoords = (self.pos[0], self.pos[1] + dirY)    
        else:
            newCoords = (self.pos[0] + dirX, self.pos[1])
        
        # Si hay un obstáculo en esas coordenadas ??
        isObstacle = self.isNeighborObstacle(newCoords)[0]
        while isObstacle:
            # Obtener vecino random
            neighbors = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
            # Obtener elemento random de arreglo
            newCoords = random.choice(neighbors)
            # Actualizar condicion
            isObstacle = self.isNeighborObstacle(newCoords)[0]
        return newCoords

    def move(self):
        
        # Obtener vecinos [N, W, E, S]
        neighbors = self.getNeighbors()
        # Establecer direccion
        newDir = self.direction
        
        # Determinar movimiento cuando está buscando
        # Si está buscando, moverse en dirección aleatoria hasta encontrar una caja
        if self.condition == "Searching":
            newPos = ()
            # Buscar alguna celda con caja e irse hacia allá
            for neighbor in self.model.grid.neighbor_iter(self.pos, moore=False):
                if neighbor.condition == "Unplaced":
                    newPos = neighbor.pos
                    break
                else:
                    newDir = self.random.randint(0,3)
                    newPos = neighbors[newDir]

            obs = self.isNeighborObstacle(newPos)
            if obs[0] and obs[1] != None:
                if obs[1].condition == "Unplaced":
                    self.model.grid.move_agent(self, newPos)
                    self.box = obs[1]
                    self.condition = "Placing"
                    self.box.condition = "Moving"
                    self.box.y = 0.8
                elif isinstance(obs[1], Cell):
                   self.model.grid.move_agent(self, newPos)
                   self.moves += 1
            elif not obs[0]:
                self.model.grid.move_agent(self, newPos)
                self.moves += 1
        
        # Viajando (con caja) a apilar la caja
        elif self.condition == "Placing":
            # Obtener siguiente ubicacion para este paso
            moveHere = self.moveToCoords(self.model.pile)
            if self.pos != self.model.pile:
                # Mover robot
                self.model.grid.move_agent(self, moveHere)
                # Mover caja
                self.model.grid.move_agent(self.box, moveHere)
                self.moves += 1
            else:
                # Soltar caja y cambiar estado
                self.box.condition = "Piled"
                self.box.y = 0.32*self.model.pile_size+0.48
                # La caja se queda una posición a la izquierda de donde está el robot
                pile = (self.model.pile[0]-1, self.model.pile[1])
                self.model.grid.move_agent(self.box, pile)
                # Actualizar ubicacion de pila
                self.model.check_pile()
                self.condition = "Searching"
                self.box = None

    def getNeighbors(self):
        # Obtener coordenadas de vecinos
        north_cell = self.pos[0], self.pos[1] + 1
        west_cell = self.pos[0] - 1, self.pos[1]
        east_cell = self.pos[0] + 1, self.pos[1]
        south_cell = self.pos[0], self.pos[1] - 1
        
        return [north_cell, west_cell, east_cell, south_cell]

    def step(self):
        # Mover en dirección 
        self.move()
    