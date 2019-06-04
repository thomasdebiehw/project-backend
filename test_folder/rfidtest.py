from time import sleep
from mfrc522 import SimpleMFRC522
from RPi import GPIO
GPIO.setmode(GPIO.BCM)
reader = SimpleMFRC522()
from classes.lcd import LCD


lcd = LCD()
lcd.reset_lcd()
try:
    while True:
        print("Hold a tag near the reader")
        id, text = reader.read()
        print("ID: %s\nText: %s" % (id,text))
        lcd.reset_lcd()
        lcd.write_string(str(id))
        sleep(5)
except KeyboardInterrupt:
    GPIO.cleanup()
    raise