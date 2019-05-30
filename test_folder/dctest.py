from RPi import GPIO
import time
from classes.sensor_ada375 import SensorADA375

sensor = SensorADA375(16)

def foo():
    pass


def joystick_callback(e):
    print("status deurcontact veranderd")
    if sensor.is_closed():
        print("deur is nu dicht")
    else:
        print("deur is nu open")


def main():
    try:
        sensor.on_change(joystick_callback)
        while True:
            if sensor.is_closed():
                print("dicht")
            else:
                print("open")
            time.sleep(1)

    except KeyboardInterrupt:
        pass
    finally:
        GPIO.setwarnings(False)     # get rid of warning when no GPIO pins set up
        GPIO.cleanup()


if __name__ == '__main__':
    main()
