from RPi import GPIO
import time
from classes.sensor_ada375 import SensorADA375
from classes.sensor_hcsr501 import SensorHCSR501

sensor = SensorADA375(16)
pir = SensorHCSR501(12, 14, True)


def foo():
    pass


def sensor_callback(e):
    print("status deurcontact veranderd")
    if sensor.is_closed():
        print("deur is nu dicht")
    else:
        print("deur is nu open")


def pir_callback(e=0):
    print("movement detected")


def main():
    try:
        sensor.on_change(sensor_callback)
        pir.on_movement(pir_callback)
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
