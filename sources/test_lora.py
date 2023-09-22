import hal
import time

_, _, _, _, lora = hal.setup()

def run():

    lora.setup()
    time.sleep_ms(2)
    lora.set_mode(lora.MODE_POWER_SAVING)
    time.sleep_ms(2)
    lora.set_mode(lora.MODE_WAKE_UP)
    time.sleep_ms(2)
    print(lora.read_version())

run()