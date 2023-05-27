from machine import SPI, Pin, I2C
import st7789 
import utime
import hw
from ds3231 import DS3231
from bbq20kbd import BBQ20Kbd
import vga2_8x16 as font
import time


clk = Pin(hw.CLK, mode=Pin.OUT, value=0)
mosi = Pin(hw.MOSI, mode=Pin.OUT, value=0)
miso = Pin(hw.MISO, mode=Pin.IN)
cs = Pin(hw.LCD_CS, mode=Pin.OUT, value=1)
reset = Pin(hw.RST, mode=Pin.OUT, value=1)
cmd_data = Pin(hw.D_C, mode=Pin.OUT, value=1)
backlight = Pin(hw.BACKLIGHT, mode=Pin.OUT, value=1)
sd_cs_mock = Pin(hw.SD_CS2, mode=Pin.IN)



spi = SPI(hw.LCD_SPI,baudrate=hw.LCD_SPEED, sck=clk, mosi=mosi, miso=miso)

tft = st7789.ST7789(spi, hw.WIDTH, hw.HEIGHT , dc=cmd_data, reset=reset, cs=cs, backlight=backlight, rotation=hw.ROTATION)

tft.init()

i2c = I2C(0, scl=Pin(hw.SDL, pull=Pin.PULL_UP), sda=Pin(hw.SDA, pull=Pin.PULL_UP), freq=400000)

ds = DS3231(i2c)

kb = BBQ20Kbd(i2c)
kb.configuration(use_mods=True, report_mods=True)

tft.fill(0)


def test_sleep():
    tft.text(font, b'Go to sleep', 0, 0, st7789.color565(0,0,0), st7789.color565(255,255,255))
    utime.sleep(1)
    tft.off()
    tft.sleep_mode(1)
    utime.sleep(1)
    tft.sleep_mode(0)
    tft.on()
    tft.text(font, b'wake up !', 0, 0, st7789.color565(0,0,0), st7789.color565(255,255,255))

def test_time():
    last_event = time.ticks_ms()
    is_sleeping = False
    kb.backlight = 150
    while True:
        if time.ticks_ms() < last_event + 3000:
            if is_sleeping:
                tft.sleep_mode(0)
                tft.on()
                is_sleeping = False
                kb.backlight = 150
            date = f"{ds.getDateTime()}"
            date_byte = bytes(date, "utf8")
            tft.text(font, date_byte, 0, 0)
        else:
            if not is_sleeping:
                tft.off()
                tft.sleep_mode(1)
                is_sleeping = True
                kb.backlight = 0

        events = kb.keys
        x, y = kb.trackpad

        if len(events) > 0 or x != 0 or y != 0:
            last_event = time.ticks_ms()



test_time()