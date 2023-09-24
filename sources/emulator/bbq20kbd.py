import logging
import time
import sys

import pygame

class BBQ20Kbd:
    PRESS = 1
    UP = 3
    DOWN = 2

    # special keys
    ANSWER = "\x06"
    HANG_UP = "\x12"
    BLACKBERRY = "\x11"
    BACK = "\x07"
    CLICK = "\x05"
    ALT = "\x1a"
    SHIFT_LEFT = "\x1b"
    SHIFT_RIGHT = "\x1c"
    SYM = "\x1d"
    BACK_SPACE = "\x08"
    
    def __init__(self) -> None:
        self._log = logging.getLogger("BBQ20Kbd")
        self._key_status = dict()
    
    def reset(self):
        raise NotImplemented()

    @property
    def version(self):
        return 0

    @property
    def status(self):
        key_count = 0
        capslock = False
        numlock = False
        return numlock, capslock, key_count

    @property
    def key_count(self):
        _, _, key_count = self.status
        return key_count

    @property
    def key(self):
        for event in pygame.event.get([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]):
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                self._key_status[event.key] = time.time()
                try:
                    char = chr(event.key)
                except:
                    char = event.key
                return BBQ20Kbd.PRESS, char

            if event.type == pygame.KEYUP:
                del self._key_status[event.key]
                try:
                    char = chr(event.key)
                except:
                    char = event.key
                return BBQ20Kbd.UP, char
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._key_status[event.button] = time.time()
                return BBQ20Kbd.PRESS, chr(event.button)

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                del self._key_status[event.button]
                return BBQ20Kbd.UP, chr(event.button)
        
        for key in self._key_status:
            if self._key_status[key] > 0 and time.time() - self._key_status[key] > 0.5:
                self._key_status[key] = -1
                try:
                    char = chr(key)
                except:
                    char = key
                return BBQ20Kbd.DOWN, char
        

    @property
    def keys(self):
        keys = []

        for _ in range(self.key_count):
            keys.append(self.key)

        return keys

    @property
    def backlight(self):
        return self._backlight

    @backlight.setter
    def backlight(self, value):
        self._backlight = value



    def configuration(self, use_mods:bool=False, report_mods:bool=False, key_int:bool=False, numlock_int:bool=False, capslock_int:bool=False, overflow_int:bool=False, overflow_on:bool=False):
        # use_mods : Should Alt, Sym and the Shift keys modify the keys being reported.
        # report_mods : Should Alt, Sym and the Shift keys be reported as well.
        # key_int : Should an interrupt be generated when a key is pressed.
        # numlock_int : Should an interrupt be generated when Num Lock is toggled.
        # capslock_int : Should an interrupt be generated when Caps Lock is toggled.
        # overflow_int : Should an interrupt be generated when a FIFO overflow happens.
        # overflow_on : When a FIFO overflow happens, should the new entry still be pushed, 
        #               overwriting the oldest one. If 0 then new entry is lost.
        
        pass

    @property
    def trackpad(self):
        for event in pygame.event.get([pygame.MOUSEMOTION]):
            if event.type == pygame.MOUSEMOTION:
                if event.pos[0] != self._trackpad[0] or event.pos[1] != self._trackpad[1]:
                    dx = self._trackpad[0] - event.pos[0]
                    dy = self._trackpad[1] - event.pos[1]
                    self._trackpad[0] = event.pos[0]
                    self._trackpad[1] = event.pos[1]

                    return dx, dy
                
        return 0,0