SDA = 0
SDL = 1 
CLK = 2
MOSI = 3
MISO = 4
LCD_CS = 5
M0 = 6
M1 = 7
RX0 = 9
TX0 = 8
AUX = 10
KB_INT = 11
RST = 12
SD_CS = 13
D_C = 14
BACKLIGHT = 16
SD_CS2 = 17

SPI_INDEX = 0
SPI_SPEED = 40000000
I2C_INDEX = 0
I2C_SPEED = 400000

UART_BAUDRATE = 9600
UART_BITS = 8
UART_PARITY = None
UART_STOP = 1

# The values' order is important, otherwis the TFT drivers will not rotate the display
WIDTH = 240
HEIGHT = 320
# ROTATION = 1 # should be this value but need board fix
ROTATION = 3