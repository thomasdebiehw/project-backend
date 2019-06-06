from RPi import GPIO
import threading


class RotaryEncoder:
    def __init__(self, CLK, DT, SW):
        self.CLK = CLK
        self.DT = DT
        self.SW = SW
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.CLK, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.DT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.SW, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.clkState = GPIO.input(self.CLK)
        self.clkLastState = GPIO.input(self.CLK)
        self.dtState = GPIO.input(self.DT)
        self.counter = 0
        GPIO.add_event_detect(self.CLK, GPIO.FALLING, callback=self.__change, bouncetime=1)
        self.callbacks = [self.__foo, self.__foo]

    def __foo(self):
        pass

    # def __change(self, e=0):
    #     self.clkState = GPIO.input(self.CLK)
    #     self.dtState = GPIO.input(self.DT)
    #     if self.clkState != self.clkLastState:
    #         if GPIO.event_detected(self.CLK):
    #             if self.dtState == self.clkState:  # turned to the left
    #                 self.callbacks[0]()
    #             else:  # turned to the right
    #                 self.callbacks[1]()
    #     self.clkLastState = self.clkState

    def __change(self, e=0):
        self.clkState = GPIO.input(self.CLK)

        if self.clkState != self.clkLastState:
            self.dtState = GPIO.input(self.DT)
            if self.dtState == self.clkState:  # turned to the left
                self.callbacks[0]()
            else:  # turned to the right
                self.callbacks[1]()
        self.clkLastState = self.clkState

    def on_turn_left(self, callback):
        self.callbacks[0] = callback

    def on_turn_right(self, callback):
        self.callbacks[1] = callback

    def on_button_press(self, callback):
        GPIO.add_event_detect(self.SW, GPIO.FALLING, callback=callback, bouncetime=500)

