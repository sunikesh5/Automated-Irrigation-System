import machine
import utime

class InternalTemp:

    sensor_temp = machine.ADC(4)
    conversion_factor = 3.3 / (65535)

    def __init__(self) -> None:
        pass

    def getInternalSensorTemp(self):
        reading = self.sensor_temp.read_u16() * self.conversion_factor
        temperature = 27 - (reading - 0.706)/0.001721
        print("Interner Temperaturmesser: " + temperature)
        return temperature