from machine import UART, Pin, I2C
import time
from esp8266 import ESP8266
import json
from Lcd1602_i2c import I2cLcd
import sys
from RemoteControl import *

class WiFi:
    esp01 = ESP8266()
    esp8266_at_ver = None

    # The PCF8574 has a jumper selectable address: 0x20 - 0x27
    DEFAULT_I2C_ADDR = 0x27

    i2c = I2C(0,scl=Pin(5), sda=Pin(4), freq=100000)
    lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16) 
    remoteControl = RemoteControl() 
    ssid = ""
    wifiPw = ""

    def __init__(self) -> None:
        pass

    def chooseWifi(self):
        print("StartUP",self.esp01.startUP())
        self.lcd.clear()
        self.lcd.putstr("Modul startet...")
        #print("ReStart",esp01.reStart())
        print("StartUP",self.esp01.startUP())
        print("Echo-Off",self.esp01.echoING())
        print("\r\n\r\n")
        '''
        Print ESP8266 AT command version and SDK details
        '''
        esp8266_at_var = self.esp01.getVersion()
        if(esp8266_at_var != None):
            print(esp8266_at_var)
            print("\r\n\r\n")
        '''
        set the current WiFi in SoftAP+STA
        '''
        self.esp01.setCurrentWiFiMode()
        '''
        list all available Wifis
        '''
        apList = self.esp01.getAvailableAPs()
        print("Waehle Wifi. OK zum bestaetigen")
        self.lcd.clear()
        self.lcd.putstr("Waehle Wifi.    Druecke weiter")
        i = 0
        remoteButton = self.remoteControl.getRemoteButton()
        if ((remoteButton == "right") or (remoteButton == "down") or (remoteButton == "OK")):
            while True:
                print(apList[i][1][1:-1])
                self.lcd.clear()
                self.lcd.putstr(apList[i][1][1:-1])
                remoteButton = self.remoteControl.getRemoteButton()
                if ((remoteButton == "right") or (remoteButton == "down")):
                    if i == (len(apList)-1):                            # Dann wäre der User einmal durchgegangen und soll von vorne anfangen
                        i = 0
                        continue
                    i += 1
                    continue
                elif ((remoteButton == "left") or (remoteButton == "up")):
                    if i > 0:
                        i -= 1
                        continue
                    else:
                        continue
                elif remoteButton == "OK":
                        self.ssid = apList[i][1][1:-1]
                        break
        # if ((remoteButton == "right") or (remoteButton == "down")):
        #     for items in apList:
        #         print(items[1][1:-1])
        #         self.lcd.clear()
        #         self.lcd.putstr(items[1][1:-1])
        #         remoteButton = self.remoteControl.getRemoteButton()
        #         if ((remoteButton == "right") or (remoteButton == "down")):
        #             continue
        #         elif remoteButton == "OK":
        #             ssid = items[1][1:-1]
        #             break
        print("Ausgewähltes Wifi: " + self.ssid)
        print("Ende list Wifis")
        '''
        line break
        '''
        print("\r\n\r\n")

    def passwordWifi(self):
        print("Starte Passworteingabe Wifi")
        self.lcd.clear()
        self.lcd.putstr("Passwort: ")
        while True:
            activebutton = self.remoteControl.getRemoteButton()
            if activebutton == "OK":
                break
            elif activebutton == "left":
                self.wifiPw = ""
                self.lcd.clear()
                self.lcd.putstr(self.wifiPw)
            else:
                self.wifiPw = self.wifiPw + activebutton
                self.lcd.clear()
                self.lcd.putstr(self.wifiPw)
        #wifiPw = wifiPw[:-2]                            #WICHTIG, sonst ist der OK Befehl im PW mit drin.
        print("Wifi PW: " + self.wifiPw)
        print("Ende Passworteingabe Wifi")
        '''
        line break
        '''
        print("\r\n\r\n")

    def connectToWifi(self):
        '''
        Connect with the WiFi
        '''
        print("Try to connect with the WiFi..")
        j = 0
        while j <= 3:
            self.lcd.clear()
            self.lcd.putstr("Verbinde mit    Wifi...")
            #if "WIFI CONNECTED" in self.esp01.connectWiFi("Crille","77777777"):
            if "WIFI CONNECTED" in self.esp01.connectWiFi(self.ssid,self.wifiPw):
                print("ESP8266 connect with the WiFi..")
                self.lcd.clear()
                self.lcd.putstr("Wifi verbunden")
                time.sleep(5)
                print("\r\n\r\n")
                break
            else:
                j += 1
                print(str(j) + ". Versuch fehlgeschlagen")
                self.lcd.clear()
                self.lcd.putstr(str(j) + ". Versuch fehlgeschlagen")
                time.sleep(2)
                if j < 3:
                    continue
                print("Verbinden fehlgeschlagen. Falsches Passwort?")
                self.lcd.clear()
                self.lcd.putstr("Passwort falsch.Nochmal?")
                activebutton = self.remoteControl.getRemoteButton()
                if activebutton == "OK":
                    self.passwordWifi()

    def connectToGardenly(self):
        print("Verbinden mit Pflanze.")
        print("Hardware ID: 1")
        print("OK zum verbinden")
        self.lcd.clear()
        self.lcd.putstr("Hardware-ID: 1  OK zum starten")
        remoteButton = self.remoteControl.getRemoteButton()
        if remoteButton == "OK":
            print("Verbinde mit Gardenly...")
            self.lcd.clear()
            self.lcd.putstr("Verbinde mit    Gardenly...")
            httpCode, httpRes = self.esp01.doHttpGet("www.gardenly.garden","/Connect","RaspberryPi-Pico", port=3080)
            print("HTTP Code:",httpCode)
            print("HTTP Response:",httpRes[:-1])
            httpResString = httpRes[:-1]
            httpResJson = json.loads(httpResString)
            if int(httpResJson["id"]) >= 1:
                print(str(httpResJson["name"]) + " verbunden")
                self.lcd.clear()
                self.lcd.putstr(str(httpResJson["name"]) + " verbunden")
                return httpResJson
            else:
                print("Keine Pflanze mit Hardware ID 1 vergeben. OK zum fortfahren")
                self.lcd.clear()
                self.lcd.putstr("Keine Pflanze mit Hardware-ID 1")
                remoteButton = self.remoteControl.getRemoteButton()
                if remoteButton == "OK":
                    return httpResJson

    

    def httpRequest(self,
                    moist="",
                    temp="",
                    hum="",
                    liqLvl="",
                    light=""):
        print("\r\n\r\n")
        print("HTTP Get Operation.......\r\n")
        '''
        Going to do HTTP Get Operation with www.gardenly.garden/Connect, It return the IP address of the connected device
        '''
        # httpCode, httpRes = self.esp01.doHttpGet("http://www.httpbin.org","/ip","RaspberryPi-Pico", port=80)
        httpCode, httpRes = self.esp01.doHttpGet("www.gardenly.garden",
                                                 "/Connect?moist="+moist
                                                 +"&temp="+temp
                                                 +"&hum="+hum
                                                 +"&liqLvl="+liqLvl
                                                 +"&light="+light,
                                                 "RaspberryPi-Pico", 
                                                 port=3080)
        print("------------- www.gardenly.garden/Connect Get Operation Result -----------------------")
        if httpCode == 200:
            print("HTTP Code:",httpCode)
            print("HTTP Response:",httpRes[:-1])
            httpResString = httpRes[:-1]
            httpResJson = json.loads(httpResString)
            print("ID: " + str(httpResJson["id"]))
            self.lcd.clear()
            self.lcd.putstr(str(httpResJson["name"]) + ": Daten gesendet")
        else:
            print("HTTP Code:",httpCode)
            print("HTTP Response:",httpRes)
            print("Fehler bei der WLAN Verbindung")
            self.lcd.clear()
            self.lcd.putstr("Fehler bei Wifi Verbindung")
        print("-----------------------------------------------------------------------------\r\n\r\n")
        time.sleep(2)
        return httpResJson
    
    def waterNowFalse(self, httpResJson):
        httpCode, httpRes = self.esp01.doHttpGet("www.gardenly.garden",
                                                 "/Watering?id="+str(httpResJson["id"])
                                                 +"&water=false",
                                                 "RaspberryPi-Pico", 
                                                 port=3080)
        print("------------- www.gardenly.garden/Watering Get Operation Result -----------------------")
        if httpCode == 200:
            print("HTTP Code:",httpCode)
            print("HTTP Response:",httpRes[:-1])
            httpResString = httpRes[:-1]
            httpResJson = json.loads(httpResString)
            print(str(httpResJson["name"]) + "erfolgreich bewässert")
            self.lcd.clear()
            self.lcd.putstr(str(httpResJson["name"]) + ": Pflanze bewaessert")
        else:
            print("HTTP Code:",httpCode)
            print("HTTP Response:",httpRes)
            print("Fehler bei der WLAN Verbindung")
            self.lcd.clear()
            self.lcd.putstr("Fehler bei Wifi Verbindung")