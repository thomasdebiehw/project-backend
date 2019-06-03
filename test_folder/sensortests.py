from RPi import GPIO
import time
from classes.sensor_ada375 import SensorADA375
from classes.sensor_hcsr501 import SensorHCSR501
from classes.lcd import LCD
from classes.rotary_encoder import RotaryEncoder

sensor = SensorADA375(16)
pir = SensorHCSR501(12, 14, True)
lcd = LCD()
renc = RotaryEncoder(26, 24, 19)


def foo():
    pass


def sensor_callback(e):
    print("status deurcontact veranderd")
    if sensor.is_closed():
        print("deur is nu dicht")
        lcd.reset_lcd()
        lcd.write_string("DEUR DICHT")
    else:
        print("deur is nu open")
        lcd.reset_lcd()
        lcd.write_string("DEUR OPEN")


def pir_callback(e=0):
    print("movement detected")
    lcd.reset_lcd()
    lcd.write_string("BEWEGING")


def left_callback(e=0):
    print("turned left")


def right_callback(e=0):
    print("turned right")


def main():
    try:
        sensor.on_change(sensor_callback)
        pir.on_movement(pir_callback)
        renc.on_turn_left(left_callback)
        renc.on_turn_right(right_callback)
        lcd.reset_lcd()
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
