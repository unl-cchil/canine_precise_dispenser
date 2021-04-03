"""precise_dispenser_driver.py

This script controls the onboard Raspberry Pi in the precise canine dispenser developed for Dr. Jeffrey R Stevens
in the Canine Cognition and Human Interaction Laboratory.  The dispenser consists of a 3D printed body with a Raspberry
Pi 4, a stepper motor driver HAT, mounted IR break beam, and a backplane for power and display connections.

Author:     Walker Arce
Date:       04/03/2021
Version:    0.1
"""

import RPi.GPIO as gpio
import time


class PreciseDispenser:
    """A simple class definition to interact with the canine treat dispenser.
    """
    def __init__(self):
        self.DIR = 22
        self.STEP = 23
        self.TREAT = 18
        gpio.setmode(gpio.BCM)
        gpio.setup(self.DIR, gpio.OUT)
        gpio.setup(self.STEP, gpio.OUT)
        gpio.setup(self.TREAT, gpio.IN)
        gpio.add_event_detect(self.TREAT, gpio.FALLING, callback=self.treat_dispensed, bouncetime=100)
        gpio.output(self.DIR, gpio.LOW)
        self.dispensing = False

    def dispense_treat(self):
        self.dispensing = True
        while self.dispensing == True:
            gpio.output(self.STEP, gpio.HIGH)
            time.sleep(0.1)
            gpio.output(self.STEP, gpio.LOW)
            time.sleep(0.1)
        return True

    def dispense_treats(self, num_treats):
        while num_treats is not 0:
            if (self.dispense_treat()):
                num_treats -= 1
                print("Remaining Treats: {0}".format(num_treats))

    def treat_dispensed(self, channel):
        self.dispensing = False

    def close(self):
        gpio.cleanup()

    
