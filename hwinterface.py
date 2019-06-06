from RPi import GPIO
import time
import threading
from classes.sensor_ds18b20 import SensorDS18B20
from classes.sensor_ada375 import SensorADA375
from classes.sensor_hcsr501 import SensorHCSR501
from classes.led import LED
from classes.lcd import LCD


class HWInterface:
    def __init__(self):
        self.a = "running"
        self.stop = False
        self.temperature_sensor = SensorDS18B20()

        self.door_sensor = SensorADA375(16)
        self.door_sensor.on_change(self.door_sensor_callback)

        self.pir_sensor = SensorHCSR501(12, 14)
        self.pir_sensor.on_movement(self.pir_callback)

        self.lcd = LCD()
        self.led = LED(15)

        self.t = threading.Thread(target=self.main)
        self.t.start()

    def main(self):
        try:
            self.lcd.reset_lcd()
            self.lcd.write_string("ALARMOSTAT")
            self.lcd.second_line()
            self.lcd.write_string("IP: 169.254.10.1")
            while True:
                if not self.stop:
                    print(self.a)
                    self.led.toggle()
                    time.sleep(1)
                else:
                    raise KeyboardInterrupt

        except KeyboardInterrupt:
            pass
        finally:
            self.lcd.reset_lcd()
            GPIO.cleanup()
            print("gestopt")

    def door_sensor_callback(self, e):
        print("status deurcontact veranderd")
        if self.door_sensor.is_closed():
            print("deur is nu dicht")
            self.lcd.reset_lcd()
            self.lcd.write_string("DEUR DICHT")
        else:
            print("deur is nu open")
            self.lcd.reset_lcd()
            self.lcd.write_string("DEUR OPEN")

    def pir_callback(self, e=0):
        print("movement detected")
        self.lcd.reset_lcd()
        self.lcd.write_string("BEWEGING")

    def get_temperature(self):
        return self.temperature_sensor.read_temp()

    def get_door_is_closed(self):
        return self.door_sensor.is_closed()

