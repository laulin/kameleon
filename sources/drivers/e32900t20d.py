
# See https://github.com/vindolin/Python-Ebyte-E32
# See https://github.com/effevee/loraE32

class E32900T20D:
    DEFAULT_CONFIGURATION = b"\xC0\x00\x00\x1A\x17\x44"
    def __init__(self, m0, m1, uart, aux) -> None:
        self._m0_pin = m0
        self._m1_pin = m1
        self._uart = uart
        self._aux = aux

    def setup(self)->None:
        # configure the peripheral
        raise NotImplemented()

    def send_frame(self, payload:bytes)->int:
        # send a payload on a channel, with an adress (0xFFFF or 0x0000 for broadcasing on the channel)
        raise NotImplemented()
    
    def recv_frame(self) -> bytes:
        raise NotImplemented()
    
    def availables(self) -> bool:
        raise NotImplemented()
    
    def set_mode(self, mode:int)->None:
        raise NotImplemented()
    
    def write_configuration(self, bytes)->None:
        raise NotImplemented()
    
    def read_configuration(self)->bytes:
        raise NotImplemented()
    
    def read_version(self)->bytes:
        raise NotImplemented()
    
    def reset(self)->None:
        raise NotImplemented()