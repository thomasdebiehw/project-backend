from RPi import GPIO
import threading


class LED:
    def __init__(self, led_pin):
        self.led_pin = led_pin
        self.__is_on_bool = True
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.led_pin, GPIO.OUT)
        GPIO.output(self.led_pin, GPIO.HIGH)
        self.t = threading.Timer(1, self.off)

    def on(self):
        if not self.__is_on_bool:
            GPIO.output(self.led_pin, GPIO.HIGH)
            self.__is_on_bool = True

    def off(self):
        if self.__is_on_bool:
            GPIO.output(self.led_pin, GPIO.LOW)
            self.__is_on_bool = False

    def turn_on_for_x_secs(self, seconds):  # non-blocking
        self.on()
        self.t.cancel()
        self.t = threading.Timer(seconds, self.off)
        self.t.start()

    def is_on(self):
        return self.__is_on()

    def toggle(self):
        if self.__is_on_bool:
            self.off()
        else:
            self.on()
