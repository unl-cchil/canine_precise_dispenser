# Raspberry Pi controlled precise treat dispenser
**This project provides the source for a precise canine treat dispenser designed for numerical discrimination tasks.**

### Overview

https://user-images.githubusercontent.com/22334349/143482424-4f7f6dd4-f7b3-43dc-927e-87879f6ca861.MOV

### Raspberry Pi Image
The SD card image for the Raspberry Pi has all dependencies installed and only needs to have its access point configured using pi-ap.  The image can be found [here](https://drive.google.com/file/d/1r1gbtBNyjnHum-6QpTX6uGOvL8lcQ7Pt/view?usp=sharing).  Use an SD card flasher to write this image to a bootable media, such as balenaEtcher, Win32DiskImager, or other similar software.

### Interfacing Example
```
from precise_dispenser_driver import PreciseDispenser

dispenser = PreciseDispenser()
try:
	dispenser.dispense_treats(10)
	print(“Successfully dispensed ten treats.”)
except ValueError as e:
	print(e)
dispenser.close()
```

### License

The software and hardware designs are available under a [Creative Commons Attribution-ShareAlike 4.0 International Public License (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/). You are free to:

* Share — copy and redistribute the material in any medium or format
* Adapt — remix, transform, and build upon the material for any purpose, even commercially. 

Under the following terms:

* Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
* ShareAlike — If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original. 


### Contact

This project was conducted by the [Canine Cognition and Human Interaction Lab](https://dogcog.unl.edu). For questions, please contact the developer Walker Arce (warce@unomaha.edu) or the principal investigator Jeffrey R. Stevens (jeffrey.r.stevens@gmail.com).

### Citation
