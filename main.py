from _datetime import datetime
from files_management import f_energy_boot
from files_management import *
from random import randint
import time
from post_http import post_scada

if __name__ == "__main__":
    print("Start App")
    fake_rpi = [120,90]
    METER_QUANTITY = 250
    f_energy_boot(fake_rpi, METER_QUANTITY,"energy.json")
    f_post_boot(fake_rpi, METER_QUANTITY,"post.json")
    time_to_post = 120
    while(1):
        for lora_id in fake_rpi:
            print("updating :", lora_id)
            for slave in range(METER_QUANTITY):
                energy_increment = randint(0, 5)
                serial = lora_hex = (lora_id).to_bytes(2, "big")+(slave).to_bytes(1, 'big')
                update_energy_file(serial, energy_increment)
                update_post_file(serial,energy_increment)
        post_scada("post.json",False)
        for i in range(time_to_post):
            print("Printing in :", time_to_post-i-1 ,"s")
            time.sleep(1)       
