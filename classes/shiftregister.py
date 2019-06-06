from RPi import GPIO
import time

GPIO.setmode(GPIO.BCM)


class Shiftregister:
    def __init__(self, DS = 17, OE = 27, ST_CP = 22, SH_CP = 5, MR = 6):
        self.DS = DS
        self.OE = OE
        self.ST_CP = ST_CP
        self.SH_CP = SH_CP
        self.MR = MR

        self.__initGPIO()
        self.__init_shift_register()

    def __initGPIO(self):
        GPIO.setup(self.DS, GPIO.OUT)
        GPIO.setup(self.OE, GPIO.OUT)
        GPIO.setup(self.ST_CP, GPIO.OUT)
        GPIO.setup(self.SH_CP, GPIO.OUT)
        GPIO.setup(self.MR, GPIO.OUT)

    def __init_shift_register(self):
        GPIO.output(self.DS, GPIO.LOW)
        GPIO.output(self.ST_CP, GPIO.LOW)
        GPIO.output(self.SH_CP, GPIO.LOW)
        GPIO.output(self.MR, GPIO.HIGH)
        GPIO.output(self.OE, GPIO.LOW)

    def write_one_bit(self, value):
        GPIO.output(self.DS, value)
        GPIO.output(self.SH_CP, GPIO.HIGH)
        GPIO.output(self.SH_CP, GPIO.LOW)
        GPIO.output(self.DS, GPIO.LOW)

    def write_one_byte(self, value):
        for bit in range(0, 8):
            GPIO.output(self.DS, 0x80 & (value << bit))
            GPIO.output(self.SH_CP, GPIO.HIGH)
            # time.sleep(0.001)
            GPIO.output(self.SH_CP, GPIO.LOW)
        GPIO.output(self.ST_CP, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(self.ST_CP, GPIO.LOW)

    def copy_to_storage_register(self):
        GPIO.output(self.ST_CP, GPIO.HIGH)
        GPIO.output(self.ST_CP, GPIO.LOW)

    def empty_storage_register(self):
        GPIO.output(self.MR, GPIO.LOW)
        GPIO.output(self.OE, GPIO.HIGH)
        self.copy_to_storage_register()
        self.__init_shift_register()

