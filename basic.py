

import RPi.GPIO as gpio

gpio.setmode(gpio.BCM)

gpio.setup(26, gpio.OUT)

class lol:
    def __init__(self, lit):
        self.lit = lit
    def __repr__(self):
        gpio.output(26, self.lit)
        return str(self.lit)

yes = lol(True)
no = lol(False)

