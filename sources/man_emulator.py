import emulator
import time
import font_8x16

e = emulator.Emulator()
e.init()

# e.pixel(1,10,emulator.WHITE)
# time.sleep(1)

# e.fill_rect(10,10,10,20,emulator.BLUE)
# time.sleep(1)

# e.rect(20,10,20,10,emulator.RED)
# time.sleep(1)

# e.fill(emulator.BLACK)
# time.sleep(1)

# e.hline(1,1,100, emulator.CYAN)
# e.vline(10,10,50, emulator.RED)
# time.sleep(1)

e.text(font_8x16, "abcdefgh", 1, 1)
time.sleep(2)
