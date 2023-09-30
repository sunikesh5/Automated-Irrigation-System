from time import sleep_ms, sleep_us
from machine import I2C, Pin
from Lcd1602_i2c import I2cLcd

class RemoteControl:

    IR_INT = Pin(17, Pin.IN, Pin.PULL_UP)             #INPUT pin

    # The PCF8574 has a jumper selectable address: 0x20 - 0x27
    DEFAULT_I2C_ADDR = 0x27

    i2c = I2C(0,scl=Pin(5), sda=Pin(4), freq=100000)
    lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)    
    dat = 0
    code_dis_flag = 0

    def read_Data(self, arg):
        if self.IR_INT.value() == 1:
            print('IRf')
        else:
            cnt = 0
            while self.IR_INT.value()==0 and cnt < 400:
                sleep_us(7)
                cnt +=1
                continue
            if cnt >= 400 or cnt < 230:
                print('SHf')
        
            else:
                if self.IR_INT.value()==1:
                    cnt = 0
                    while self.IR_INT.value()==1 and cnt < 215:
                        sleep_us(7)
                        cnt +=1
                        continue
                    if cnt >= 215 or cnt < 100:
                        print('SLf')
                
                    else:
                        data=[]
                        j=0
                        while j<32:
                            cnt = 0    
                            while self.IR_INT.value()==0 and cnt < 30:
                                sleep_us(7)
                                cnt +=1
                                continue
                            if cnt >= 30 or cnt < 10:
                                print('CL_bit',j)
                            else:
                                cnt = 0 
                                while self.IR_INT.value()==1 and cnt < 70:
                                    sleep_us(7)
                                    cnt +=1
                                    continue
                                if cnt >= 70 or cnt < 10:
                                    print('CH_bit',j)
                                else:
                                    if cnt > 35:
                                        data.append(1)
                                    else:
                                        data.append(0)
                            j+=1            
                        
                        code3 = data[16:24]
                        code4 = data[24:32]
                        code3_buf = 0
                        code4_buf = 0
                        for i in range(8):
                            code3_buf+=code3[i]*2**(7-i)
                            code4_buf+=code4[i]*2**(7-i)
                        if code3_buf+code4_buf == 255:
                            self.dat = code3_buf
                            print('IR code:',self.dat)                       
                            self.code_dis_flag = 1

    def statusRemoteControl(self):
        self.IR_INT.irq(handler=self.read_Data, trigger=Pin.IRQ_FALLING)                     #IO Interrupts
        while True:
            if self.code_dis_flag:
                self.code_dis_flag = 0
                self.lcd.clear()
                self.lcd.move_to(5, 0)
                self.lcd.putstr("IR code:")
                
                if self.dat == 162:            
                    self.lcd.move_to(6, 1)       
                    self.lcd.putstr("1")
            
                elif self.dat == 98:            
                    self.lcd.move_to(6, 1)       
                    self.lcd.putstr("2")
                
                elif self.dat == 226:
                    self.lcd.move_to(6, 1)       
                    self.lcd.putstr("3")
                
                elif self.dat == 34:
                    self.lcd.move_to(6, 1)       
                    self.lcd.putstr("4")    
                
                elif self.dat == 2:             
                    self.lcd.move_to(6, 1)       
                    self.lcd.putstr("5")    
                
                elif self.dat == 194:             
                    self.lcd.move_to(6, 1)       
                    self.lcd.putstr("6")    
                
                elif self.dat == 224:             
                    self.lcd.move_to(6, 1)       
                    self.lcd.putstr("7")
                
                elif self.dat == 168:             
                    self.lcd.move_to(6, 1)       
                    self.lcd.putstr("8")    
                
                elif self.dat == 144:             
                    self.lcd.move_to(6, 1)       
                    self.lcd.putstr("9")   
                
                elif self.dat == 152:             
                    self.lcd.move_to(6, 1)       
                    self.lcd.putstr("0")
                
                elif self.dat == 104:             
                    self.lcd.move_to(6, 1)       
                    self.lcd.putstr("*")
                
                elif self.dat == 176:             
                    self.lcd.move_to(6, 1)       
                    self.lcd.putstr("#")    
                
                elif self.dat == 24:             
                    self.lcd.move_to(6, 1)       
                    self.lcd.putstr("up")
                
                elif self.dat == 74:             
                    self.lcd.move_to(6, 1)       
                    self.lcd.putstr("down")
                
                elif self.dat == 16:
                    self.lcd.move_to(6, 1)       
                    self.lcd.putstr("left")    
                
                elif self.dat == 90:
                    self.lcd.move_to(6, 1)       
                    self.lcd.putstr("right")    
            
                elif self.dat == 56:            
                    self.lcd.move_to(6, 1)       
                    self.lcd.putstr("OK")

    def getRemoteButton(self):
        self.IR_INT.irq(handler=self.read_Data, trigger=Pin.IRQ_FALLING)                     #IO Interrupts
        while True:
            if self.code_dis_flag:
                self.code_dis_flag = 0
                if self.dat == 162:            
                    return "1"
            
                elif self.dat == 98:            
                    return "2"
                
                elif self.dat == 226:
                    return "3"
                
                elif self.dat == 34:
                    return "4"    
                
                elif self.dat == 2:             
                    return "5"   
                
                elif self.dat == 194:             
                    return "6"   
                
                elif self.dat == 224:             
                    return "7"
                
                elif self.dat == 168:             
                    return "8"  
                
                elif self.dat == 144:             
                    return "9"  
                
                elif self.dat == 152:             
                    return "0"
                
                elif self.dat == 104:             
                    return "*"
                
                elif self.dat == 176:             
                    return "#"
                
                elif self.dat == 24:             
                    return "up"
                
                elif self.dat == 74:             
                    return "down"
                
                elif self.dat == 16:
                    return "left"
                
                elif self.dat == 90:
                    return "right"
            
                elif self.dat == 56:            
                    return "OK"