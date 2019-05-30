from RPi import GPIO
import threading
from classes.led import LED


class SensorHCSR501:
    def __init__(self, sensor_pin, statusled_pin=0, statusled_isrealtime=False):
        self.sensor_pin = sensor_pin
        self.led = 0
        self.realtime = statusled_isrealtime
        self.callbacks = []
        if statusled_pin:
            self.led = LED(statusled_pin)
            self.led.off()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.sensor_pin, GPIO.IN, GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.sensor_pin, GPIO.RISING, callback=self.__movement, bouncetime=250)
        if self.realtime:  # defining statusled_isrealtime will create a seperate thread to control the led in real time
            t = threading.Thread(target=self.real_time_led)
            t.daemon = True
            t.start()

    def __movement(self, e=0):
        if not self.realtime:
            if self.led:
                self.led.turn_on_for_x_secs(3)
        for callback in self.callbacks:
            callback()

    def on_movement(self, my_callback):
        self.callbacks.append(my_callback)

    def real_time_led(self):
        while True:
            if GPIO.input(self.sensor_pin):
                self.led.on()
            else:
                self.led.off()

