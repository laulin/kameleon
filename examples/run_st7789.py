from machine import SPI, Pin
import st7789 
import utime
import hw

# This example show how to setup the TFT and fill it with color


clk = Pin(hw.CLK, mode=Pin.OUT, value=0)
mosi = Pin(hw.MOSI, mode=Pin.OUT, value=0)
miso = Pin(hw.MISO, mode=Pin.IN)
cs = Pin(hw.LCD_CS, mode=Pin.OUT, value=1)
reset = Pin(hw.RST, mode=Pin.OUT, value=1)
cmd_data = Pin(hw.D_C, mode=Pin.OUT, value=1)
backlight = Pin(hw.BACKLIGHT, mode=Pin.OUT, value=1)
sd_cs_mock = Pin(hw.SD_CS2, mode=Pin.IN)



spi = SPI(hw.LCD_SPI,baudrate=hw.LCD_SPEED, sck=clk, mosi=mosi, miso=miso)

tft = st7789.ST7789(spi, hw.WIDTH, hw.HEIGHT, dc=cmd_data, reset=reset, cs=cs, backlight=backlight)

tft.init()

while True:
    tft.fill(st7789.RED)
    utime.sleep(1)
    tft.fill(st7789.BLACK)
    utime.sleep(1)