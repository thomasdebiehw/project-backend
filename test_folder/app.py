from flask import Flask, jsonify, request
from flask_cors import CORS
from classes.sensor_ds18b20 import SensorDS18B20
from classes.database import Database
from datetime import datetime

app = Flask(__name__)
CORS(app)

temperature_sensor = SensorDS18B20()
conn = Database(app=app, user='project', password='ditwachtwoordmagjezekerweten',
                db='alarmostat', host='169.254.10.1', port=3306)
endpoint = '/api/v1'


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route(endpoint + '/sensors/temperature', methods=['GET'])
def temperature():
    if request.method == 'GET':
        val = temperature_sensor.read_temp()
        insert_test(val)
        return jsonify(temperature=val), 200


@app.route(endpoint + '/components', methods=['GET'])
def get_components():
    if request.method == 'GET':
        components = conn.get_data(
            "SELECT * FROM component;")
        return jsonify(components), 200


if __name__ == '__main__':
    app.run()


def insert_test(temperatuur):
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    try:
        st = 'INSERT INTO `alarmostat`.`measurement` (idmeasurement, measurementdatetime, measuredvalue, idcomponent)' \
             'VALUES (DEFAULT, \'{0}\', \'{1}\',1);'.format(formatted_date, temperatuur)
        conn.set_data(st)
    except Exception as e:
        print(e)
