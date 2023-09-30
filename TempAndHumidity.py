import machine
from machine import I2C, Pin                                       #include hardware device
import time
from time import sleep_ms, ticks_ms                                #include delay time
from Lcd1602_i2c import I2cLcd                                     #define LCD1602 Function device
from Dht11 import DHT11 
import json

class TempAndHumidity:

    #The PCF8574 has a jumper selectable address: 0x20 - 0x27 
    DEFAULT_I2C_ADDR = 0x27#0X27#                                  #define I2C Address
    dht = DHT11(15)                                                #define DHT11 pin function:GP15
    i2c = I2C(0,scl=Pin(5), sda=Pin(4), freq=100000)               #define LCD I/O PIN and Freq.
    lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)                     #define I2C defult address.

    def __init__(self) -> None:
        pass
                                
    def readTaHData(self):
        DATA = self.dht.read_data()    
        t = DATA[0]                                                    #read Temp.& Humidity
        h = DATA[1]                                                    
        return [str(t),str(h)]                                         

    def getTempAndHumidity(self, httpResJson):
        dat = self.readTaHData() 
        sleep_ms(1000)                                             #delay time 1000ms 
        self.lcd.clear()
        self.lcd.putstr(str(httpResJson["name"]) + ": Temp: " + str(dat[0]) + "c | Luftf.: " + str(dat[1]) + "%")
        # self.lcd.move_to(9, 0)
        # self.lcd.putstr("Temp.:" + str(dat[0]))
        # self.lcd.putstr("c")
        # self.lcd.move_to(0, 1)
        # self.lcd.putstr("Luftf.: " + str(dat[1]) + "%")
        # # self.lcd.move_to(9, 1)
        # # self.lcd.putstr(str(dat[0]))
        # # self.lcd.putstr("%")
        time.sleep(5)
        return [str(dat[0]),str(dat[1])] 