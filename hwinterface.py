import time, threading, datetime, mysql.connector
from subprocess import check_output
from RPi import GPIO
from mfrc522 import SimpleMFRC522
from classes.sensor_ds18b20 import SensorDS18B20
from classes.sensor_ada375 import SensorADA375
from classes.sensor_hcsr501 import SensorHCSR501
from classes.rotary_encoder import RotaryEncoder
from classes.buzzer import Buzzer
from classes.led import LED
from classes.lcd import LCD


class HWInterface:
    def __init__(self):
        self.mydb = mysql.connector.connect(host="localhost", user="project", passwd="ditwachtwoordmagjezekerweten", database="alarmostat")
        self.mycursor = self.mydb.cursor()
        self.dbout = []

        self.screen = -1
        self.stop = False
        self.button_pressed = False

        self.armed = False
        self.arming = False
        self.display_change = False
        self.triggered = False
        self.countdown = 15

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
        self.lcd.show_cursor(False)

        self.led = LED(15)
        self.buzzer = Buzzer(13)
        self.buzzer.off()

        self.reader = SimpleMFRC522()
        self.rfidtag = 0
        self.rfidt = threading.Thread(target=self.rfid)
        self.rfidt.setDaemon(True)
        self.rfidt.start()

        self.t = threading.Thread(target=self.main)
        self.t.start()

    def main(self):
        try:
            self.lcd.reset_lcd()
            self.lcd.write_string("ALARMOSTAT")
            while True:
                if not self.stop:
                    if self.button_pressed:
                        self.lcd.reset_lcd()
                        if self.screen < 4:
                            self.screen += 1
                        else:
                            self.screen = 0
                        self.lcd_text()
                        self.button_pressed = False
                    elif self.screen == 4 or self.screen == 5:
                        self.lcd_text()
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
            self.lcd.move_cursor(0)
            self.lcd.write_string("Current: ")
            temp = self.temperature_sensor.read_temp()
            self.lcd.write_string("{0}C".format(str(temp)))
            self.lcd.second_line()
            self.lcd.write_string("Set: {0}C".format(str(self.temperature_set)))

        elif self.screen == 2:
            self.lcd.move_cursor(0)
            if self.door_sensor.is_closed():
                self.lcd.write_string("Door closed")
            else:
                self.lcd.write_string("Door open")

        elif self.screen == 3:
            self.lcd.reset_lcd()
            self.lcd.write_string("No events")
            self.lcd.second_line()
            if self.armed:
                self.lcd.write_string("System ARMED")
            else:
                self.lcd.write_string("System DISARMED")

        elif self.screen == 4:
            now = datetime.datetime.now()
            self.lcd.move_cursor(0)
            self.lcd.write_string(now.strftime("%Y-%m-%d"))
            self.lcd.second_line()
            self.lcd.write_string(now.strftime("%H:%M:%S"))

        elif self.screen == 5:
            self.lcd.move_cursor(0)
            if self.arming:
                self.lcd.write_string("System ARMING in")
                self.lcd.second_line()
                self.lcd.write_string("{0} seconds ".format(str(int(self.buzzer.countdown_timer))))
            elif self.armed:
                self.lcd.write_string("System ARMED                    ")
            else:
                self.lcd.write_string("System DISARMED ")
                if self.display_change:
                    self.lcd.second_line()
                    self.lcd.write_string("Hello {0}".format(self.dbout[0][0]))
                    self.display_change = False

    def rfid(self):
        while True:
            self.rfidtag = self.reader.read_id()
            self.mycursor.execute(
                "SELECT username FROM user WHERE userrfidtag={0};".format(self.rfidtag))
            self.dbout = []
            for x in self.mycursor:
                self.dbout.append(x)
            if len(self.dbout) >= 1:
                print(self.dbout[0][0])
                self.lcd.reset_lcd()
                self.change_alarm_status()
                time.sleep(2)
            else:
                time.sleep(2)

    def arm(self):
        self.arming = True
        self.buzzer.countdown(self.countdown)
        if self.arming:
            self.lcd.reset_lcd()
            self.armed = True
            self.buzzer.sound()
        self.arming = False

    def change_alarm_status(self):
        if self.armed:
            self.armed = False
            self.display_change = True
            self.buzzer.sound()
        elif self.arming:
            self.arming = False
            self.display_change = True
            self.buzzer.stop_countdown = True
            self.buzzer.sound()
        else:
            cd_thread = threading.Thread(target=self.arm)
            cd_thread.setDaemon(True)
            cd_thread.start()
            self.screen = 5





