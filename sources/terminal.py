import font_8x16

class Terminal:
    FONT_HEIGHT = font_8x16.HEIGHT
    FONT_WIDTH = font_8x16.WIDTH
    TFT_WIDTH = 320
    TFT_HEIGHT = 240
    LINE_LENGTH = int(TFT_WIDTH / FONT_WIDTH)
    MAX_LINES = int(TFT_HEIGHT/FONT_HEIGHT) - 2
    def __init__(self, tft, keyboard) -> None:
        self._tft = tft
        self._keyboard = keyboard

        self._on_enter = None
        self._lines = []
        self._lines_updated = False
        self._prompt = ""

    def draw_sep(self, bitmap):
        offset = int(Terminal.TFT_WIDTH / bitmap.WIDTH)
        for i in range(offset):
            self._tft.bitmap(bitmap, i*bitmap.WIDTH, Terminal.TFT_HEIGHT - Terminal.FONT_HEIGHT*2, 0)

    def update(self):
        if self.update_keyboard():
            self.draw_prompt()

        self.draw_lines()

    def update_keyboard(self):
        updated = False
        events = self._keyboard.keys

        for status, key in events:
            if status == self._keyboard.PRESS:
                
                if key == self._keyboard.BACK_SPACE:
                    self._prompt = self._prompt[:-1]
                    updated = True
                elif key == "\n":
                    if self._on_enter:
                        self._on_enter(self._prompt)
                    self._prompt = ""
                    updated = True
                elif ord(key) >= 0x20:
                    self._prompt += key
                    updated = True

        if len(self._prompt) > Terminal.MAX_LINES:
            self._prompt = self._prompt[0:Terminal.LINE_LENGTH]

        return updated

    def draw_prompt(self):
        y = Terminal.TFT_HEIGHT - Terminal.FONT_HEIGHT
        self._tft.text(font_8x16, self._prompt, 0, y)
        x = len(self._prompt) * Terminal.FONT_WIDTH
        sx = Terminal.TFT_WIDTH - x
        self._tft.fill_rect(x, y, sx, Terminal.FONT_HEIGHT, 0)

    
    def add_line(self, line:str):

        if len(line) > Terminal.LINE_LENGTH:
            line = line[0:Terminal.LINE_LENGTH]

        self._lines.append(line)

        if len(self._lines) > Terminal.MAX_LINES:
            self._lines = self._lines[1:]

        self._lines_updated = True

    def draw_lines(self):
        if self._lines_updated:
            self._tft.fill_rect(0, 0, Terminal.TFT_WIDTH, Terminal.FONT_HEIGHT * Terminal.MAX_LINES, 0)
            for i, l in enumerate(self._lines):
                self._tft.text(font_8x16, l, 0, i*Terminal.FONT_HEIGHT)

            self._lines_updated = False

    def on_enter_callback(self, callback):
        self._on_enter = callback


    

    