from flask import Flask, jsonify, request
from model import *
from os import getenv

app = Flask("City")

cars = 3
timeLimit = 10
city = None
currentStep = 0

# Inicializar con parámetros de usuarios
@app.route('/init', methods = ['POST'])
def initialize():
    global city, cars, timeLimit
    if request.method == 'POST':
        cars = int(request.form.get('cars'))
        timeLimit = int(request.form.get('timeLimit'))
        print(request.form)

        city = City(cars)

        return jsonify({"message": "Initializing model"})

# Obtener posiciones de coches
@app.route('/cars', methods = ['GET'])
def cars():
    global city
    if request.method == 'GET':
        if city == None:
            return jsonify({"error": "Model is not initialized. Initialize and try again"})
        """ carsData = [
            {
                "x": agent.pos[0], 
                "y": agent.pos[1], 
                "directionLightLeft": agent.directionLight[0], 
                "directionLightRight": agent.directionLight[1], 
                "isParked": agent.is_parked, 

            } for agent in city.schedule.agents if isinstance(agent, Car)
        ] """
        carsData = {
            "positions": [], 
            "directionLightLeft": [],
            "directionLightRight": [],
            "isParked": [],
        }
        for agent in city.schedule.agents:
            if isinstance(agent, Car):
                carsData["positions"].append({"x": agent.pos[0], "z": agent.pos[1], "y": 0})
                carsData["directionLightLeft"].append(agent.directionLight[0])
                carsData["directionLightRight"].append(agent.directionLight[1])
                carsData["isParked"].append(agent.is_parked)

        print(carsData)
        # return jsonify(carsData[0])
        return jsonify(carsData)

# Obtener estados de los semáforos
@app.route('/trafficlights', methods = ['GET'])
def trafficLights():
    global city
    if request.method == 'GET':
        if city == None:
            return jsonify({"error": "Model is not initialized. Initialize and try again"})
        trafficLightsStates = [agent.state for agent in city.schedule.agents if isinstance(agent, Traffic_Light)]
        return jsonify({"states": trafficLightsStates})

# Obtener actualizaciones del modelo
@app.route('/update', methods = ['GET'])
def update():
    global city, currentStep
    if request.method == 'GET':
        if city == None:
            return jsonify({"error": "Model is not initialized. Initialize and try again"})
        city.step()
        currentStep += 1
        return str(city.running)

# Obtener estadísticas finales
@app.route('/finalstats', methods = ['GET'])
def finalStats():
    global city
    if request.method == 'GET':
        if city == None:
            return jsonify({"error": "Model is not initialized. Initialize and try again"})
        parked_cars, moves = city.finalStats()
        return jsonify({"states": [str(parked_cars), str(moves)]})

port = int(getenv('PORT', 8080))
app.run(host='0.0.0.0', port=port, debug=True)