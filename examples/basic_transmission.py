import time

import hal 
from terminal import Terminal
import bitmap.terminal_bitmap as terminal_bitmap

tft, _, keyboard, _, lora = hal.setup()

terminal = Terminal(tft, keyboard)
terminal.draw_sep(terminal_bitmap)

def update_recv():
    if lora.available():
        if lora.recv_frame_length() > 0:
            data = lora.recv_frame()
            terminal.add_line("recv: " + str(data, "ascii"))


def on_enter(data:str):
    if not lora.available():
        lora.wait()
    
    terminal.add_line("send: " + data)
    lora.send_frame(bytes(data, "ascii"))

    lora.wait()

terminal.on_enter_callback(on_enter)

terminal.add_line(str(lora.read_version()))

while True:
    update_recv()
    terminal.update()

    time.sleep_ms(10)
