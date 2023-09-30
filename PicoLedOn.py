import machine

class PicoLedOn:

    led_pico = machine.Pin(25, machine.Pin.OUT)

    def __init__(self) -> None:
        self.led_pico.value(0)
        
    def ledOn(self):
        self.led_pico.value(1)
        print("LED AN")
    
    def ledOff(self):
        self.led_pico.value(0)
        print("LED AUS")