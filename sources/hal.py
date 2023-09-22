

try:
    from machine import SPI, Pin, I2C, UART
    import os, sdcard
    import st7789 
    from drivers.ds3231 import DS3231
    from drivers.bbq20kbd import BBQ20Kbd
    from drivers.e32900t20d import E32900T20D
    import drivers.hw as hw
    MICROPYTHON = True
except Exception as e:
    print(e)
    import tempfile

    from emulator.context import Context
    from emulator.st7789 import ST7789
    from drivers.ds3231 import DS3231
    from drivers.bbq20kbd import BBQ20Kbd
    MICROPYTHON = False


def setup():
    if MICROPYTHON:
        # SD_MOUNTING_POINT = "/sd"
        # # SPI
        # clk_pin = Pin(hw.CLK, mode=Pin.OUT, value=0)
        # mosi_pin = Pin(hw.MOSI, mode=Pin.OUT, value=0)
        # miso_pin = Pin(hw.MISO, mode=Pin.IN)
        # cs_pin = Pin(hw.LCD_CS, mode=Pin.OUT, value=1)
        # reset_pin = Pin(hw.RST, mode=Pin.OUT, value=1)
        # cmd_data_pin = Pin(hw.D_C, mode=Pin.OUT, value=1)
        # backlight_pin = Pin(hw.BACKLIGHT, mode=Pin.OUT, value=1)
        # sd_cs_mock_pin = Pin(hw.SD_CS2, mode=Pin.IN)

        # spi = SPI(hw.SPI_INDEX,baudrate=hw.SPI_SPEED, sck=clk_pin, mosi=mosi_pin, miso=miso_pin)

        # tft = st7789.ST7789(spi, hw.WIDTH, hw.HEIGHT , dc=cmd_data_pin, reset=reset_pin, cs=cs_pin, backlight=backlight_pin, rotation=hw.ROTATION)
        # tft.init()

        # # I2C
        # scl_pin = Pin(hw.SDL, pull=Pin.PULL_UP)
        # sda_pin = Pin(hw.SDA, pull=Pin.PULL_UP)

        # i2c = I2C(hw.I2C_INDEX, scl=scl_pin, sda=sda_pin, freq=hw.I2C_SPEED)

        # realtime_clock = DS3231(i2c)

        # keyboard = BBQ20Kbd(i2c)
        # keyboard.configuration(use_mods=True, report_mods=True)

        # sd=sdcard.SDCard(spi, Pin(hw.SD_CS))
        # os.mount(sd,SD_MOUNTING_POINT)

        # LORA and UART
        #M0 = 6
        #M1 = 7
        #RX0 = 8
        #TX0 = 9
        #AUX = 10

        m0_pin = Pin(hw.M0, mode=Pin.OUT, value=0)
        m1_pin = Pin(hw.M1, mode=Pin.OUT, value=0)
        tx_pin = Pin(hw.TX0, mode=Pin.OUT, value=1)
        rx_pin = Pin(hw.RX0, mode=Pin.IN)
        aux_pin = Pin(hw.AUX, mode=Pin.IN)

        uart = UART(1, hw.UART_BAUDRATE)
        uart.init(hw.UART_BAUDRATE, bits=hw.UART_BITS, parity=hw.UART_PARITY, stop=hw.UART_STOP, rx=rx_pin, tx=tx_pin, rxbuf=512, timeout=20, timeout_char=5)

        lora = E32900T20D(m0_pin, m1_pin, uart, aux_pin)


        return None, None, None, None, lora
        #return tft, realtime_clock, keyboard, SD_MOUNTING_POINT, lora
    else:
        ctx = Context()
        tft = ST7789(ctx)
        tft.init()
        keyboard = BBQ20Kbd()
        realtime_clock = DS3231()

        sd_mounting_point = tempfile.TemporaryDirectory()

        return tft, realtime_clock, keyboard, sd_mounting_point, None