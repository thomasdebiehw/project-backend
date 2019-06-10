from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO
from classes.database import Database
from hwinterface import HWInterface
import signal
import atexit


app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)
hw = HWInterface()

conn = Database(app=app, user='project', password='ditwachtwoordmagjezekerweten',
                db='alarmostat', host='169.254.10.1', port=3306)
endpoint = '/api/v1'


def close_thread(signum=0, frame=0):
    print("closing thread")
    hw.stop = True


signal.signal(signal.SIGINT, close_thread)
atexit.register(close_thread)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route(endpoint + '/sensors/temperature', methods=['GET'])
def temperature():
    if request.method == 'GET':
        val = hw.get_temperature()
        return jsonify(temperature=val), 200


@app.route(endpoint + '/list/components', methods=['GET'])
def get_components():
    if request.method == 'GET':
        components = conn.get_data(
            "SELECT * FROM component;")
        return jsonify(components), 200


@app.route(endpoint + '/list/events', methods=['GET'])
def get_events():
    if request.method == 'GET':
        components = conn.get_data(
            "SELECT * FROM event ORDER BY idevent DESC LIMIT 100;")
        return jsonify(components), 200


@app.route(endpoint + '/list/measurements', methods=['GET'])
def get_measurements():
    if request.method == 'GET':
        components = conn.get_data(
            "SELECT * FROM measurement ORDER BY idmeasurement DESC LIMIT 100;")
        return jsonify(components), 200


@socketio.on("connect")
def connecting():
    socketio.emit("connected")
    print("Connection with client established")


if __name__ == '__main__':
    app.run()


