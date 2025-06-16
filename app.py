from flask import Flask, request, jsonify
from models import Spaceship, Mission, CrewMember

app = Flask(__name__)

# Инициализация данных
fleet = {
    "spaceships": [],
    "missions": [],
    "crew": []
}

# Генераторы ID
def next_id(collection):
    return max([item[list(item.keys())[0]] for item in collection], default=0) + 1

# Вспомогательные функции
def find_spaceship(spaceship_id):
    return next((s for s in fleet["spaceships"] if s["spaceship_id"] == spaceship_id), None)

def find_mission(mission_id):
    return next((m for m in fleet["missions"] if m["mission_id"] == mission_id), None)

# API Endpoints
@app.route('/api/v1/spaceships', methods=['GET', 'POST'])
def handle_spaceships():
    if request.method == 'GET':
        return jsonify(fleet["spaceships"])
    
    data = request.get_json()
    try:
        new_ship = Spaceship(
            spaceship_id=next_id(fleet["spaceships"]),
            name=data['name'],
            ship_type=data['type'],
            status=data.get('status', 'available')
        )
        fleet["spaceships"].append(new_ship.to_dict())
        return jsonify(new_ship.to_dict()), 201
    except (KeyError, ValueError) as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/v1/spaceships/<int:spaceship_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_spaceship(spaceship_id):
    ship = find_spaceship(spaceship_id)
    if not ship:
        return jsonify({"error": "Spaceship not found"}), 404
    
    if request.method == 'GET':
        return jsonify(ship)
    
    elif request.method == 'PUT':
        data = request.get_json()
        if 'status' in data:
            try:
                Spaceship(**ship).update_status(data['status'])
                ship['status'] = data['status']
                return jsonify(ship)
            except ValueError as e:
                return jsonify({"error": str(e)}), 400
        return jsonify({"error": "No valid fields provided"}), 400
    
    elif request.method == 'DELETE':
        fleet["spaceships"].remove(ship)
        return jsonify({"message": "Spaceship deleted"}), 200

@app.route('/api/v1/missions', methods=['GET', 'POST'])
def handle_missions():
    if request.method == 'GET':
        return jsonify(fleet["missions"])
    
    data = request.get_json()
    try:
        new_mission = Mission(
            mission_id=next_id(fleet["missions"]),
            name=data['name'],
            goal=data['goal'],
            status=data.get('status', 'planned')
        )
        fleet["missions"].append(new_mission.to_dict())
        return jsonify(new_mission.to_dict()), 201
    except (KeyError, ValueError) as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/v1/missions/<int:mission_id>/add_ship', methods=['POST'])
def add_ship_to_mission(mission_id):
    mission = find_mission(mission_id)
    if not mission:
        return jsonify({"error": "Mission not found"}), 404
    
    data = request.get_json()
    if 'spaceship_id' not in data:
        return jsonify({"error": "spaceship_id is required"}), 400
    
    ship = find_spaceship(data['spaceship_id'])
    if not ship:
        return jsonify({"error": "Spaceship not found"}), 404
    
    try:
        Mission(**mission).add_spaceship(Spaceship(**ship))
        mission["spaceships"].append(ship)
        ship["status"] = "on_mission"
        return jsonify(mission)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# Запуск приложения
if __name__ == '__main__':
    app.run(debug=True)
