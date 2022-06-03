import machine
from time import sleep
from machine import Timer, Pin
import neopixel

class LED():
    def __init__(self, pin, n, count_max = 3000):
        self.np = neopixel.NeoPixel(Pin(pin), n)
        self.n = n
        self.lux = 15000
        self.count_max = count_max
        self.count = 0

    def set_color(self, r, g, b):
        for i in range(self.n):
            self.np[i] = (r, g, b)
        self.np.write()

    def update_lux(self, lux):
        self.lux = lux
        

    def start(self):
        try:
            def led_on(duty):
                if self.count < duty*self.count_max:
                    self.set_color(170, 0, 255)
                else:
                    self.set_color(0, 0, 0)
                self.count += 1
                if self.count >= self.count_max:
                    self.count = 0

            def led_start(lux):
                full_sun = 45000
                part_sun = 20000
                shade = 10000
                low = 5000
                dark = 500

                if lux > full_sun:
                    led_on(0)
                elif lux > part_sun:
                    led_on(0.2)
                elif lux > shade:
                    led_on(0.4)
                elif lux > low:
                    led_on(0.6)
                elif lux > dark:
                    led_on(0.8)
                elif lux < dark:
                    led_on(1)

            def led_cb(t):
                led_start(self.lux)

            tim = Timer(0)
            tim.init(period = 1, mode = Timer.PERIODIC, callback = led_cb)

            sleep(0.01)
        
        except KeyboardInterrupt:
            tim.deinit()
            sleep(0.1)
            print ("[Interrupted]")