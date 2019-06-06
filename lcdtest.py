from classes.lcd import LCD
from RPi import GPIO
import time

lcd = LCD()

def main():
    try:
        while True:
            lcd.reset_lcd()
            lcd.show_cursor(False)
            time.sleep(2)
            lcd.write_string("lijn tekst langer dan 16 karakters", False)
            time.sleep(2)
            while True:
                lcd.write_instructions(0x18)
                time.sleep(0.3)

            # lcd.write_instructions(	0x1C) # shift right

    except KeyboardInterrupt:
        pass
    finally:
        GPIO.setwarnings(False)     # get rid of warning when no GPIO pins set up
        GPIO.cleanup()


if __name__ == '__main__':
    main()