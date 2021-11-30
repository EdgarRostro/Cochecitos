from flask import Flask, jsonify, request
from model import *

PORT = 8585

app = Flask("City")

cars = 3
timeLimit = 10
city = None
currentStep = 0

# Inicializar con parámetros de usuarios
@app.route('/init', method=['POST'])
def init():
    global city, cars
    if request.method == 'POST':
        cars = int(request.form.get('cars'))
        timeLimit = int(request.form.get('timeLimit'))
        print(request.form)

        neighborhood = City(cars)

        return jsonify({"message": "Initializing model"})

# Obtener posiciones de coches
@app.route('/cars', method = ['GET'])
def cars():
    global city
    if request.method == 'GET':
        if city == None:
            return jsonify({"error": "Model is not initialized. Initialize and try again"})
        carsData = [{"x": agent.pos[0], "y": agent.pos[1], "directionLight": agent.directionLight, "isParked": agent.is_parked} for agent in city.schedule.agents if isinstance(agent, Car)]
        return jsonify({"cars": carsData})

# Obtener estados de los semáforos
@app.route('/trafficlights', method = ['GET'])
def trafficLights():
    global city
    if request.method == 'GET':
        if city == None:
            return jsonify({"error": "Model is not initialized. Initialize and try again"})
        trafficLightsStates = [{"x": agent.pos[0], "y": agent.pos[1], "state": agent.state} for agent in city.schedule.agents if isinstance(agent, Traffic_Light)]
        return jsonify({"trafficLights": trafficLightsStates})

# Obtener actualizaciones del modelo
@app.route('/update', method = ['GET'])
def update():
    global city, currentStep
    if request.method == 'GET':
        if city == None:
            return jsonify({"error": "Model is not initialized. Initialize and try again"})
        city.step()
        currentStep += 1
        return str(city.running)

# Obtener estadísticas finales
@app.route('/finalstats', method = ['GET'])
def finalStats():
    global city
    if request.method == 'GET':
        return "Hola aqui aun faltan las estadísticas."

if __name__ == "__main__":
    app.runt(host="localhost", port=PORT, debug=True)