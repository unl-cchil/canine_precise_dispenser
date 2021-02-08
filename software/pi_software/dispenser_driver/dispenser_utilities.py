"""dispenser_utilities.py

This script creates a serial interface to the retrofitted Treat & Train device developed
for Dr. Jeffrey Stevens' canine operant conditioning studies.  The member methods
comply with the USB protocol developed to interact with its internal state machine
and encapsulates a comport definition and a configurable delay period.

Supported device operations include (replace X with relevant value):
    Dispense treats in [0, 9] range:                            CDXE
    Dispense treats in [0, 255] range:                          CAXE
    Update the RF remote dispensation amount in range [0, 9]:   CBXE
    Update motor speed in range [0, 255]:                       CMXE
    Debug sensors:                                              CP0E
    Wheel test routine:                                         CF0E

    Note: The value placed in X will be represented in ASCII, so for the 'D' command it will be valid in ASCII range
    [0, 9], in which case the device will convert the value passed from ASCII to decimal.  In the case of the 'A'
    command, it treats the ASCII value as the number of treats and does not convert the value to decimal.

    Supports version 0.4 of the dispenser firmware.

Author:     Walker Arce
Date:       05/17/2020
Version:    0.3
"""

import serial
import serial.tools.list_ports
import time


class CanineDispenser:
    """A simple class definition to interact with the canine treat dispenser.

    self.comport - pyserial USB port object used to communicate with the device.
    self.delay - period in seconds to wait before sending command to allow for reset.
    """
    def __init__(self, comport_name='/dev/ttyACM0', delay=1):
        """
        Parameters
        :param comport_name: str
            The name of the USB port to connect to, i.e. '/dev/ttyACM0' or 'COM31'
        :param delay: int or float
            The period in seconds to wait before sending command to allow for reset
        """
        try:
            self.comport = serial.Serial(comport_name, baudrate=9600, timeout=None)
            self.delay = delay
        except serial.SerialException:
            print('Failed to open serial port, double check port and try again.')
            print('Port: ' + comport_name)

    def update_rf_amount(self, num_treats):
        """Sends a command to the dispenser to update the number of treats dispensed when using the RF remote.
        Parameters
        :param num_treats: int
            The number of treats in range [0, 9] to dispense
        :return: byte
            0 for success, 1 for failure
        """
        if num_treats < 0 or num_treats > 9:
            print('Number of treats must be within range [0, 9], please retry.')
            return
        if self.comport.isOpen():
            command = 'CB'.encode('ascii') + str(num_treats).encode('ascii') + 'E'.encode('ascii')
            time.sleep(self.delay)
            self.comport.write(command)
        return self.comport.read(1)

    def dispense_treats(self, num_treats):
        """Sends command to dispense treats in range [0, 9]
        Parameters
        :param num_treats: int
            The number of treats in range [0, 9] to dispense
        :return: byte
            0 for success, 1 for failure
        """
        if int(num_treats) < 0 or int(num_treats) > 9:
            print('Number of treats must be within range [0, 9], please retry.  '
                  'Use dispense_treats_multi to dispense more treats.')
            return
        if self.comport.isOpen():
            command = 'CD'.encode('ascii') + str(num_treats).encode('ascii') + 'E'.encode('ascii')
            time.sleep(self.delay)
            self.comport.write(command)
        else:
            print('No open comport on this object.')
            return
        return self.comport.read(1)

    def dispense_treats_multi(self, num_treats):
        """Sends command to dispense a greater amount of treats, in range [0, 255]
        Parameters
        :param num_treats: int
            The number of treats to dispense in range [0, 255]
        :return: byte
            0 for success, 1 for failure
        """
        if int(num_treats) < 0 or int(num_treats) > 255:
            print('Number of treats must be within range [0, 255], please retry.')
            return
        if self.comport.isOpen():
            command = 'CA'.encode('ascii') + chr(num_treats).encode('ascii') + 'E'.encode('ascii')
            time.sleep(self.delay)
            self.comport.write(command)
        return self.comport.read(1)

    def change_motor_speed(self, motor_speed):
        """Sends command to update the motor speed with provided value in range [0, 255]
        Note: Increasing the motor speed beyond 127 (default) is not recommended for expected use case.
        Parameters
        :param motor_speed: int
            Speed of the motor in range [0, 255] or [0V, 12V] equivalent
        :return: byte
            0 for success, 1 for failure
        """
        if motor_speed < 0 or motor_speed > 255:
            print('Motor speed must be within valid range [0, 255], please retry.')
            return
        if self.comport.isOpen():
            command = 'CM'.encode('ascii') + chr(motor_speed).encode('ascii') + 'E'.encode('ascii')
            time.sleep(self.delay)
            self.comport.write(command)
        return self.comport.read(1)

    def debug_sensors(self):
        """Sends command to get the current state of the sensors, used for debugging sensor issues
        :return: str
            String representing the current value of the sensors
        """
        if self.comport.isOpen():
            self.comport.write('CP0E'.encode('ascii'))
        return read_dispenser_line(self)

    def wheel_test(self):
        """Sends command to run the wheel test procedure
        Try breaking the eyelet sensor to verify operation or updating the motor speed to change the max speed
        :return: None
            Loop is terminated by the dispenser sending a '0' for successful completion
        """
        if self.comport.isOpen():
            self.comport.write('CF0E'.encode('ascii'))
            wheel_out = ""
            while wheel_out != b'0':
                wheel_out = read_dispenser_line(self)
                if wheel_out[-3:] != '127':
                    print(wheel_out)
                elif wheel_out[-3:] == '127':
                    print(wheel_out)
                    wheel_out = self.comport.read(1)

    def disconnect(self):
        """Disconnects the internal comport object.
        :return: none
        """
        self.comport.close()


def list_comports():
    """Wrapper utility to show exposed COM ports.
    :return: list
        List consisting of serial object representing the available COM ports
    """
    comports = serial.tools.list_ports.comports()
    print([comport.device for comport in comports])
    return comports


def read_dispenser_line(dispenser):
    """Wrapper function on serial.readline() function to handle Arduino Serial.println(). Use in loop to handle
    continuous output.
    Source: https://stackoverflow.com/questions/24074914/python-to-arduino-serial-read-write
    :param dispenser: CanineDispenser
        Pass a dispenser object with an open comport
    :return: str
        Trimmed Arduino output string
    """
    line_out = str(dispenser.comport.readline())
    return line_out[2:][:-5]


def dispenser_test(expected_dispensers):
    """This function is to be used to test multiple dispensers for basic functionality
    Parameters
    :param expected_dispensers: int
        The number of dispensers to be connected to
    :return: None
        Used to break while loop, returns None value
    """
    comports = list_comports()

    dispensers = []

    while expected_dispensers != 0:
        try:
            com_select = input("Select COM port from list above: ")
            if int(com_select) < 0 or int(com_select) > len(comports) - 1:
                print('Invalid input. Valid range is 0 to', len(comports) - 1)
            else:
                dispensers.append(CanineDispenser(comport_name=comports[int(com_select)].device))
                expected_dispensers -= 1
        except:
            print('Invalid COM port selected, use numerals in range [0, 9]. Returning control.')
            return

    while True:
        command = input('Enter number of treats to dispense [0, 255] or "exit" to quit: ')
        try:
            if command == 'exit':
                for dispenser in dispensers:
                    dispenser.disconnect()
                return
            elif int(command) < 0 or int(command) > 255:
                print('Invalid input. Valid range is [0, 255].')
            else:
                for dispenser in dispensers:
                    if int(command) > 9:
                        out = dispenser.dispense_treats_multi(int(command))
                    elif int(command) < 10:
                        out = dispenser.dispense_treats(command)
                    if out == b'1':
                        print('Invalid command for', dispenser.comport.name)
                    elif out == b'0':
                        print('Successful command for', dispenser.comport.name)
        except:
            print('Invalid input. Only use numerals [0, 9] or type "exit". Returning control.')
            return


def dispenser_functionality_test(comport_name):
    """Sends all commands that return a byte return code.
    Parameters
    :param comport_name: str
        Name of the COM port, i.e. '/dev/ttyACM0' or 'COM31'
    :return: None
        Prints state of the commands to command line
    """
    dispenser = CanineDispenser(comport_name=comport_name)
    D_out = dispenser.dispense_treats(1)
    A_out = dispenser.dispense_treats_multi(1)
    M_out = dispenser.change_motor_speed(127)
    RF_out = dispenser.update_rf_amount(1)

    if D_out == b'0' and A_out == b'0' and M_out == b'0' and RF_out == b'0':
        print('D: ', D_out, '\nA: ', A_out, '\nM: ', M_out, '\nRF: ', RF_out, '\nDispenser operating successfully.')
    else:
        print('D: ', D_out, '\nA: ', A_out, '\nM: ', M_out, '\nRF: ', RF_out, '\nDispenser not operating correctly.')
