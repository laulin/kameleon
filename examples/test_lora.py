import hal
import time

# This example show how to setup the lora device and send a frame

_, _, _, _, lora = hal.setup()

def run():

    lora.setup()
    time.sleep_ms(2)
    lora.set_mode(lora.MODE_NORMAL)
    time.sleep_ms(2)
    print(lora.read_version())
    time.sleep_ms(20)
    print(lora.read_configuration())
    lora.set_mode(lora.MODE_WAKE_UP)
    time.sleep_ms(2)
    lora.wait()
    lora.send_frame(b"deadbeef")


run()