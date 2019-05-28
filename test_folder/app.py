from flask import Flask, jsonify
from flask_cors import CORS
from classes.sensor_ds18b20 import SensorDS18B20

app = Flask(__name__)
CORS(app)

temperature_sensor = SensorDS18B20()
endpoint = '/api/v1'


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route(endpoint + '/sensors/temperature')
def temperature():
    return jsonify(temperature_sensor.read_temp()), 200


if __name__ == '__main__':
    app.run()
