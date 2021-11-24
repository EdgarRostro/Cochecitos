from flask import Flask, jsonify, request
from model import *

app = Flask("Warehouse")

width = 25
height = 25
density = 0.2
robots = 3
timer = 500
warehouse = None
currentStep = 0

# Función para leer los parámetros del usuario
@app.route('/init', methods=['POST'])
def begin():
    global width, height, density, robots, timer, warehouse, currentStep

    if request.method == 'POST':
        robots = int(request.form.get('robots'))
        width = int(request.form.get('width'))
        height = int(request.form.get('height'))
        density = float(request.form.get('density'))
        timer = int(request.form.get('timer'))
        currentStep = 0

        print(request.form)
        print(robots, width, height)
        
        warehouse = Room(width, height, density, robots, timer)

        return jsonify({"message":"Parameters recieved, model initiated."})

# Función para mover robots
@app.route('/getRobots', methods = ['GET'])
def robots():
    global warehouse

    if request.method == 'GET':
        robotsPos = [{"x" : agent.pos[0], "y" : 0.4, "z" : agent.pos[1]} for agent in warehouse.schedule.agents if isinstance(agent, Robot)]

        return jsonify({'positions': robotsPos})

# Función para mover cajas
@app.route('/getBoxes', methods=['GET'])
def boxes():
    global warehouse

    if request.method == 'GET':
        boxPositions = [{"x": agent.pos[0], "y":agent.y, "z":agent.pos[1]} for agent in warehouse.schedule.agents if isinstance(agent, Box)]

    return jsonify({'positions': boxPositions})

# Actualizar modelo
@app.route('/update', methods=['GET'])
def updateModel():
    global currentStep, warehouse
    if request.method == 'GET':
        warehouse.step()
        currentStep += 1
        return jsonify({'message':f'Model updated to step {currentStep}.', 'currentStep':currentStep})

@app.route('/getConditions', methods=['GET'])
def conditions():
    global warehouse

    if request.method == 'GET':
        robotsCond = [{"condition": agent.condition} for agent in warehouse.schedule.agents if isinstance(agent, Robot)]

        return jsonify({'conditions': robotsCond})

if __name__=='__main__':
    app.run(host="localhost", port=8585, debug=True)