from RPi import GPIO
import time
import threading
from classes.sensor_ds18b20 import SensorDS18B20


class HWInterface:
    def __init__(self):
        self.a = "running"
        t = threading.Thread(target=self.main)
        t.start()

    def main(self):
        try:
            while True:
                print(self.a)
                time.sleep(1)

        except KeyboardInterrupt:
            pass
        finally:
            GPIO.cleanup()
            print("gestopt")

