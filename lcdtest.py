from classes.lcd import LCD
from RPi import GPIO
import time

lcd = LCD()

def main():
    try:
        while True:
            lcd.reset_lcd()
            time.sleep(2)

            lcd.move_cursor(1)
            time.sleep(2)
            lcd.show_cursor(False)
            time.sleep(2)

            lcd.write_string("test")
            time.sleep(2)

    except KeyboardInterrupt:
        pass
    finally:
        GPIO.setwarnings(False)     # get rid of warning when no GPIO pins set up
        GPIO.cleanup()


if __name__ == '__main__':
    main()