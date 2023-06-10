import pygame
import logging
from typing import List, Tuple


def from_565_to_888(color: int) -> Tuple[int, int, int]:
    r = (color >> 11) & 0x1F
    g = (color >> 5) & 0x3F
    b = color & 0x1F

    r = (r << 3) | (r >> 2)
    g = (g << 2) | (g >> 4)
    b = (b << 3) | (b >> 2)

    return r, g, b

def from_888_to_565(r: int, g: int, b: int) -> int:
    r = r >> 3
    g = g >> 2
    b = b >> 3

    return (r << 11) | (g << 5) | b

BLACK = from_888_to_565(0,0,0)
BLUE  = from_888_to_565(0,0,255)
RED = from_888_to_565(255,0,0)
GREEN = from_888_to_565(0,255,0)
CYAN = from_888_to_565(0,255,255)
MAGENTA = from_888_to_565(255,0,255)
YELLOW = from_888_to_565(255,255,0)
WHITE = from_888_to_565(255,255,255)

class Emulator:
    WIDTH, HEIGHT = 320, 240
    def __init__(self) -> None:
        self._windows = None
        self._log = logging.getLogger("Emulator")

    def width(self)->int:
        return Emulator.WIDTH
    
    def height(self)->int:
        return Emulator.HEIGHT
    
    def hard_reset(self):
        """
        Hard reset display.
        """
        raise NotImplemented()

    def soft_reset(self):
        """
        Soft reset display.
        """
        raise NotImplemented()

    def sleep_mode(self, value: bool):
        """
        Enable or disable display sleep mode.
        Args:
            value (bool): if True enable sleep mode. if False disable sleep mode
        """
        raise NotImplemented()

    def inversion_mode(self, value: bool):
        """
        Enable or disable display inversion mode.
        Args:
            value (bool): if True enable inversion mode. if False disable
            inversion mode
        """
        raise NotImplemented()

    def rotation(self, rotation: int):
        """
        Set display rotation.
        Args:
            rotation (int):
                - 0-Portrait
                - 1-Landscape
                - 2-Inverted Portrait
                - 3-Inverted Landscape
        """
        raise NotImplemented()

    def vline(self, x: int, y: int, length: int, color: int):
        """
        Draw vertical line at the given location and color.
        Args:
            x (int): x coordinate
            y (int): y coordinate
            length (int): length of line
            color (int): 565 encoded color
        """
        self.line(x,y,x, y+length, color)

    def hline(self, x: int, y: int, length: int, color: int):
        """
        Draw horizontal line at the given location and color.
        Args:
            x (int): x coordinate
            y (int): y coordinate
            length (int): length of line
            color (int): 565 encoded color
        """
        self.line(x,y,x+length, y, color)

    def pixel(self, x: int, y: int, color: int):
        """
        Draw a pixel at the given location and color.
        Args:
            x (int): x coordinate
            y (int): y coordinate
            color (int): 565 encoded color
        """
        color888 = from_565_to_888(color)
        pygame.draw.rect(self._windows, color888, pygame.Rect(x, y, 1, 1))
        pygame.display.flip()

    def blit_buffer(self, buffer: bytes, x: int, y: int, width: int, height: int):
        """
        Copy buffer to display at the given location.
        Args:
            buffer (bytes): Data to copy to display
            x (int): Top left corner x coordinate
            y (int): Top left corner y coordinate
            width (int): Width
            height (int): Height
        """
        raise NotImplemented()

    def rect(self, x: int, y: int, width: int, height: int, color: int):
        """
        Draw a rectangle at the given location, size and color.
        Args:
            x (int): Top left corner x coordinate
            y (int): Top left corner y coordinate
            w (int): Width in pixels
            h (int): Height in pixels
            color (int): 565 encoded color
        """
        color888 = from_565_to_888(color)
        pygame.draw.rect(self._windows, color888, pygame.Rect(x, y, width, height), 1)
        pygame.display.flip()

    def fill_rect(self, x: int, y: int, width: int, height: int, color: int):
        """
        Draw a rectangle at the given location, size and filled with color.
        Args:
            x (int): Top left corner x coordinate
            y (int): Top left corner y coordinate
            width (int): Width in pixels
            height (int): Height in pixels
            color (int): 565 encoded color
        """
        color888 = from_565_to_888(color)
        pygame.draw.rect(self._windows, color888, pygame.Rect(x, y, width, height))
        pygame.display.flip()

    def fill(self, color: int):
        """
        Fill the entire FrameBuffer with the specified color.
        Args:
            color (int): 565 encoded color
        """
        color888 = from_565_to_888(color)
        pygame.draw.rect(self._windows, color888, pygame.Rect(0, 0, Emulator.WIDTH, Emulator.HEIGHT))
        pygame.display.flip()

    def line(self, x0: int, y0: int, x1: int, y1: int, color: int):
        """
        Draw a single pixel wide line starting at x0, y0 and ending at x1, y1.
        Args:
            x0 (int): Start point x coordinate
            y0 (int): Start point y coordinate
            x1 (int): End point x coordinate
            y1 (int): End point y coordinate
            color (int): 565 encoded color
        """
        color888 = from_565_to_888(color)
        pygame.draw.line(self._windows, color888, (x0,y0), (x1,y1), 1)
        pygame.display.flip()

    def vscrdef(self, tfa: int, vsa: int, bfa: int):
        """
        Set Vertical Scrolling Definition.
        To scroll a 135x240 display these values should be 40, 240, 40.
        There are 40 lines above the display that are not shown followed by
        240 lines that are shown followed by 40 more lines that are not shown.
        You could write to these areas off display and scroll them into view by
        changing the TFA, VSA and BFA values.
        Args:
            tfa (int): Top Fixed Area
            vsa (int): Vertical Scrolling Area
            bfa (int): Bottom Fixed Area
        """
        raise NotImplemented()

    def vscsad(self, vssa: int):
        """
        Set Vertical Scroll Start Address of RAM.
        Defines which line in the Frame Memory will be written as the first
        line after the last line of the Top Fixed Area on the display
        Example:
            for line in range(40, 280, 1):
                tft.vscsad(line)
                utime.sleep(0.01)
        Args:
            vssa (int): Vertical Scrolling Start Address
        """
        raise NotImplemented()

    def text(self, font, text: str, x0: int, y0: int, color: int=WHITE, background: int=BLACK):
        """
        Draw text on display in specified font and colors. 8 and 16 bit wide
        fonts are supported.
        Args:
            font (module): font module to use.
            text (str): text to write
            x0 (int): column to start drawing at
            y0 (int): row to start drawing at
            color (int): 565 encoded color to use for characters
            background (int): 565 encoded color to use for background
        """
        byte_text = bytes(text, "ascii")
        background888 = from_565_to_888(background)
        color888 = from_565_to_888(color)

        surface = pygame.Surface((font.WIDTH * len(byte_text), font.HEIGHT))
        surface.fill(background888)

        PITCH = int((font.WIDTH * font.HEIGHT) / 8)
        for index, char in enumerate(byte_text):
            if char >= font.FIRST and char <= font.LAST:
                first_char_index = (char - font.FIRST) * PITCH 
                last_char_index = first_char_index + PITCH
                data = font._FONT[first_char_index:last_char_index]

                for i in range(font.WIDTH * font.HEIGHT):
                    x = i & (font.WIDTH-1)
                    y = int(i/(font.HEIGHT/2))
                    mask = 0x80 >> (i & 7)
                    offset = int(i / 8)
                    print(index, i, x, y, hex(mask), offset)
                    if mask & data[offset]:
                        surface.set_at((x + index*font.WIDTH, y), color888)
            else:
                self._log.error(f"{char} is not printable with the font")

        self._windows.blit(surface, (x0, y0))
        pygame.display.flip()


    def bitmap(self, bitmap, x: int, y: int, index: int=0):
        """
        Draw a bitmap on display at the specified column and row
        Args:
            bitmap (bitmap_module): The module containing the bitmap to draw
            x (int): column to start drawing at
            y (int): row to start drawing at
            index (int): Optional index of bitmap to draw from multiple bitmap
                module
        """
        raise NotImplemented()

    # @micropython.native
    def write(self, font, string: str, x: int, y: int, fg: int=WHITE, bg: int=BLACK,
              background_tuple=None, fill_flag=None):
        """
        Write a string using a converted true-type font on the display starting
        at the specified column and row
        Args:
            font (font): The module containing the converted true-type font
            string (str): The string to write
            x (int): column to start writing
            y (int): row to start writing
            fg (int): foreground color, optional, defaults to WHITE
            bg (int): background color, optional, defaults to BLACK
            background_tuple: Transparency can be emulated by providing a
                background_tuple containing (bitmap_buffer, width, height).
                This is the same format used by the jpg_decode method.
                See examples/T-DISPLAY/clock/clock.py for an example.
            fill_flag:
        """
        raise NotImplemented()

    def write_len(self, font, string: str):
        """
        Returns the width in pixels of the string if it was written with the
        specified font
        Args:
            font (font): The module containing the converted true-type font
            string (string): The string to measure
        """
        raise NotImplemented()

    def madctl(self, value):
        """
        Returns the current value of the MADCTL register. Optionally sets the
        MADCTL register if a value is passed to the method.
        """
        raise NotImplemented()

    def init(self):
        """
        Must be called to initialize the display.
        """
        # Initialise pygame
        pygame.init()

        # Créer la fenêtre
        self._windows = win = pygame.display.set_mode((Emulator.WIDTH, Emulator.HEIGHT))

    def on(self):
        """
        Turn on the backlight pin if one was defined during init.
        """
        raise NotImplemented()

    def off(self):
        """
        Turn off the backlight pin if one was defined during init.
        """
        raise NotImplemented()

    def circle(self, x: int, y: int, r: int, color: int):
        """
        Draws a circle with radius r centered at the (x, y) coordinates in the given color.
        """
        raise NotImplemented()

    def fill_circle(self, x: int, y: int, r: int, color: int):
        """
        Draws a filled circle with radius r centered at the (x, y) coordinates in the given color.
        """
        raise NotImplemented()

    def draw(self, vector_font, s: str, x: int, y: int, fg: int=WHITE, scale: int=1.0):
        """
        Draw text to the display using the specified hershey vector font with
        the coordinates as the lower-left corner of the text. The foreground
        color of the text can be set by the optional argument fg, otherwise
        the foreground color defaults to WHITE. The size of the text can be
        scaled by specifying a scale value. The scale value must be larger
        than 0 and can be a floating point or an integer value. The scale value
        defaults to 1.0. See the README.md in the vector/fonts directory
        for example fonts and the utils directory for a font conversion program.
        """
        raise NotImplemented()

    def draw_len(self, vector_font, s: str, scale: int=1.0):
        """
        Returns the width of the string in pixels if drawn with the specified font.
        """
        raise NotImplemented()

    def jpg(self, jpg_filename: str, x: int, y: int, method=None):
        """
        Draw JPG file on the display at the given x and y coordinates as the
        upper left corner of the image. There memory required to decode and
        display a JPG can be considerable as a full screen 320x240 JPG would
        require at least 3100 bytes for the working area + 320 * 240 * 2 bytes
        of ram to buffer the image. Jpg images that would require a buffer
        larger than available memory can be drawn by passing SLOW for method.
        The SLOW method will draw the image a piece at a time using the Minimum
        Coded Unit (MCU, typically a multiple of 8x8) of the image.
        """
        raise NotImplemented()

    def jpg_decode(self, jpg_filename: str, x: int, y: int, width: int, height: int):
        """
        Decode a jpg file and return it or a portion of it as a tuple composed
        of (buffer, width, height). The buffer is a color565 blit_buffer
        compatible byte array. The buffer will require width * height * 2 bytes of memory.

        If the optional x, y, width and height parameters are given the buffer
        will only contain the specified area of the image.
        See examples/T-DISPLAY/clock/clock.py
        examples/T-DISPLAY/toasters_jpg/toasters_jpg.py for examples.
        """
        raise NotImplemented()

    def polygon_center(self, polygon: List[Tuple[int, int]]):
        """
        Return the center of the polygon as an (x, y) tuple.
        The polygon should consist of a list of (x, y) tuples forming a closed convex polygon.
        """
        raise NotImplemented()

    def fill_polygon(self, polygon: List[Tuple[int, int]], x: int, y: int, color: int,
                     angle: int=0, center_x: int=0, center_y: int=0):
        """
        Draw a filled polygon at the x, y coordinates in the color given.
        The polygon may be rotated angle radians about the center_x and center_y point.
        The polygon should consist of a list of (x, y) tuples forming a closed convex polygon.
        """

    def polygon(self, polygon: List[Tuple[int, int]], x: int, y: int, color: int,
                angle: int, center_x: int, center_y: int):
        """
        Draw a polygon at the x, y coordinates in the color given.
        The polygon may be rotated angle radians a bout the center_x and center_y point.
        The polygon should consist of a list of (x, y) tuples forming a closed convex polygon.

        See the T-Display roids.py for an example.
        """
        raise NotImplemented()

    def bounding(self, status: bool, as_rect=False):
        """
        Bounding turns on and off tracking the area of the display that has been written to.
        Initially tracking is disabled, pass a True value to enable tracking and False to
        disable. Passing a True or False parameter will reset the current bounding rectangle
        to (display_width, display_height, 0, 0).

        Returns a four integer tuple containing (min_x, min_y, max_x, max_y)
        indicating the area of the display that has been written to since the last clearing.

        If as_rect parameter is True, the returned tuple will contain
        (min_x, min_y, width, height) values.
        """
        raise NotImplemented()

    def offset(self, x_start: int, y_start: int):
        """
        The memory in the ST7789 controller is configured for a 240x320 display.
        When using a smaller display like a 240x240 or 135x240 an offset needs
        to added to the x and y parameters so that the pixels are written to
        the memory area that corresponds to the visible display. The offsets
        may need to be adjusted when rotating the display.
        """
        raise NotImplemented()
