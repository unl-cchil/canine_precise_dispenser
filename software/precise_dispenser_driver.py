"""precise_dispenser_driver.py

This script controls the onboard Raspberry Pi in the precise canine dispenser developed for Dr. Jeffrey R Stevens
in the Canine Cognition and Human Interaction Laboratory.  The dispenser consists of a 3D printed body with a Raspberry
Pi 4, a stepper motor driver HAT, mounted IR break beam, and a backplane for power and display connections.

Author:     Walker Arce
Date:       09/17/2021
Version:    0.3
"""

import RPi.GPIO as gpio
import time


class PreciseDispenser:
    """
    A simple class definition to interact with the canine treat dispenser.
    """
    def __init__(self, loaded_treats=59, timeout=3):
        """
        Initializer for the canine treat dispenser, configures control variables and Pi GPIO.
        :param loaded_treats: The number of treats that are loaded into the dispenser for this session.  Defaults to max, 59 treats.
        :param timeout: The amount of time before the dispenser throw an error between dispensation events
        """
        # Set control variables
        self.step_width = 0.005
        self.loaded_treats = loaded_treats
        self.dispensing_timeout = timeout
        self.dispensing_start = 0
        # Setup pin definitions
        self.ENABLE = 24
        self.RESET = 23
        self.SLEEP = 22
        self.STEP = 18
        self.DIR = 27
        self.TREAT = 17
        # Configure pins
        gpio.setmode(gpio.BCM)
        gpio.setup(self.DIR, gpio.OUT)
        gpio.setup(self.STEP, gpio.OUT)
        gpio.setup(self.TREAT, gpio.IN, pull_up_down=gpio.PUD_UP)
        gpio.setup(self.ENABLE, gpio.OUT)
        gpio.setup(self.RESET, gpio.OUT)
        gpio.setup(self.SLEEP, gpio.OUT)
        # Set outputs and trigger events
        gpio.add_event_detect(self.TREAT, gpio.FALLING, callback=self.treat_dispensed, bouncetime=100)
        gpio.output(self.DIR, gpio.LOW)
        gpio.output(self.ENABLE, gpio.LOW)
        gpio.output(self.RESET, gpio.HIGH)
        gpio.output(self.SLEEP, gpio.HIGH)
        # Initialize the dispensing variable to False
        self.dispensing = False
        self.step_check = 0

    def edge_wait_thread(self):
        gpio.wait_for_edge(self.TREAT, gpio.FALLING)

    def dispense_treat_angle(self):
        for i in range(0, 53):
            self.forward_step()

    def terminate(self):
        self.stop_thread = True

    def forward_step(self):
        gpio.output(self.STEP, gpio.HIGH)
        time.sleep(self.step_width)
        gpio.output(self.STEP, gpio.LOW)
        time.sleep(self.step_width)

    def dispense_treat(self):
        """
        Function to dispense a single treat.  Should not be used directly, use dispense_treats for error handling.
        :returns: True for successful dispensation of a single treat, False for a failure to dispense the treat.
        """
        if self.step_check < 0:
            self.step_check = 0
        self.step_check += 54
        self.start = time.time()
        self.dispensing = True
        while self.dispensing:
            if time.time() - self.start > self.dispensing_timeout:
                return False
            self.forward_step()
            self.step_check -= 1
            if self.dispensing and self.step_check == 0:
                self.dispensing = False
        return True

    def dispense_treats(self, num_treats):
        """
        Dispenses the specified number of treats.  If the requested number of treats is greater than the remaining treats, a ValueError is thrown.  If the treat dispenser
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
        """
        A callback function for when a treat is dispensed.  This is detected on the falling edge of the IR break beam.
        :param channel: The channel to identify the callback source.
        :returns: None.
        """
        self.start = time.time()
        self.dispensing = False

    def close(self):
        """Closes the dispenser object and cleans up the GPIO assignments.

        :returns: None.
        """
        gpio.remove_event_detect(self.TREAT)
        gpio.cleanup()
