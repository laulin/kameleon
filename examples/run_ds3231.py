from machine import Pin, I2C
import hw
import utime

from ds3231 import DS3231

# This example show how to get time from RTC

i2c = I2C(0, scl=Pin(hw.SDL, pull=Pin.PULL_UP), sda=Pin(hw.SDA, pull=Pin.PULL_UP), freq=400000)

ds = DS3231(i2c)

while True:
    print(ds.getDateTime())
    utime.sleep(1)
    