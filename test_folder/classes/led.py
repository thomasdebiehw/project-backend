from RPi import GPIO
import threading


class LED:
    def __init__(self, led_pin):
        self.led_pin = led_pin
        self.is_on = True
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.led_pin, GPIO.OUT)
        GPIO.output(self.led_pin, GPIO.HIGH)
        self.t = threading.Timer(1, self.off)

    def on(self):
        if not self.is_on:
            GPIO.output(self.led_pin, GPIO.HIGH)
            self.is_on = True

    def off(self):
        if self.is_on:
            GPIO.output(self.led_pin, GPIO.LOW)
            self.is_on = False

    def turn_on_for_x_secs(self, seconds):  # non-blocking
        self.on()
        self.t.cancel()
        self.t = threading.Timer(seconds, self.off)
        self.t.start()
