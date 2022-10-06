from network import WLAN
import machine
import config
import ubinascii


def wifi_connect():
    wlan = WLAN(mode=WLAN.STA)
    nets = wlan.scan()
    for net in nets:
        print(net)
        if net.ssid == config.WIFI_SSID:
            print('Network found!')
            wlan.connect(net.ssid, auth=(net.sec, config.WIFI_PASS))
            while not wlan.isconnected():
                machine.idle()
            print('WLAN connection succeeded!')
            break
    return ubinascii.hexlify(machine.unique_id()).decode()
