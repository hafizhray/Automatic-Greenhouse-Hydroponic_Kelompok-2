import machine
from machine import Pin, ADC
from time import sleep_ms, sleep
from mov_avg import Mov_Avg

class Water_Sens():
    def __init__(self, adc, pwr, min = 300, max = 1410):
        self.adc = ADC(Pin(adc), atten = ADC.ATTN_11DB)
        self.pwr = Pin(pwr, Pin.OUT)
        self.min = min
        self.max = max
        self.range = max - min

    def raw(self):
        self.pwr.on()
        sleep_ms(10)
        water_val = self.adc.read()
        self.pwr.off()
        return water_val
    
    def read(self):
        # water_val = (self.raw() - self.min) * 1410 / self.range + 300
        water_val = self.raw()
        # water_lvl = 9/100000*water_val**2 - 0.0702*water_val + 13.325
        water_lvl = 44.944/1000**2*water_val**2 - 9.8087/1000*water_val + 0.6794
        if water_lvl < 100:
            return water_lvl
        elif water_lvl < 0.02:
            return 0.00
        else:
            return 100.00
    

