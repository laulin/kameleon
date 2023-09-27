import utime
import sources.font_8x16 as font
import time
import hal
import os

tft, rtc, keyboard, sd = hal.setup()

tft.fill(0)


def test_sleep():
    tft.text(font, b'Go to sleep', 0, 0)
    utime.sleep(1)
    tft.off()
    tft.sleep_mode(1)
    utime.sleep(1)
    tft.sleep_mode(0)
    tft.on()
    tft.text(font, b'wake up !', 0, 0)

def test_time():
    last_event = time.ticks_ms()
    is_sleeping = False
    keyboard.backlight = 150
    while True:
        if time.ticks_ms() < last_event + 3000:
            if is_sleeping:
                tft.sleep_mode(0)
                tft.on()
                is_sleeping = False
                keyboard.backlight = 150
            date = f"{rtc.getDateTime()}"
            date_byte = bytes(date, "utf8")
            tft.text(font, date_byte, 0, 0)
        else:
            if not is_sleeping:
                tft.off()
                tft.sleep_mode(1)
                is_sleeping = True
                keyboard.backlight = 0

        events = keyboard.keys
        x, y = keyboard.trackpad

        if len(events) > 0 or x != 0 or y != 0:
            last_event = time.ticks_ms()

def test_sd():
    print("Start of sd test")
    print(os.listdir('/sd'))

    with open("/sd/test.txt", "w") as f:
        f.write("hello world")

    print(os.listdir('/sd'))

    with open("/sd/test.txt", "r") as f:
        print("written : ", f.read())

    print("End of sd test")

test_sd()
#test_time()