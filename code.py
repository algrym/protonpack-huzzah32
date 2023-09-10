# SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""CircuitPython Essentials Internal RGB LED red, green, blue example"""
import time
import board
import neopixel
import version
import adafruit_fancyled.adafruit_fancyled as fancyled

led = neopixel.NeoPixel(board.NEOPIXEL, 1)

led.brightness = 0.3

print("github.com/algrym/protonpack-huzzah32/code.py -", version.__version__)
print(f" - Adafruit FancyLed v{fancyled.__version__}")

while True:
    print("Hello World!")
    led[0] = (255, 0, 0)
    time.sleep(0.5)
    led[0] = (0, 255, 0)
    time.sleep(0.5)
    led[0] = (0, 0, 255)
    time.sleep(0.5)
