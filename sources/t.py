import time

import hal 
from terminal import Terminal
import terminal_bitmap

tft, _, keyboard, _, lora = hal.setup()

terminal = Terminal(tft, keyboard)
terminal.draw_sep(terminal_bitmap)
terminal.on_enter_callback(terminal.add_line)

while True:
    terminal.update()

    time.sleep_ms(10)
