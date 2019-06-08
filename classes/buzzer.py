from RPi import GPIO
import time


class Buzzer:
    def __init__(self, buzzer_pin):
        self.buzzer_pin = buzzer_pin
        self.stop_countdown = False
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.buzzer_pin, GPIO.OUT)
        GPIO.output(self.buzzer_pin, GPIO.HIGH)

    def on(self):
        GPIO.output(self.buzzer_pin, GPIO.HIGH)

    def off(self):
        GPIO.output(self.buzzer_pin, GPIO.LOW)

    def countdown(self, duration):
        self.stop_countdown = False
        for i in range(duration*3):
            if self.stop_countdown:
                break
            self.on()
            time.sleep(0.1)
            self.off()
            time.sleep(0.05)
        if not self.stop_countdown:
            self.on()
            time.sleep(2)
        self.off()
        self.stop_countdown = False
