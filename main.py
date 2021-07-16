from _datetime import datetime, date
from random import randint
from time import sleep
from post_http import post_scada
from datetime import time
from sqlite_manager import *
from datetime import datetime

def update_energy(meter_serial, energy_increment):
    meter_energy = get_energy(meter_serial)
    update_date_base(meter_serial, meter_energy + energy_increment)
    
if __name__ == "__main__":
    print("Start App")
    fake_rpi = [120,90]
    METER_QUANTITY = 250
    with open("config.json","r+") as config_file:
        config_dic = json.load(config_file)
    energy_load(config_dic["loras"])
    time_to_post = config_dic["post_time"]
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
                serial = (lora_id).to_bytes(2, "big")+(slave).to_bytes(1, 'big')
                update_energy(serial.hex(), energy_increment)
        post_json = load_json( config_dic["ID"], config_dic["write_api_key"])
        post_scada(post_json,False)
        for i in range(time_to_post):
            print("Printing in :", time_to_post-i-1 ,"s")
            sleep(1)       
