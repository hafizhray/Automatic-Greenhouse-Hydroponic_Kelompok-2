from machine import ADC, Pin
import time


class LDR:
    """This class read a value from a light dependent resistor (LDR)"""

    def __init__(self, pin):
        """
        Initializes a new instance.
        :parameter pin A pin that's connected to an LDR.
        :parameter min_value A min value that can be returned by value() method.
        :parameter max_value A max value that can be returned by value() method.
        """

        # initialize ADC (analog to digital conversion)
        self.adc = ADC(Pin(pin))

        # set 11dB input attenuation (voltage range roughly 0.0v - 3.6v)
        self.adc.atten(ADC.ATTN_11DB)

    def read(self):
        """
        Read a raw value from the LDR.
        :return A value from 0 to 4095.
        """
        return self.adc.read()

    def resistance(self, a = 1):
        adc_val = self.read()
        if adc_val < 1:
            adc_val == 1
        return adc_val*a*10000/(4095.01 - adc_val*a)

    def lux(self, a = 1):
        try:
            lux = int(round(1.25*10000000*(self.resistance(a)**(-1.4059)), 0))
            if lux > 999999:
                lux = 999999
        except:
            lux = 999999
        return lux
    