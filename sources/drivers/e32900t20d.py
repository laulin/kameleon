
# See https://github.com/vindolin/Python-Ebyte-E32
# See https://github.com/effevee/loraE32

import time

class E32900T20D:
    DEFAULT_CONFIGURATION = b"\xC1\x00\x00\x1A\x17\x44"
    MODE_NORMAL = 0
    MODE_WAKE_UP = 1
    MODE_POWER_SAVING = 2
    MODE_SLEEP = 3
    def __init__(self, m0, m1, uart, aux) -> None:
        self._m0_pin = m0
        self._m1_pin = m1
        self._uart = uart
        self._aux = aux

        self._current_mode = E32900T20D.MODE_NORMAL

    def setup(self)->None:
        # configure the peripheral
        self._current_mode = E32900T20D.MODE_NORMAL
        self.set_mode(E32900T20D.MODE_NORMAL)


    def send_frame(self, payload:bytes)->int:
        # send a payload on a channel, with an adress (0xFFFF or 0x0000 for broadcasing on the channel)
        raise NotImplemented()
    
    
    def recv_frame(self) -> bytes:
        raise NotImplemented()
    
    def availables(self) -> bool:
        return self._aux.value()
    
    def set_mode(self, mode:int)->None:
        if mode == self._current_mode:
            return
        print(f"change mode to {mode}")
        self._current_mode = mode
        if mode == 0:
            self._m0_pin.value(0)
            self._m1_pin.value(0)
        elif mode == 1:
            self._m0_pin.value(1)
            self._m1_pin.value(0)
        elif mode == 2:
            self._m0_pin.value(0)
            self._m1_pin.value(1)
        elif mode == 3:
            self._m0_pin.value(1)
            self._m1_pin.value(1)
        else:
            raise Exception(f"Mode {mode} is not valid")
    
    def write_configuration(self, bytes)->None:
        raise NotImplemented()
    
    def read_configuration(self)->bytes:
        raise NotImplemented()
    
    def read_version(self)->dict:
        CMD = b"\xc3\xc3\xc3"
        MODEL = { '0x32':433, '0x38':470, '0x45':868, '0x44':915, '0x46':170 }
        mode_stack = self._current_mode
        time.sleep_ms(50)
        self.set_mode(E32900T20D.MODE_SLEEP)
        time.sleep_ms(50)
        self._uart.write(CMD)

        # To be improved
        time.sleep_ms(200)

        data = self._uart.read(6)
        print(data)
        # output = {
        #     "model" : MODEL[data[1]],
        #     "version" : hex(data[2]),
        #     "feature" : hex(data[3])
        # }

        self.set_mode(mode_stack)

        #return output
    
    def reset(self)->None:
        raise NotImplemented()