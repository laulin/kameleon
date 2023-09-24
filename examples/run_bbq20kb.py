from machine import Pin, I2C
import time
import hw

from bbq20kbd import BBQ20Kbd

# Show how to use the keyboard

i2c = I2C(0, scl=Pin(hw.SDL, pull=Pin.PULL_UP), sda=Pin(hw.SDA, pull=Pin.PULL_UP), freq=400000)
kb = BBQ20Kbd(i2c)
kb.configuration(use_mods=True, report_mods=True)
print(f"Kb {kb} initiated with {i2c}")
print(f"version : {kb.version}")

loop = True
backlight_delta = 1
backlight_value = 0
while loop:
    events = kb.keys

    if len(events):
        print(events)
        if (2, " ") in  events:
            loop = False

    x, y = kb.trackpad

    if x !=0 or y !=0 :
        print(f"T({x},{y})")

    backlight_value += backlight_delta

    if backlight_value >= 255 :
        backlight_delta = -1
    if backlight_value <= 0:
        backlight_delta = 1

    kb.backlight = backlight_value

    time.sleep(0.05)