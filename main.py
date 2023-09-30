import machine
import utime
from time import sleep_ms, ticks_ms                                #include delay time
from machine import I2C, Pin                                       #include hardware device
from Lcd1602_i2c import I2cLcd                                     #define LCD1602 Function device
from Dht11 import DHT11                                            #define DHT11 Function device
from CurrentDateTime import CurrentDateTime
from TempAndHumidity import TempAndHumidity
from PicoLedOn import PicoLedOn
from LiquidLevel import *
from WiFi import *
from RemoteControl import *
import json
from Soilmoisture import *
from Light import *
from Pump import *

class Main:

    #Variablen initiieren
    picoLed = PicoLedOn()                                             
    tempHumidity = TempAndHumidity()
    liquidLevel = LiquidLevel()      
    wifi = WiFi() 
    httpResJson = json
    soilmoisture = Soilmoisture()
    light = Light()
    pump = Pump()
    
    def __init__(self) -> None:
        self.picoLed.ledOn()
        #######################
        ####### WiFi ##########
        #######################
        self.wifi.chooseWifi()
        self.wifi.passwordWifi()
        self.wifi.connectToWifi()
        self.httpResJson = self.wifi.connectToGardenly()
        while True:
            if int(self.httpResJson["id"]) >= 1:
                break
            else:
                self.httpResJson = self.wifi.connectToGardenly()

        #######################
        ##### main loop #######
        #######################
        i = 0
        while True:                                                    #infinity loop
            i += 1
            print("\r\n\r\n------------- Durchgang " + str(i) + "-------------")
            sleep_ms(int(self.httpResJson["transferIntervall"]) * 1000) #Automationseinstellung
            tempHumList = self.tempHumidity.getTempAndHumidity(self.httpResJson)
            self.httpResJson = self.wifi.httpRequest(self.soilmoisture.getSoilmoisture(self.httpResJson), 
                                                     tempHumList[0], 
                                                     tempHumList[1], 
                                                     self.liquidLevel.getLiquidLevel(self.httpResJson), 
                                                     self.light.getLight(self.httpResJson))
            print("Check WaterNow")
            if self.httpResJson["waterNow"] == True:
                self.pump.pumpOn()
                sleep_ms(2000)
                self.pump.pumpOff()
                self.wifi.waterNowFalse(self.httpResJson)

Main()