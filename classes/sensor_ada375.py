from RPi import GPIO


class SensorADA375:
    def __init__(self, sensor_pin):
        self.sensor_pin = sensor_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def on_change(self, my_callback):
        GPIO.add_event_detect(self.sensor_pin, GPIO.BOTH, callback=my_callback, bouncetime=250)

    def is_closed(self):
        if GPIO.input(self.sensor_pin) == 1:
            return False
        else:
            return True
