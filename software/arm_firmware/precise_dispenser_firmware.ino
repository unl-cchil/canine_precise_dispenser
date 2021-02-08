/*
 * Treat & Train Custom Driver
 * Author: Walker Arce, May 2020
 * 
 * This program is used to drive the Treat & Train device for pellet dispensation.
 * It operates using a simple USB command protocol and can also be driven by the use of the
 * accompanying RF remote.
 * 
 * The current operation of the system is as follows:
 *    1. A command is sent over USB to dispense a pellet,
 *        a. Drives wheel until pellet sensor is broken or wheel goes a full rotation.
 *    2. The button 'Dispense' is clicked on the RF remote
 *        a. Drives wheel until pellet sensor is broken or wheel goes a full rotation.
 *        
 * The motor can be driven at a variety of levels, for the second state of operation, it will be driven at half speed (6V DC).
 * 
 * This initial version is meant to simply replicate functionality.  The Treat & Train can be restored to original functionality
 * by reconnecting the internal board and sensors.
 * 
 * v0.4
 * 17 May 2020
 */

#include "pins.h" 

#define Serial        SerialUSB
#define SerialDebug   false
#define VOLTAGE_SCALE 3.3
#define ADC_PRECISION 4096.0
#define LOGIC_LOW     0.09

//Function Prototypes
/*
 *  Functionality test of the wheel movement and sensor outputs. 
 *  No parameters or return values.
 */
void testWheel();
/*
 *  Prints out the current state of the IR sensors. 
 *  No parameters or return values.
 */
void debugSensors();
/*
 *  Begins routine to dispense the number of treats specified.
 *  cycles - int, the number of treats to be dispensed.
 *  motorSpeed - int, the speed of the motor [0, 255].
 *  motorDir - bool, clockwise or counter-clockwise.
 *  isASCII - bool, if cycles is encoded as ASCII, then it will be converted to decimal.
 *  returns - bool, stops motor and returns True when complete.
 */
bool dispenseCommand(int cycles, int motorSpeed, bool motorDir, bool isASCII);
/*
 *  Converts a raw float value to a specified precision, i.e. 1.945 -> 1.95.
 *  raw - float, the raw floating point number to be converted.
 *  precision - int, the number of values after the decimal point.
 *  returns - float, converted float value.
 */
float roundFloat(float raw, int precision);
/*
 *  Returns the ADC reading from the specified pin after the specified number of samples.
 *  pin - int, the pin to be read from.
 *  samples - int, the number of times to average over before returning a value.
 *  returns - float, the raw floating point value of the pin, in volts.
 */
float getVoltage(int pin, int samples);
/*
 *  Function driven by getVoltage, returns the raw ADC reading averaged over the sampling period.
 *  pin - int, the pin to be read from.
 *  numReadings - int, the number of readings to average over.
 *  returns - int, raw, averaged ADC reading.
 */
int getAverageReading(int pin, int numReadings);
/*
 *  Function to move the dispenser wheel motor, at a specified speed and in a specified direction.
 *  motorSpeed - int, speed to move the motor at [0, 255].
 *  motorDir - bool, clockwise or counter-clockwise.
 */
void moveMotor(int motorSpeed, bool motorDir);
/*
 *  Deasserts the motor control lines.
 *  No parameters or return values.
 */
void stopMotor();
/*
 *  Initializes the pins specified in the file pins.h
 *  No parameters or return values.
 */
void initPins();

//Voltage sensing variables
float Vout = 0.00;
float Vin = 0.00;
float R1 = 1000000.00; // resistance of R1 (1M) 
float R2 = 1000000.00; // resistance of R2 (1M) 

//Peripheral sampling variables
float sampleVoltage = 0;
float wheelVoltage = 0;
float treatVoltage = 0;
int clickSignal = 0;

int clickCycles = 1;
int globalMotorSpeed = 127;

void setup()
{
   Serial.begin(9600);
   analogReadResolution(12); // Set analog input resolution to max, 12-bits
   initPins();
   stopMotor();
   //while(1){ debugSensors(); }
   //moveMotor(125, true);
}

void loop()
{
  //Listen for the RF remote
  if (digitalRead(CLICK) == HIGH)
  {
    if(dispenseCommand(clickCycles, 127, false, false))
    {
      Serial.println("Successfully dispensed");
    }
    else
    {
      Serial.println("Error occurred");
    }
    while(digitalRead(CLICK) == HIGH) {}
  }
  //Wait for USB input
  while(Serial.available() > 0)
  {
    char command[4];
    size_t bytesRead = Serial.readBytes(command, 4);
    //Check for 'C' being sent
    if (command[0] == 67 && command[3] == 69)
    {
      switch(command[1])
      {
        //Check for 'F' being send
        //This performs the motor test to verify funtionality
        case 70:
          testWheel();
          Serial.print(0x00, HEX);
          break;
        //Check for 'D' being sent
        //This dispenses the specified number of treats, give or take.
        case 68:
          if (dispenseCommand(command[2], globalMotorSpeed, false, true))
          {
            Serial.print(0x00, HEX);
          }
          else
          {
            Serial.print(0x01, HEX);
          }
          break;
        //Check for 'P' being sent
        //This prints out the current state of the internal sensors.
        case 80:
          debugSensors();
          break;
        //Check for 'B' being sent
        //This updates the number of treats dispensed when RF remote is clicked
        case 66:
          clickCycles = command[2] - 0x30;
          Serial.print(0x00, HEX);
          break;
        //Check for 'A' being sent
        //This is meant to be used when more than nine treats are expected to be dispensed
        //Does not convert ASCII character to decimal
        case 65:
          if (dispenseCommand(command[2], globalMotorSpeed, false, false))
          {
            Serial.print(0x00, HEX);
          }
          else
          {
            Serial.print(0x01, HEX);
          }
          break;
        //Check for 'M' being sent
        //This allows the changing of the global motor speed
        //Not recommended to be used
        case 77:
          globalMotorSpeed = command[2];
          Serial.print(0x00, HEX);
          break;
        //Command not recognized
        default:
          Serial.print(0x01, HEX);
          break;
      }
    }
    else
    {
      Serial.print(0x01, HEX);
    }
  }
}

void testWheel()
{
  int motorSpeed = 0;
  while(motorSpeed < globalMotorSpeed)
  {
    moveMotor(motorSpeed++, true);
    wheelVoltage = getVoltage(WHEEL_SENSOR, 10);
    wheelVoltage = roundFloat(wheelVoltage, 1); 
  
    treatVoltage = getVoltage(TREAT_SENSOR, 10);
    treatVoltage = roundFloat(treatVoltage, 1);
  
    Serial.print("Wheel Voltage: ");
    Serial.print(wheelVoltage);
    Serial.print("V | Treat Voltage: ");
    Serial.print(treatVoltage);
    Serial.print("V");
    Serial.print(" | Speed: ");
    Serial.print(motorSpeed);
    Serial.println();
    delay(200);
  }
  stopMotor();
}

void debugSensors()
{  
  wheelVoltage = getVoltage(WHEEL_SENSOR, 10);
  wheelVoltage = roundFloat(wheelVoltage, 1); 

  treatVoltage = getVoltage(TREAT_SENSOR, 10);
  treatVoltage = roundFloat(treatVoltage, 1); 

  Serial.print("Wheel Voltage: ");
  Serial.print(wheelVoltage);
  Serial.print("V | Treat Voltage: ");
  Serial.print(treatVoltage);
  Serial.print("V");
  Serial.println();
}

bool dispenseCommand(int cycles, int motorSpeed, bool motorDir, bool isASCII)
{
  sampleVoltage = getVoltage(TREAT_SENSOR, 10);
  sampleVoltage = roundFloat(sampleVoltage, 1);
  
  int treatSamples = cycles;
  if (isASCII) { treatSamples = cycles - 0x30; }
  int wheelSamples = treatSamples * 3;
  moveMotor(motorSpeed, motorDir);

  while (treatSamples > 0)
  {
    treatVoltage = getVoltage(TREAT_SENSOR, 10);
    treatVoltage = roundFloat(treatVoltage, 1);
    
    if (treatVoltage < sampleVoltage)
    {
      treatSamples--;
      while (treatVoltage < sampleVoltage)
      {
        treatVoltage = getVoltage(TREAT_SENSOR, 10);
        treatVoltage = roundFloat(treatVoltage, 1);
      }
    }
  }
  stopMotor();
  return true;
}

//Source: https://stackoverflow.com/questions/1343890/how-do-i-restrict-a-float-value-to-only-two-places-after-the-decimal-point-in-c
float roundFloat(float raw, int precision)
{
  return floorf(raw * (10 * precision)) / 10;
}
//Source: https://create.arduino.cc/projecthub/next-tech-lab/voltmeter-using-arduino-00e7d1
float getVoltage(int pin, int samples)
{
  int val = getAverageReading(pin, samples);
  Vout = (val * VOLTAGE_SCALE) / ADC_PRECISION; // formula for calculating voltage out i.e. V+, here 5.00
  Vin = Vout / (R2/(R1+R2)); // formula for calculating voltage in i.e. GND
  if (Vin < LOGIC_LOW)//condition 
  {
   Vin=0.00;
  } 
  return Vin;
}

int getAverageReading(int pin, int numReadings)
{
  int adcReading = 0;
  for (int i = 0; i < numReadings; i++)
  {
    adcReading += analogRead(pin);
  }
  adcReading /= numReadings;
  return adcReading;
}

void moveMotor(int motorSpeed, bool motorDir)
{
  //Set motor speed before driving motor
  analogWrite(MSPEED, motorSpeed);
  //If true, then drive it clockwise
  if (motorDir)
  {
    digitalWrite(MDRIVERA, HIGH);
    digitalWrite(MDRIVERB, LOW);
  }
  //If false, then drive it counter-clockwise
  else
  {
    digitalWrite(MDRIVERA, LOW);
    digitalWrite(MDRIVERB, HIGH);
  }
}

void stopMotor()
{
  analogWrite(MSPEED, 0);
  digitalWrite(MDRIVERA, LOW);
  digitalWrite(MDRIVERB, LOW);
}

void initPins()
{
  //Initialize inputs
  pinMode(WHEEL_SENSOR, INPUT);
  pinMode(TREAT_SENSOR, INPUT);
  pinMode(CLICK, INPUT);

  //Initialize outputs
  pinMode(MDRIVERA, OUTPUT);
  pinMode(MDRIVERB, OUTPUT);
  pinMode(MSPEED, OUTPUT);
}
