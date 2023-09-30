import machine                                                       #include hardware devices
import utime                                                         #include delay time
from Lcd1602_i2c import I2cLcd                                       #define LCD1602 Function device
from machine import I2C, Pin, Signal                                    #include hardware device
import time

class Pump:

    #The PCF8574 has a jumper selectable address: 0x20 - 0x27 
    DEFAULT_I2C_ADDR = 0x27#0X27#                                  #define I2C Address
    i2c = I2C(0,scl=Pin(5), sda=Pin(4), freq=100000)               #define LCD I/O PIN and Freq.
    lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)                     #define I2C defult address.

    PUMP = Signal(Pin(8, Pin.OUT), invert=True)                    #define pump address

    def __init__(self) -> None:
        self.PUMP.off()

    def pumpOn(self):
        self.PUMP.on()                                              
        print("Pumpe AN")
        
    def pumpOff(self):
        self.PUMP.off()
        print("Pumpe AUS")