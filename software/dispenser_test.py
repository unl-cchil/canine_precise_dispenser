from precise_dispenser_driver import PreciseDispenser
import time

dispenser = PreciseDispenser(59, timeout=3)

for i in range(1, 11):
    try:
        dispenser.dispense_treats(i)
        print("Dispensed {0} treats".format(i))
    except ValueError as e:
        print(e)
    time.sleep(3)
dispenser.close()