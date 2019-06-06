from RPi import GPIO
from classes.shiftregister import Shiftregister
import time


class LCD:
    def __init__(self, is_vier_bits=0, e=20, rs=21):
        super().__init__()
        self.sr = Shiftregister()
        self.is_vier_bits = is_vier_bits
        self.e = e
        self.rs = rs
        self.__show_cursor = True

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.rs, GPIO.OUT)
        GPIO.setup(self.e, GPIO.OUT)
        self.reset_lcd()

    def __pulse__(self):
        GPIO.output(self.e, 1)
        GPIO.output(self.e, 0)
        # time.sleep(0.01)

    def __set_data_bit__(self, byte):
        for a in range(8):
            self.sr.write_one_byte(byte)
            self.sr.copy_to_storage_register()

    def write_character(self, value):
        GPIO.output(self.rs, 1)
        self.__set_data_bit__(ord(value))
        self.__pulse__()

    def write_string(self, value):
        count = 0
        for i in value:
            if count == 16:
                self.second_line()
            self.write_character(i)
            count += 1
            # time.sleep(0.01)

    def write_instructions(self, value):
        GPIO.output(self.rs, 0)
        self.__set_data_bit__(value)
        self.__pulse__()
        time.sleep(0.01)

    def second_line(self):
        GPIO.output(self.rs, 0)
        self.__set_data_bit__(0b10101000)
        self.__pulse__()

    def square(self):
        GPIO.output(self.rs, 1)
        self.__set_data_bit__(219)
        self.__pulse__()

    def reset_lcd(self):
        self.write_instructions(0b00111000)
        self.write_instructions(0b00001111)
        self.write_instructions(1)
        if not self.__show_cursor:
            self.write_instructions(0x0C)

    def move_cursor(self, location):
        if location > 16:
            loc = 0x80 + 0x40 + location-16
        else:
            loc = 0x80 + location
        self.write_instructions(loc)

    def show_cursor(self, boolean):
        if boolean:
            self.write_instructions(0x0F)
            self.__show_cursor = True
        else:
            self.write_instructions(0x0C)
            self.__show_cursor = False


