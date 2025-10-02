from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__)
devices = {
    "light_1": {"type": "light", "status": "off", "name": "Living Room Light"},
    "light_2": {"type": "light", "status": "off", "name": "Bedroom Light"},
    "door_1": {"type": "door_lock", "status": "locked", "name": "Front Door"},
    "thermostat_1": {"type": "thermostat", "status": "22", "name": "Main Thermostat"},
    "tv_1": {"type": "tv", "status": "off", "name": "Living Room TV"},
    "fan_1": {"type": "fan", "status": "off", "name": "Ceiling Fan"},
}

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/style.css')
def serve_css():
    return send_from_directory('.', 'style.css')

@app.route('/api/devices', methods=['GET'])
def get_devices():
    return jsonify(devices), 200

@app.route('/api/devices/<device_id>', methods=['GET'])
def get_device(device_id):
    device = devices.get(device_id)
    if device:
        return jsonify({device_id: device}), 200
    else:
        return jsonify({"error": "Device not found"}), 404

@app.route('/api/devices/<device_id>', methods=['PUT'])
def update_device(device_id):
    if device_id not in devices:
        return jsonify({"error": "Device not found"}), 404
    data = request.get_json()
    new_status = data.get("status")

    if not new_status:
        return jsonify({"error": "Missing 'status' field"}), 400
  
    devices[device_id]["status"] = new_status
    return jsonify({device_id: devices[device_id]}), 200

if __name__ == '__main__':
    app.run(debug=True)