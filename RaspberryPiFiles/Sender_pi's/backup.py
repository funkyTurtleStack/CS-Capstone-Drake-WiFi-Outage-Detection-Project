# Code from https://timhanewich.medium.com/how-to-use-a-reyax-rylr998-lora-module-with-a-raspberry-pi-pico-and-other-microcontrollers-4ae52686836f
# imports
import reyax
import time
import machine
import network
# from pythonping import ping


def Scan_Wifi_and_Send():
    networks = wlan.scan()
    print(f"Found {len(networks)} networks")

    entries = []
    for net in networks:
        ssid = net[0].decode("utf-8").replace(",","").replace("|","")
        rssi = net[3]
        entries.append(f"{ssid}:{rssi}")


    payload = "|".join(entries)


    # LoRa only allows 240 bytes of data
    if len(payload) > 200:
        payload = payload[:200]
        
    print(f"Sending: {payload}")

    try:
        lora.send(0, payload.encode("ascii"))
    except Exception as e:
        print(f"Send Failed: {e}")

wlan = network.WLAN(network.STA_IF)
wlan.active(True)



# setting up GPIO pins and lora for the radio transmitter
u = machine.UART(0, baudrate=115200, tx=machine.Pin(0), rx=machine.Pin(1))
lora = reyax.RYLR998(u)

try:
    if lora.pulse:
        print("Connected")
    else:
        print("LoRa not responding")
except Exception as e:
    print(f"LoRa init failed: {e}")


fail_count = 0
while True:
    for i in range(60): # send a message every 15 minutes
        # sleep for 15 seconds
        try:
            Scan_Wifi_and_Send()
            fail_cunt = 0
        except Exception as e:
            print(f"Error: {e}")
            fail_count += 1
            if fail_count >= r:
                print("Resetting UART module")
                u = machine.UART(0, baudrate=115200, tx=machine.Pin(0), rx = machine.Pin(1))
                fail_count = 0
        time.sleep(15)