from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO
from classes.database import Database
from hwinterface import HWInterface
import signal, atexit, time, threading


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
    print("Connection with client established")
    index_data_emit()


@socketio.on("toggle_alarm")
def toggle_alarm():
    hw.change_alarm_status()
    index_data_emit()


@socketio.on("change-temp")
def change_temperature(data):
    print(data)
    hw.temperature_set = float(data)


@socketio.on("acknowledge_event")
def ack_event(data):
    hw.db_acknowledge_event(data)
    new_alarm_raised_events_emit()


def periodic_data_emit():
    while True:
        print("periodic emit")
        index_data_emit()
        new_alarm_raised_events_emit()
        time.sleep(10)


def index_data_emit():
    alarm_status = "unavailable"
    if hw.alarm_raised:
        alarm_status = "ALARM"
    elif hw.armed:
        alarm_status = "Armed"
    elif not hw.armed and hw.arming:
        alarm_status = "Arming"
    elif not hw.armed:
        alarm_status = "Disarmed"
    if hw.led.is_on():
        heating_status = "Heating ON"
    else:
        heating_status = "Heating OFF"

    socketio.emit("index_emit", {"alarm_status": alarm_status, "heating_status": heating_status,
                                "set_temperature": hw.temperature_set,
                                "current_temperature": hw.current_temperature})


def new_alarm_raised_events_emit():
    events = hw.db_get_events_readable("alarm_raised")
    socketio.emit("new_alarm_raised_events", events)


periodic_emit_t = threading.Thread(target=periodic_data_emit)
periodic_emit_t.start()

if __name__ == '__main__':
    app.run()


