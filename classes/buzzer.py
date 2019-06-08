from RPi import GPIO
import time


class Buzzer:
    def __init__(self, buzzer_pin):
        self.buzzer_pin = buzzer_pin
        self.stop_countdown = False
        self.countdown_timer = 0
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.buzzer_pin, GPIO.OUT)
        GPIO.output(self.buzzer_pin, GPIO.HIGH)

    def on(self):
        GPIO.output(self.buzzer_pin, GPIO.HIGH)

    def off(self):
        GPIO.output(self.buzzer_pin, GPIO.LOW)

    def countdown(self, duration):
        self.stop_countdown = False
        self.countdown_timer = duration
        for i in range(duration - int(duration*0.2)):
            if self.stop_countdown:
                break
            for i in range(0,2):
                self.on()
                time.sleep(0.1)
                self.off()
                time.sleep(0.4)
            self.countdown_timer -= 1
        if not self.stop_countdown:
            self.on()
            for i in range(int(duration*0.2)):
                time.sleep(1)
                self.countdown_timer -= 1
        self.off()
        self.stop_countdown = False

    def sound(self):
        for i in range(0, 3):
            time.sleep(0.05)
            self.on()
            time.sleep(0.1)
            self.off()
