BITMAPS = 1
HEIGHT = 16
WIDTH = 16
COLORS = 2
BPP = 1
BITS = HEIGHT * WIDTH * BITMAPS * BPP
PALETTE = [0x0000,0xFFFF]
_bitmap =\
b'\xf0\xf0'\
b'\xe1\xe1'\
b'\xc3\xc3'\
b'\x87\x87'\
b'\x0f\x0f'\
b'\x1e\x1e'\
b'\x3c\x3c'\
b'\x78\x78'\
b'\xf0\xf0'\
b'\xe1\xe1'\
b'\xc3\xc3'\
b'\x87\x87'\
b'\x0f\x0f'\
b'\x1e\x1e'\
b'\x3c\x3c'\
b'\x78\x78'

BITMAP = memoryview(_bitmap)