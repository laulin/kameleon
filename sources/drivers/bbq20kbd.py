# based on https://github.com/solderparty/arturo182_CircuitPython_BBQ10Keyboard/blob/master/bbq10keyboard.py
# under MIT licence

from micropython import const
import time

# https://github.com/solderparty/i2c_puppet

_ADDRESS_KBD = const(0x1F)

_REG_VER = const(0x01)  # fw version
_REG_CFG = const(0x02)  # config
_REG_INT = const(0x03)  # interrupt status
_REG_KEY = const(0x04)  # key status
_REG_BKL = const(0x05)  # backlight
_REG_DEB = const(0x06)  # debounce cfg
_REG_FRQ = const(0x07)  # poll freq cfg
_REG_RST = const(0x08)  # reset
_REG_FIF = const(0x09)  # fifo
_REG_BK2 = const(0x0A)  # backlight 2
_REG_DIR = const(0x0B)  # gpio direction
_REG_PUE = const(0x0C)  # gpio input pull enable
_REG_PUD = const(0x0D)  # gpio input pull direction
_REG_GIO = const(0x0E)  # gpio value
_REG_GIC = const(0x0F)  # gpio interrupt config
_REG_GIN = const(0x10)  # gpio interrupt status
_REG_HLD = const(0x11)  # Key hold threshold configuration
_REG_ADR = const(0x12)  # Device I2C address
_REG_IND = const(0x13)  # Interrupt duration
_REG_CF2 = const(0x14)  # The configuration register 2
_REG_TOX = const(0x15)  # Trackpad X Position
_REG_TOY = const(0x16)  # Trackpad Y position


_WRITE_MASK      = const(1 << 7)

CFG_OVERFLOW_ON  = const(1 << 0)
CFG_OVERFLOW_INT = const(1 << 1)
CFG_CAPSLOCK_INT = const(1 << 2)
CFG_NUMLOCK_INT  = const(1 << 3)
CFG_KEY_INT      = const(1 << 4)
CFG_PANIC_INT    = const(1 << 5)
CFG_REPORT_MODS  = const(1 << 6)
CFG_USE_MODS     = const(1 << 7)

INT_OVERFLOW     = const(1 << 0)
INT_CAPSLOCK     = const(1 << 1)
INT_NUMLOCK      = const(1 << 2)
INT_KEY          = const(1 << 3)
INT_PANIC        = const(1 << 4)
INT_GPIO         = const(1 << 5)  # since FW 0.4

KEY_CAPSLOCK     = const(1 << 5)
KEY_NUMLOCK      = const(1 << 6)
KEY_COUNT_MASK   = const(0x1F)

DIR_OUTPUT       = const(0)
DIR_INPUT        = const(1)

PUD_DOWN         = const(0)
PUD_UP           = const(1)

STATE_IDLE       = const(0)
STATE_PRESS      = const(1)
STATE_LONG_PRESS = const(2)
STATE_RELEASE    = const(3)


# on rp2 : I2C(1, scl=Pin(3), sda=Pin(2), freq=400000)
class BBQ20Kbd:
    def __init__(self, i2c):
        self._i2c = i2c
        self._buffer = bytearray(2)

        if _ADDRESS_KBD not in self._i2c.scan():
            raise Exception(f"Can reach the keyboad with i2c {self._i2c}")

        self.reset()

    def reset(self):
        # This function reset the keyboard
        # It waits until the device is ready. After 1 second, a timeout is raised
        buffer = bytearray(1)
        buffer[0] = _REG_RST
        self._i2c.writeto(_ADDRESS_KBD, buffer)

        # Wait
        counter = 100
        while counter:
            if _ADDRESS_KBD in self._i2c.scan():
                return
            else:
                time.sleep(0.01)
                counter -= 1
        raise Exception("Failed to reach the keyboard after the reset")

    @property
    def version(self):
        ver = self._read_register(_REG_VER)
        return (ver >> 4, ver & 0x0F)

    @property
    def status(self):
        status = self._read_register(_REG_KEY)
        key_count = status & KEY_COUNT_MASK
        capslock = (status & KEY_CAPSLOCK) > 0
        numlock = (status & KEY_NUMLOCK) > 0
        return numlock, capslock, key_count

    @property
    def key_count(self):
        _, _, key_count = self.status
        return key_count

    @property
    def key(self):
        # return key status and key str
        # key status : 
        # * 1 : push
        # * 2 : hold
        # * 3 : release
        
        if self.key_count == 0:
            return None

        self._i2c.readfrom_mem_into(_ADDRESS_KBD, _REG_FIF, self._buffer)

        return (int(self._buffer[0]), chr(self._buffer[1]))

    @property
    def keys(self):
        keys = []

        for _ in range(self.key_count):
            keys.append(self.key)

        return keys

    @property
    def backlight(self):
        return self._read_register(_REG_BKL) / 255

    @backlight.setter
    def backlight(self, value):
        self._write_register(_REG_BKL, int(255 * value))

    @property
    def backlight2(self):
        if self.version < (0, 4):
            raise NotImplementedError('This function requires FW version 0.4 or newer')

        return self._read_register(_REG_BK2) / 255

    @backlight.setter
    def backlight2(self, value):
        if self.version < (0, 4):
            raise NotImplementedError('This function requires FW version 0.4 or newer')

        self._write_register(_REG_BK2, int(255 * value))

    @property
    def gpio(self):
        return self._read_register(_REG_GIO)

    @gpio.setter
    def gpio(self, value):
        self._write_register(_REG_GIO, value)


    def _read_register(self, reg:int)->None:
        # read a register and store the result in the class buffer

        output = self._i2c.readfrom_mem(_ADDRESS_KBD, reg, 1)

        return output[0]

    def _write_register(self, reg:int, value:int)->None:
        addr = reg | _WRITE_MASK
        buffer = bytearray(1)
        buffer[0] = value
        self._i2c.writeto_mem(_ADDRESS_KBD, addr, buffer)

    def _update_register_bit(self, reg, bit, value):
        reg_val = self._read_register(reg)
        old_val = reg_val

        if value:
            reg_val |= (1 << bit)
        else:
            reg_val &= ~(1 << bit)

        if reg_val != old_val:
            self._write_register(reg, reg_val)

    def _get_register_bit(self, reg, bit):
        return self._read_register(reg) & (1 << bit) != 0

    @property
    def interrupt_status(self):
        return self._read_register(_REG_INT)


    def configuration(self, use_mods:bool=False, report_mods:bool=False, key_int:bool=False, numlock_int:bool=False, capslock_int:bool=False, overflow_int:bool=False, overflow_on:bool=False):
        # use_mods : Should Alt, Sym and the Shift keys modify the keys being reported.
        # report_mods : Should Alt, Sym and the Shift keys be reported as well.
        # key_int : Should an interrupt be generated when a key is pressed.
        # numlock_int : Should an interrupt be generated when Num Lock is toggled.
        # capslock_int : Should an interrupt be generated when Caps Lock is toggled.
        # overflow_int : Should an interrupt be generated when a FIFO overflow happens.
        # overflow_on : When a FIFO overflow happens, should the new entry still be pushed, 
        #               overwriting the oldest one. If 0 then new entry is lost.
        
        register = 0
        if use_mods: register |= CFG_USE_MODS
        if report_mods: register |= CFG_REPORT_MODS
        if key_int: register |= CFG_KEY_INT
        if numlock_int: register |= CFG_NUMLOCK_INT
        if capslock_int: register |= CFG_CAPSLOCK_INT
        if overflow_int: register |= CFG_OVERFLOW_INT
        if overflow_on: register |= CFG_OVERFLOW_ON
        
        self._write_register(_REG_CFG, register)

    @property
    def trackpad(self):
        tox = self._read_register(_REG_TOX)
        toy = self._read_register(_REG_TOY)
        return tox | (-(tox & 0x80)), toy | (-(toy & 0x80))
