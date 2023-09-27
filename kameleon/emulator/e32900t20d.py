
import redis

class E32900T20D:
    MODE_NORMAL = 0
    MODE_WAKE_UP = 1
    MODE_POWER_SAVING = 2
    MODE_SLEEP = 3
    CHANNEL_NAME = "lora"
    def __init__(self, redis:redis.Redis) -> None:
        self._redis = redis

        self._pubsub = self._redis.pubsub()
        self._pubsub.subscribe(E32900T20D.CHANNEL_NAME)

        self._tmp_message = None

    def setup(self)->None:
        pass

    def send_frame(self, payload:bytes)->int:
        self._redis.publish(E32900T20D.CHANNEL_NAME, payload)
    
    
    def recv_frame(self) -> bytes:
        if self._tmp_message is not None:
            output = self._tmp_message
            self._tmp_message = None
            return output
        
        for message in self._pubsub.listen():
            if message['type'] == 'message':
                return message['data']
    
    def recv_frame_length(self) -> int:
        if self._tmp_message is not None:
            return len(self._tmp_message)
        
        self._tmp_message = self.recv_frame()

        if self._tmp_message is None:
            return 0
        else:
            return len(self._tmp_message)
    
    def available(self) -> bool:
        return True
    
    def set_mode(self, mode:int)->None:
        pass
    
    def write_configuration(self, bytes)->None:
        raise NotImplemented()
       
    def read_configuration(self)->bytes:
        return b"\xC2\x00\x00\x1A\x06\x44"

    
    def read_version(self)->dict:
        output = {
            "model" : "0x32",
            "version" : "0x14",
            "feature" : "0x10"
        }

        return output
    
    def reset(self)->None:
        raise NotImplemented()
    
    def wait(self, timeout=100):
        pass