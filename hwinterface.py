from subprocess import check_output
from RPi import GPIO
import time
import threading
from classes.sensor_ds18b20 import SensorDS18B20
from classes.sensor_ada375 import SensorADA375
from classes.sensor_hcsr501 import SensorHCSR501
from classes.rotary_encoder import RotaryEncoder
from classes.led import LED
from classes.lcd import LCD


class HWInterface:
    def __init__(self):
        self.a = "running"
        self.screen = -1
        self.stop = False
        self.button_pressed = False
        self.temperature_set = 21.000
        self.temperature_sensor = SensorDS18B20()
        self.rotary_encoder = RotaryEncoder(26, 24, 19)
        self.rotary_encoder.on_button_press(self.button_callback)
        self.rotary_encoder.on_turn_right(self.turned_right)
        self.rotary_encoder.on_turn_left(self.turned_left)

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
            while True:
                if not self.stop:
                    if self.button_pressed:
                        if self.screen < 2:
                            self.screen += 1
                        else:
                            self.screen = 0
                        self.lcd_text()
                        self.button_pressed = False
                    time.sleep(0.01)
                else:
                    raise KeyboardInterrupt

        except KeyboardInterrupt:
            pass
        finally:
            self.lcd.reset_lcd()
            GPIO.cleanup()
            print("thread stopped")

    def button_callback(self, e):
        print("button pressed")
        self.button_pressed = True

    def turned_right(self, e=0):
        self.temperature_set = self.temperature_set + 0.500
        self.lcd_text()
        print("right")

    def turned_left(self, e=0):
        self.temperature_set = self.temperature_set - 0.500
        self.lcd_text()
        print("left")

    def door_sensor_callback(self, e):
        print("status deurcontact veranderd")
        if self.door_sensor.is_closed():
            print("deur is nu dicht")
        else:
            print("deur is nu open")
        if self.screen == 2:
            self.lcd_text()

    def pir_callback(self, e=0):
        print("movement detected")
        # self.lcd.reset_lcd()
        # self.lcd.write_string("BEWEGING")

    def get_temperature(self):
        return self.temperature_sensor.read_temp()

    def get_door_is_closed(self):
        return self.door_sensor.is_closed()

    def lcd_text(self):
        if self.screen == 0:
            ips = check_output(['hostname', '--all-ip-addresses'])
            ips = str(ips)[2:len(ips) - 3]
            ipslist = ips.split(" ")
            self.lcd.reset_lcd()
            self.lcd.write_string(ipslist[0])
            self.lcd.second_line()
            if len(ipslist) >= 2:
                self.lcd.write_string(ipslist[1])

        elif self.screen == 1:
            self.lcd.reset_lcd()
            self.lcd.write_string("Current: ")
            temp = self.temperature_sensor.read_temp()
            self.lcd.write_string("{0}C".format(str(temp)))
            self.lcd.second_line()
            self.lcd.write_string("Set: {0}C".format(str(self.temperature_set)))

        elif self.screen == 2:
            if self.door_sensor.is_closed():
                self.lcd.reset_lcd()
                self.lcd.write_string("Door closed")
            else:
                self.lcd.reset_lcd()
                self.lcd.write_string("Door open")



