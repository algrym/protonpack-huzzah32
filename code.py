# SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""CircuitPython Essentials Internal RGB LED red, green, blue example"""
import time

import adafruit_fancyled.adafruit_fancyled as fancyled
import board
import digitalio
import neopixel

import version

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

print("github.com/algrym/protonpack-huzzah32/code.py -", version.__version__)
print(f" - Adafruit FancyLed v{fancyled.__version__}")
print(f" - NeoPixel v{neopixel.__version__}")

while True:
    print("blink blink!")
    led.value = True
    time.sleep(0.1)
    led.value = False
    time.sleep(0.1)
    led.value = True
    time.sleep(0.1)
    led.value = False
    time.sleep(1.0)
