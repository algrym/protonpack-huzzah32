#!/usr/bin/env python3
import atexit
import os
import random
import sys
import time

import adafruit_fancyled.adafruit_fancyled as fancyled
import board
import microcontroller
import neopixel
import supervisor

import version

# Software version
protonpack_version: str = version.__version__

# Update this to match the number of NeoPixel LEDs connected to your boards
neopixel_stick_num_pixels: int = 20
neopixel_ring_num_pixels: int = 60

# Which pins are the stick and ring connected to?
# (These should be different, but you do you.)
neopixel_stick_pin = board.A0
neopixel_ring_pin = board.A1

# Pixel brightness
neopixel_stick_brightness: float = 0.3  # 0.008 is the dimmest I can make the stick
neopixel_ring_brightness: float = 0.5  # 0.008 is the dimmest I can make them
brightness_levels = (0.25, 0.3, 0.15)  # balance the colors better so white doesn't appear blue-tinged

# How fast should the neopixel cycle?
# This is (similar to) microseconds per increment so: Higher is slower
neopixel_stick_speed: int = 20
neopixel_ring_speed_current: int = 80  # Start this high to emulate spin-up
neopixel_ring_speed_cruise: int = 10
change_speed: int = 30  # How often should we change speed?

# how many LEDs should the ring light at one time?
ring_cursor_width: int = 3

#
###################################################################
# No config beyond this point
###################################################################
#

# Print startup info
print(f"-=< protonpack v{protonpack_version} - https://github.com/algrym/protonpack-huzzah32/ >=-")
print(f" - uname: {os.uname()}")
print(f" - cpu uid: {microcontroller.cpu.uid}")
print(f" -- freq: {microcontroller.cpu.frequency / 1e6} MHz")
print(f" -- reset reason: {microcontroller.cpu.reset_reason}")
print(f" -- nvm: {len(microcontroller.nvm)} bytes")
print(f" - python v{sys.version}")
print(f" - Adafruit fancyled v{fancyled.__version__}")
print(f" - neopixel v{neopixel.__version__}")

# Color constants
RED = fancyled.gamma_adjust(fancyled.CRGB(255, 0, 0), brightness=brightness_levels).pack()
ORANGE = fancyled.gamma_adjust(fancyled.CRGB(255, 165, 0), brightness=brightness_levels).pack()
YELLOW = fancyled.gamma_adjust(fancyled.CRGB(255, 255, 0), brightness=brightness_levels).pack()
GREEN = fancyled.gamma_adjust(fancyled.CRGB(0, 255, 0), brightness=brightness_levels).pack()
BLUE = fancyled.gamma_adjust(fancyled.CRGB(0, 0, 255), brightness=brightness_levels).pack()
PURPLE = fancyled.gamma_adjust(fancyled.CRGB(128, 0, 128), brightness=brightness_levels).pack()
WHITE = fancyled.gamma_adjust(fancyled.CRGB(255, 255, 255), brightness=brightness_levels).pack()
OFF = (0, 0, 0)

ring_on_color = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, WHITE]

# initialize neopixels
print(f" -- stick size {neopixel_stick_num_pixels} on {neopixel_stick_pin}")
stick_pixels = neopixel.NeoPixel(neopixel_stick_pin,
                                 neopixel_stick_num_pixels,
                                 brightness=neopixel_stick_brightness)
print(f" -- ring  size {neopixel_ring_num_pixels} on {neopixel_ring_pin}")
ring_pixels = neopixel.NeoPixel(neopixel_ring_pin,
                                neopixel_ring_num_pixels,
                                brightness=neopixel_ring_brightness)

def all_off():
    # callback to turn everything off and restart
    print('Exiting: all pixels off.')
    stick_pixels.fill(OFF)
    ring_pixels.fill(OFF)
    supervisor.reload()


# turn everything off on exit
atexit.register(all_off)

# set up main driver loop
ring_cursor_on = ring_cursor_off = ring_color_index = 0
stick_cursor = stick_max_previous = stick_max = 0
stick_pixel_max = 1
stick_clock_next = ring_clock_next = adjust_clock_next = 0

# main driver loop
print(' - Entering main event loop.')
while True:
    clock = supervisor.ticks_ms()

    # increment speeds
    if clock > adjust_clock_next:
        # calculate time of next speed update
        adjust_clock_next = clock + change_speed

        # adjust stick max if it's too low
        if stick_pixel_max < len(stick_pixels):
            stick_pixel_max += 1

        # adjust ring speed if it's too low
        if neopixel_ring_speed_current > neopixel_ring_speed_cruise:
            neopixel_ring_speed_current -= 1
            ring_pixels[ring_cursor_off] = WHITE  # spark when we change speed

        # Trigger active: decrement the power meter!
        if (clock % 150) == 0:
            if stick_cursor > 0:
                stick_pixels[stick_cursor] = OFF
                stick_pixels[stick_max_previous] = GREEN
                stick_cursor -= 1
        continue  # Skip the ring and stick updates if the trigger is down

    # increment the power cell
    if clock > stick_clock_next:
        # calculate time of next stick update
        stick_clock_next = clock + neopixel_stick_speed

        # reset if the cursor is over the max
        if stick_cursor > stick_max:
            ring_pixels[ring_cursor_off] = WHITE  # spark when we hit max
            stick_max_previous = stick_max
            stick_max = random.randrange(0, stick_pixel_max - 1)
            stick_cursor = 0
            stick_pixels.fill(OFF)

        # turn on the appropriate pixels
        stick_pixels[stick_cursor] = BLUE
        stick_pixels[stick_max_previous] = GREEN
        stick_cursor += 1

    # increment the ring
    if clock > ring_clock_next:
        # Calculate time of next ring update
        ring_clock_next = clock + neopixel_ring_speed_current

        # turn on the appropriate pixels
        ring_pixels[ring_cursor_on] = ring_on_color[ring_color_index]
        ring_pixels[ring_cursor_off] = OFF

        # increment cursors
        ring_cursor_off = (ring_cursor_on - ring_cursor_width) % len(ring_pixels)
        ring_cursor_on = (ring_cursor_on + 1) % len(ring_pixels)

    time.sleep(0.001)
