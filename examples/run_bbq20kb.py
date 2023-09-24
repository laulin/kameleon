from machine import Pin, I2C
import time
import hal 

tft, _, keyboard, _, lora = hal.setup()

# Show how to use the keyboard

keyboard.configuration(use_mods=True, report_mods=True)
print(f"version : {keyboard.version}")

loop = True
backlight_delta = 1
backlight_value = 0
while loop:
    events = keyboard.keys

    if len(events):
        print(events)
        if (2, " ") in  events:
            loop = False

    x, y = keyboard.trackpad

    if x !=0 or y !=0 :
        print(f"T({x},{y})")

    backlight_value += backlight_delta

    if backlight_value >= 255 :
        backlight_delta = -1
    if backlight_value <= 0:
        backlight_delta = 1

    keyboard.backlight = backlight_value

    time.sleep(0.05)