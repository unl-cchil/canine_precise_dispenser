"""precise_dispenser_driver.py

This script controls the onboard Raspberry Pi in the precise canine dispenser developed for Dr. Jeffrey R Stevens
in the Canine Cognition and Human Interaction Laboratory.  The dispenser consists of a 3D printed body with a Raspberry
Pi 4, a stepper motor driver HAT, mounted IR break beam, and a backplane for power and display connections.

Author:     Walker Arce
Date:       04/03/2021
Version:    0.2
"""

import RPi.GPIO as gpio
import time


class PreciseDispenser:
    """
    A simple class definition to interact with the canine treat dispenser.
    """
    def __init__(self, loaded_treats=59, timeout=3, version="BB"):
        """Initializer for the canine treat dispenser, configures control variables and Pi GPIO.

        :param loaded_treats: The number of treats that are loaded into the dispenser for this session.  Defaults to max, 59 treats.
        :param timeout: The amount of time before the dispenser throw an error between dispensation events
        :param version: The HAT version that is being used, "BB" for breadboard and "P" for production
        :returns: None.
        """
        # Set control variables
        self.loaded_treats = loaded_treats
        self.dispensing_timeout = timeout
        self.dispensing_start = 0
        # Setup pin definitions
        if version == "BB":
            self.TREAT = 18
            self.DIR = 22
            self.STEP = 23
        elif version == "P":
            self.ENABLE = 25
            self.RESET = 8
            self.SLEEP = 7
            self.STEP = 12
            self.DIR = 16
            self.BREAK = 20
        # Configure pins
        gpio.setmode(gpio.BCM)
        gpio.setup(self.DIR, gpio.OUT)
        gpio.setup(self.STEP, gpio.OUT)
        gpio.setup(self.TREAT, gpio.IN)
        # Set outputs and trigger events
        gpio.add_event_detect(self.TREAT, gpio.FALLING, callback=self.treat_dispensed, bouncetime=100)
        gpio.output(self.DIR, gpio.LOW)
        # Initialize the dispensing variable to False
        self.dispensing = False

    def dispense_treat(self):
        """Function to dispense a single treat.  Should not be used directly, use dispense_treats for error handling.

        :returns: True for successful dispensation of a single treat, False for a failure to dispense the treat.
        """
        self.dispensing = True
        self.start = time.time()
        while self.dispensing == True:
            gpio.output(self.STEP, gpio.HIGH)
            time.sleep(0.1)
            gpio.output(self.STEP, gpio.LOW)
            time.sleep(0.1)
            if time.time() - self.start > self.dispensing_timeout:
                return False
        return True

    def dispense_treats(self, num_treats):
        """Dispenses the specified number of treats.  If the requested number of treats is greater than the remaining treats, a ValueError is thrown.  If the treat dispenser
        loop times out, a ValueError is thrown.

        :param num_treats: A number between 1 and the remaining number of treats.
        :returns: None.  Throws ValueError when an error event is encountered.
        """
        if num_treats > self.loaded_treats:
            raise ValueError("Not enough treats remaining to dispense {0} treats!".format(num_treats))
        while num_treats is not 0:
            if (self.dispense_treat()):
                num_treats -= 1
                self.loaded_treats -= 1
            else:
                raise ValueError("Treat was unable to dispense, {0} treats remaining with {1} treats in jogger, check for jams!".format(num_treats, self.loaded_treats))

    def treat_dispensed(self, channel):
        """A callback function for when a treat is dispensed.  This is detected on the falling edge of the IR break beam.

        :param channel: The channel to identify the callback source.
        :returns: None.
        """
        self.start = time.time()
        self.dispensing = False

    def close(self):
        """Closes the dispenser object and cleans up the GPIO assignments.

        :returns: None.
        """
        gpio.cleanup()

    
