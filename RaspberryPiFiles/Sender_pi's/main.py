# Code from https://timhanewich.medium.com/how-to-use-a-reyax-rylr998-lora-module-with-a-raspberry-pi-pico-and-other-microcontrollers-4ae52686836f
# imports
import reyax
import time
import machine
import network
# from pythonping import ping


def Scan_Wifi_and_Send():
    networks = wlan.scan()

    entries = []
    for net in networks:
        ssid = net[0].decode("utf-8").repace(",","").replace("|","")
        rssi = net[3]
        entries.append(f"{ssid}:{rssi}")


    payload = "|".join(entries)


    # LoRa only allows 240 bytes of data
    if len(payload) > 200:
        payload = payload[:200]

    lora.send(0, payload.encode("ascii"))

wlan = network.Wlan()
wlan.active(True)



# setting up GPIO pins and lora for the radio transmitter
u = machine.UART(0, baudrate=115200, tx=machine.Pin(0), rx=machine.Pin(1))
lora = reyax.RYLR998(u)

if lora.pulse: # the pulse function returns True if a simple test command was able to validate the existence of the connected RYLR998 module.
    print("Connected")

while True:
    for i in range(60): # send a message every 15 minutes
        # sleep for 15 seconds
        Scan_Wifi_and_Send()
        time.sleep(15)