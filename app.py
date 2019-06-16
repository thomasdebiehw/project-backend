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
                db='alarmostat', host='localhost', port=3306)
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
            "SELECT event.*, user.username, component.* FROM event INNER JOIN user ON event.iduser = user.iduser INNER JOIN component on event.idcomponent = component.idcomponent ORDER BY idevent DESC LIMIT 100;")
        return jsonify(components), 200


@app.route(endpoint + '/list/measurements', methods=['GET'])
def get_measurements():
    if request.method == 'GET':
        components = conn.get_data(
            "SELECT * FROM measurement ORDER BY idmeasurement DESC LIMIT 100;")
        return jsonify(components), 200


@app.route(endpoint + '/list/temperature', methods=['GET'])
def get_measurements_temp():
    if request.method == 'GET':
        components = conn.get_data(
            "SELECT * FROM alarmostat.measurement INNER JOIN component ON measurement.idcomponent = component.idcomponent where componenttype = 'thermostat' order by idmeasurement desc limit 5000;")
        return jsonify(components), 200


@socketio.on("connect")
def connecting():
    print("Connection with client established")
    index_data_emit()


@socketio.on("sensor")
def sensor_data():
    sensors = []
    sensors.append(("ADA375 Door sensor", hw.door_sensor.walkin,))
    sensors.append(("HCSR501 Motion sensor", hw.pir_sensor.walkin,))
    socketio.emit("sensor-list", sensors)
    socketio.emit("alarm_timeouts", {"walkin": hw.countdown_walkin, "walkout": hw.countdown_walkout})
    socketio.emit("heating-linked", hw.link_heating)


@socketio.on("toggle-heating-link")
def toggle_heating_link():
    hw.link_heating = not hw.link_heating
    socketio.emit("heating-linked", hw.link_heating)


@socketio.on("change-sensor-walkin")
def change_walking(data):
    if data == "ADA375 Door sensor":
        hw.door_sensor.walkin = not hw.door_sensor.walkin
    elif data == "HCSR501 Motion sensor":
        hw.pir_sensor.walkin = not hw.pir_sensor.walkin
    sensor_data()


@socketio.on("toggle_alarm")
def toggle_alarm():
    hw.change_alarm_status()
    index_data_emit()


@socketio.on("change-temp")
def change_temperature(data):
    print(data)
    hw.temperature_set = float(data)


@socketio.on("change-walkin")
def change_walkin(data):
    hw.countdown_walkin = int(data)


@socketio.on("change-walkout")
def change_walkout(data):
    hw.countdown_walkout = int(data)


@socketio.on("clear-alarm-status")
def clear():
    hw.web_show_alarm = False
    index_data_emit()


def periodic_data_emit():
    while True:
        print("periodic emit")
        index_data_emit()
        time.sleep(10)


def index_data_emit():
    alarm_status = "unavailable"
    socketio.emit("heating-linked", hw.link_heating)
    if hw.alarm_raised:
        alarm_status = "ALARM"
    elif hw.armed:
        alarm_status = "Armed"
    elif not hw.armed and hw.arming:
        alarm_status = "Arming"
    elif not hw.armed:
        alarm_status = "Disarmed"
    if hw.heating.is_on():
        heating_status = "Heating ON"
    else:
        heating_status = "Heating OFF"

    socketio.emit("index_emit", {"alarm_status": alarm_status, "heating_status": heating_status,
                                "set_temperature": hw.temperature_set,
                                "current_temperature": hw.current_temperature})
    new_alarm_raised_events_emit()


def new_alarm_raised_events_emit():
    obj = {"empty": True}
    if hw.web_show_alarm:
        events = hw.db_get_events("alarm_raised", 1)
        if len(events) != 0:
            obj = {"empty": False, "time": events[0][1].strftime("%d/%m/%Y, %H:%M"), "sensor": events[0][6]}
    socketio.emit("new_alarm_raised_events", obj)


periodic_emit_t = threading.Thread(target=periodic_data_emit)
periodic_emit_t.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0')


