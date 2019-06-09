from RPi import GPIO
from classes.led import LED


class SensorHCSR501:
    def __init__(self, sensor_pin, statusled_pin=0, walkin = False):
        self.sensor_pin = sensor_pin
        self.led = 0
        self.walkin = walkin
        self.callbacks = []
        if statusled_pin:
            self.led = LED(statusled_pin)
            self.led.off()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.sensor_pin, GPIO.IN, GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.sensor_pin, GPIO.BOTH, callback=self.__callback, bouncetime=250)

    def __callback(self, e=0):
        if GPIO.input(self.sensor_pin):
            if self.led:
                self.led.on()
            for callback in self.callbacks:
                callback()
        else:
            if self.led:
                self.led.off()

    def on_movement(self, my_callback):
        self.callbacks.append(my_callback)

