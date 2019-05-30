from RPi import GPIO
import time


class Buzzer:
    def __init__(self, buzzer_pin):
        self.buzzer_pin = buzzer_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.buzzer_pin, GPIO.OUT)
        GPIO.output(self.buzzer_pin, GPIO.HIGH)

    def on(self):
        GPIO.output(self.buzzer_pin, GPIO.HIGH)

    def off(self):
        GPIO.output(self.buzzer_pin, GPIO.LOW)

    def countdown(self, duration):
        for i in range(duration*3):
            self.on()
            time.sleep(0.1)
            self.off()
            time.sleep(0.05)
        self.on()
        time.sleep(2)
        self.off()
