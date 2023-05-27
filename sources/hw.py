SDA = 0
SDL = 1 
CLK = 2
MOSI = 3
MISO = 4
LCD_CS = 5
M0 = 6
M1 = 7
RX0 = 8
TX0 = 9
AUX = 10
KB_INT = 11
RST = 12
SD_CS = 13
D_C = 14
BACKLIGHT = 16
SD_CS2 = 17

LCD_SPI = 0
LCD_SPEED = 80000000

# The values' order is important, otherwis the TFT drivers will not rotate the display
WIDTH = 240
HEIGHT = 320
# ROTATION = 1 # should be this value but need board fix
ROTATION = 3