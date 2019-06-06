from flask import Flask, jsonify, request
from flask_cors import CORS
from classes.database import Database
from hwinterface import HWInterface
import signal
import atexit


app = Flask(__name__)
CORS(app)
hw = HWInterface()

conn = Database(app=app, user='project', password='ditwachtwoordmagjezekerweten',
                db='alarmostat', host='169.254.10.1', port=3306)
endpoint = '/api/v1'


def close_thread(signum=0, frame=0):
    print("ctrlchandler")
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


@app.route(endpoint + '/components', methods=['GET'])
def get_components():
    if request.method == 'GET':
        components = conn.get_data(
            "SELECT * FROM component;")
        return jsonify(components), 200


if __name__ == '__main__':
    app.run()


