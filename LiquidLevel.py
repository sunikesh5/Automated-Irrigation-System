import machine
from machine import I2C, Pin, ADC                                        #include hardware device
import time
from Lcd1602_i2c import I2cLcd   
import json

class LiquidLevel:

    #The PCF8574 has a jumper selectable address: 0x20 - 0x27
    DEFAULT_I2C_ADDR = 0x27#0X27#                                       #define I2C Address
    i2c = I2C(0,scl=Pin(5), sda=Pin(4), freq=100000)                    #define LCD I/O PIN and Freq.
    lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)                          #define I2C defult address.
    
    adc = ADC(26)                                                       # create an ADC object acting on a pin
    
    def __init__(self) -> None:
        pass

    def getLiquidLevel(self, httpResJson):
        sensorDataRaw = int(self.adc.read_u16())
        sensorDataPercent = round((sensorDataRaw/65535)*100)
        print("Wasserstand im Tank Raw value: " + str(sensorDataRaw))
        print("Wasserstand im Tank Percent: " + str(sensorDataPercent) +" %")
        self.lcd.clear()
        self.lcd.putstr(str(httpResJson["name"]) + ": Wasserstand Tank " + str(sensorDataPercent) + " %")
        time.sleep(5)
        return str(sensorDataPercent)