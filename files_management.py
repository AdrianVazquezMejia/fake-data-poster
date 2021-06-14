import datetime
import json
import logging


log = logging.getLogger('files')
ch = logging.NullHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)


def save2file(file, data):
    file.seek(0)
    file.truncate()
    json.dump(data, file)


def update_post_file(serial, data):
    with open("post.json", 'r+') as post_file:
        post_dic = json.load(post_file)
        updates = post_dic['updates']
        for meter_dict in updates:
            if serial.hex() == meter_dict['meterid']:
                meter_dict["energy"] = meter_dict["energy"]+ data
                now = str(datetime.datetime.now())
                meter_dict["date"] = now
                log.debug("updated  %s", str(meter_dict))
                break
        post_dic['updates'] = updates
        save2file(post_file, post_dic)


def update_energy_file(serial, data):
    with open("energy.json", 'r+') as energy_file:
        energy_dic = json.load(energy_file)
        energy_dic[serial.hex()] = energy_dic[serial.hex()]+data
        log.info("Updated %s: %s at %s", serial.hex(), str(data),str(datetime.datetime.now()) )
        save2file(energy_file, energy_dic)


def f_energy_boot(loras,slaves, energy_path):
    with open(energy_path, 'r+') as energy_file:
        energy_dic = json.load(energy_file)
        for lora_edges in loras:
            for slave in range(slaves):
                id_meter = (lora_edges).to_bytes(
                    2, 'big') + (slave).to_bytes(1, 'big')
                if id_meter.hex() not in energy_dic.keys():
                    energy_dic[id_meter.hex()] = 0
            log.debug("Energy updated %s", str(energy_dic))
            save2file(energy_file, energy_dic)
        energy_file.close()


def f_post_boot(loras,slaves, post_path):
    with open(post_path, 'r+') as post_file:
        post_dic = json.load(post_file)
        log.debug("post dic %s", str(post_dic))
        updates = post_dic['updates']
        log.debug(str(updates))
        for lora_edges in loras:
            for slave in range(slaves):
                id_meter = (lora_edges).to_bytes(
                    2, 'big') + (slave).to_bytes(1, 'big')
                log.debug("idmeter: %s", str(id_meter.hex()))
                isUpdate = False
                for update in updates:
                    isUpdate = False
                    if id_meter.hex() == update['meterid']:
                        isUpdate = True
                        break
                if not isUpdate:
                    with open("energy.json","r+") as energy_file:
                        energy_dic = json.load(energy_file)
                        meter_dic = {}
                        meter_dic["meterid"] = id_meter.hex()
                        meter_dic["energy"] =  energy_dic[id_meter.hex()]
                        now = datetime.datetime.now()
                        now = str(now)
                        meter_dic["date"] = now
                        updates.append(meter_dic)
                        log.debug("appending %s", str(updates))
            post_dic['updates'] = updates
        save2file(post_file, post_dic)
        post_file.close()
