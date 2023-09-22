
# See https://github.com/vindolin/Python-Ebyte-E32
# See https://github.com/effevee/loraE32

import time

class E32900T20D:
    DEFAULT_CONFIGURATION = b"\xC2\x00\x00\x1A\x06\x44"
    MODE_NORMAL = 0
    MODE_WAKE_UP = 1
    MODE_POWER_SAVING = 2
    MODE_SLEEP = 3
    def __init__(self, m0, m1, uart, aux) -> None:
        self._m0_pin = m0
        self._m1_pin = m1
        self._uart = uart
        self._aux = aux

        self._current_mode = E32900T20D.MODE_WAKE_UP

    def setup(self)->None:
        # configure the peripheral
        self._current_mode = E32900T20D.MODE_WAKE_UP
        self.set_mode(E32900T20D.MODE_WAKE_UP)

    def send_frame(self, payload:bytes)->int:
        # send a payload on a channel, with an adress (0xFFFF or 0x0000 for broadcasing on the channel)
        self._uart.write(payload)
        self._uart.flush()
    
    
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
    
    def _read_command(self, command:bytes, expected_bytes:int)->bytes:
        mode_stack = self._current_mode
        self.set_mode(E32900T20D.MODE_SLEEP)
        # write the command and wait all bits is transmitted
        self._uart.write(command)
        self._uart.flush()        
        # wait for the AUX raising edge
        self.wait()
      
        data = self._uart.read(expected_bytes)

        self.set_mode(mode_stack)

        return data
    
    def read_configuration(self)->bytes:
        CMD = b"\xc1\xc1\xc1"
        return self._read_command(CMD, 6)

    
    def read_version(self)->dict:
        CMD = b"\xc3\xc3\xc3"
        data = self._read_command(CMD, 4)

        output = {
            "model" : hex(data[1]),
            "version" : hex(data[2]),
            "feature" : hex(data[3])
        }

        return output
    
    def reset(self)->None:
        raise NotImplemented()
    
    def wait(self, timeout=100):
        while self.availables() == 0:
            time.sleep_ms(1)
            timeout -= 1
            if timeout == 0:
                raise Exception("Wait timeout")