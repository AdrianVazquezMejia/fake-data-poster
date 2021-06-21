from _datetime import datetime, date
from files_management import f_energy_boot
from files_management import *
from random import randint
from time import sleep
from post_http import post_scada
from datetime import time
from datetime import datetime

if __name__ == "__main__":
    print("Start App")
    fake_rpi = [120,90]
    METER_QUANTITY = 250
    f_energy_boot(fake_rpi, METER_QUANTITY,"energy.json")
    f_post_boot(fake_rpi, METER_QUANTITY,"post.json")
    time_to_post = 120
    time_morning = time(hour=8, minute=0)
    time_night = time(hour=18, minute=0)
    time_sleep = time(hour=22, minute=0)
    while(1):
        for lora_id in fake_rpi:
            print("updating :", lora_id)
            hour, minutes,_= str(datetime.now()).split()[1].split(":")
            time_now = time(hour=int(hour), minute=int(minutes))
            max_pulses = 5
            if(time_now<time_night and time_now>time_morning):
                max_pulses = 5
            if(time_now<time_sleep and time_now>time_night):
                max_pulses = 15
            if(time_now<time_morning or time_now>time_sleep):
                max_pulses = 1
            for slave in range(METER_QUANTITY):
                energy_increment = randint(0, max_pulses)
                serial = lora_hex = (lora_id).to_bytes(2, "big")+(slave).to_bytes(1, 'big')
                update_energy_file(serial, energy_increment)
                update_post_file(serial,energy_increment)
        post_scada("post.json",True)
        for i in range(time_to_post):
            print("Printing in :", time_to_post-i-1 ,"s")
            sleep(1)       
