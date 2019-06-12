import time, threading, multiprocessing, datetime, mysql.connector
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
        self.alarm_raised = False
        self.last_event_user = 0
        self.countdown_walkin = 15
        self.countdown_walkout = 15

        self.temperature_previous = 21.000
        self.temperature_set = 21.000
        self.temperature_armed = 16.000
        self.temperature_sensor = SensorDS18B20()
        self.current_temperature = self.get_temperature()

        self.rotary_encoder = RotaryEncoder(26, 18, 19)
        self.rotary_encoder.on_button_press(self.button_callback)
        self.rotary_encoder.on_turn_right(self.turned_right)
        self.rotary_encoder.on_turn_left(self.turned_left)

        self.door_sensor = SensorADA375(16)
        self.door_sensor.on_change(self.door_sensor_callback)

        self.pir_sensor = SensorHCSR501(12, 23)
        self.pir_sensor.on_movement(self.pir_callback)

        self.lcd = LCD()
        self.lcd.show_cursor(False)

        self.led = LED(24)
        self.buzzer = Buzzer(13)
        self.buzzer.off()

        self.reader = SimpleMFRC522()
        self.rfidtag = 0
        self.rfidt = threading.Thread(target=self.rfid)
        self.rfidt.setDaemon(True)
        self.rfidt.start()
        # self.rfidp = multiprocessing.Process(target=self.rfid)
        # self.rfidp.daemon = True
        # self.rfidp.start()

        self.tempt = threading.Thread(target=self.__update_temperature)
        self.tempt.setDaemon(True)
        self.tempt.start()

        self.t = threading.Thread(target=self.main)
        self.t.start()

    def main(self):
        try:
            self.lcd.reset_lcd()
            self.lcd.write_string("ALARMOSTAT")
            while True:
                if not self.stop:
                    self.lcd_text()
                    time.sleep(0.1)
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
        if self.screen < 4:
            self.screen += 1
        else:
            self.screen = 0

    def turned_right(self, e=0):
        self.temperature_set = self.temperature_set + 0.500
        print("right")

    def turned_left(self, e=0):
        self.temperature_set = self.temperature_set - 0.500
        print("left")

    def door_sensor_callback(self, e):
        if self.door_sensor.is_closed():
            print("door closed")
            self.db_add_measurement("closed", "ada375")
        else:
            print("door opened")
            self.db_add_measurement("opened", "ada375")
            if self.armed and not self.triggered and self.door_sensor.walkin:
                self.triggered = True
                wit = threading.Thread(target=self.walkin, args=("ada375",))
                wit.setDaemon(True)
                wit.start()
            elif self.armed and not self.triggered and not self.door_sensor.walkin:
                self.triggered = True
                self.raise_alarm("ada375")

    def pir_callback(self, e=0):
        print("movement detected")
        self.db_add_measurement("movement", "hcsr501")
        if self.armed and not self.triggered and not self.pir_sensor.walkin:
            self.triggered = True
            self.raise_alarm("hcsr501")
        elif self.armed and not self.triggered and self.pir_sensor.walkin:
            self.triggered = True
            wit = threading.Thread(target=self.walkin, args=("hcsr501",))
            wit.setDaemon(True)
            wit.start()

    def get_temperature(self):
        temp = self.temperature_sensor.read_temp()
        self.db_add_measurement(temp, "ds18b20")
        return temp

    def __update_temperature(self):
        while True:
            print("temp update")
            self.current_temperature = self.get_temperature()
            self.temperature_control()
            time.sleep(20)

    def get_door_is_closed(self):
        return self.door_sensor.is_closed()

    def lcd_text(self):
        if self.button_pressed:
            self.lcd.reset_lcd()
            self.button_pressed = False
        self.lcd.move_cursor(0)
        if self.screen == 0:
            ips = check_output(['hostname', '--all-ip-addresses'])
            ips = str(ips)[2:len(ips) - 3]
            ipslist = ips.split(" ")
            self.lcd.write_string(ipslist[0])
            self.lcd.second_line()
            if len(ipslist) >= 2:
                self.lcd.write_string(ipslist[1])

        elif self.screen == 1:
            self.lcd.write_string("Set: {0}C".format(str(self.temperature_set)))
            self.lcd.second_line()
            self.lcd.write_string("Current: ")
            temp = self.current_temperature
            self.lcd.write_string("{0}C  ".format(str(temp)))

        elif self.screen == 2:
            if self.door_sensor.is_closed():
                self.lcd.write_string("Door closed")
            else:
                self.lcd.write_string("Door open  ")

        elif self.screen == 3:
            self.lcd.write_string("No events")
            self.lcd.second_line()
            if self.armed:
                self.lcd.write_string("System ARMED")
            else:
                self.lcd.write_string("System DISARMED")

        elif self.screen == 4:
            now = datetime.datetime.now()
            self.lcd.write_string(now.strftime("%Y-%m-%d"))
            self.lcd.second_line()
            self.lcd.write_string(now.strftime("%H:%M:%S"))

        elif self.screen == 5:
            if self.arming:
                self.lcd.write_string("System ARMING in")
                self.lcd.second_line()
                self.lcd.write_string("{0} seconds      ".format(str(int(self.buzzer.countdown_timer))))
            elif self.triggered and not self.alarm_raised:
                self.lcd.write_string("DISARM NOW")
                self.lcd.second_line()
                self.lcd.write_string("{0} seconds ".format(str(int(self.buzzer.countdown_timer))))
            elif self.alarm_raised:
                self.lcd.write_string("ALARM                           ")
            elif self.armed:
                self.lcd.write_string("System ARMED                    ")
            else:
                self.lcd.write_string("System DISARMED ")
                if self.display_change:
                    self.lcd.second_line()
                    self.lcd.write_string("Hello {0}".format(self.last_event_user))
                    self.display_change = False

    def rfid(self):
        while True:
            self.rfidtag = self.reader.read_id()
            self.db_add_measurement(self.rfidtag, "rfidrc522")
            self.mycursor.execute(
                "SELECT username FROM user WHERE userrfidtag={0};".format(self.rfidtag))
            self.dbout = []
            for x in self.mycursor:
                self.dbout.append(x)
            if len(self.dbout) >= 1:
                print(self.dbout[0][0])
                self.last_event_user = self.dbout[0][0]
                self.lcd.reset_lcd()
                self.change_alarm_status(True)
                time.sleep(2)
            else:
                time.sleep(2)

    def arm(self, rfid=False):
        self.arming = True
        self.buzzer.countdown(self.countdown_walkout)
        if self.arming:
            self.lcd.reset_lcd()
            self.armed = True
            self.buzzer.sound()
        if rfid and self.arming:
            self.db_add_event("system_armed", "rfidrc522", self.last_event_user)
        elif not rfid and self.arming:
            self.db_add_event("system_armed", "web", self.last_event_user)
        self.arming = False

    def change_alarm_status(self, rfid=False):
        if not rfid:
            self.last_event_user = "system"
        if self.armed:
            self.armed = False
            self.display_change = True
            self.buzzer.stop_action = True
            self.triggered = False
            self.alarm_raised = False
            self.buzzer.sound()
            if rfid:
                self.db_add_event("system_disarmed", "rfidrc522", self.last_event_user)
            else:
                self.db_add_event("system_disarmed", "web", self.last_event_user)
        elif self.arming:
            self.arming = False
            self.display_change = True
            self.buzzer.stop_action = True
            self.buzzer.sound()
            if rfid:
                self.db_add_event("system_arming_canceled", "rfidrc522", self.last_event_user)
            else:
                self.db_add_event("system_arming_canceled", "web", self.last_event_user)
        else:
            cd_thread = threading.Thread(target=self.arm, args=(rfid,))
            cd_thread.setDaemon(True)
            cd_thread.start()
            self.screen = 5
            if rfid:
                self.db_add_event("system_arming", "rfidrc522", self.last_event_user)
            else:
                self.db_add_event("system_arming", "web", self.last_event_user)

    def walkin(self, sensor):
        self.db_add_event("walkin_triggered", sensor, "system")
        self.triggered = True
        self.lcd.reset_lcd()
        self.buzzer.countdown(self.countdown_walkin)
        if self.triggered:
            self.lcd.reset_lcd()
            self.raise_alarm(sensor)

    def raise_alarm(self, sensor):
        alarmt = threading.Thread(target=self.buzzer.alarm)
        alarmt.setDaemon(True)
        alarmt.start()
        self.alarm_raised = True
        self.db_add_event("alarm_raised", sensor, "system")

    def db_add_event(self, eventtype, component, user):
        now = datetime.datetime.now()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
        self.mycursor.execute(
            "SELECT iduser FROM user WHERE username=\'{0}\';".format(user))
        self.dbout = []
        for x in self.mycursor:
            self.dbout.append(x)
            print(x)
        iduser = self.dbout[0][0]
        self.mycursor.execute(
            "SELECT idcomponent FROM component WHERE componentname=\'{0}\';".format(component))
        self.dbout = []
        for x in self.mycursor:
            self.dbout.append(x)
            print(x)
        idcomponent = self.dbout[0][0]
        sql = "INSERT INTO event (idevent, eventdatetime, eventtype, idcomponent, iduser, acknowledged) VALUES (DEFAULT, %s, %s, %s, %s, FALSE);"
        val = (formatted_date, eventtype, idcomponent, iduser)
        self.mycursor.execute(sql, val)
        self.mydb.commit()
        self.dbout = []
        for x in self.mycursor:
            self.dbout.append(x)
            print(x)

    def db_add_measurement(self, measuredvalue, component):
        now = datetime.datetime.now()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
        self.mycursor.execute(
            "SELECT idcomponent FROM component WHERE componentname=\'{0}\';".format(component))
        self.dbout = []
        for x in self.mycursor:
            self.dbout.append(x)
            print(x)
        idcomponent = self.dbout[0][0]
        sql = "INSERT INTO measurement (idmeasurement, measurementdatetime, measuredvalue, idcomponent) VALUES (DEFAULT, %s, %s, %s);"
        val = (formatted_date, measuredvalue, idcomponent)
        self.mycursor.execute(sql, val)
        self.mydb.commit()
        self.dbout = []
        for x in self.mycursor:
            self.dbout.append(x)
            print(x)

    def temperature_control(self):
        if self.temperature_set - self.current_temperature >= 0.5 and not self.led.is_on():
            print("aan")
            self.led.on()
        elif self.current_temperature - self.temperature_set >= 0.5 and self.led.is_on():
            print("uit")
            self.led.off()






