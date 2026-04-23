import reyax
import time
import machine

def Scan_Wifi_and_Send():
    # Fake scan results mimicking what network.WLAN.scan() returns
    networks = [
        (b"MyLaptopHotspot", b"", 1, -45, 3, False),
        (b"NeighborNet",     b"", 6, -78, 3, False),
        (b"TestNetwork",     b"", 11, -82, 3, False),
    ]

    entries = []
    for net in networks:
        ssid = net[0].decode("utf-8").replace(",", "").replace("|", "")
        rssi = net[3]
        entries.append(f"{ssid}:{rssi}")

    payload = "|".join(entries)

    if len(payload) > 200:
        payload = payload[:200]

    print("Payload:", payload)
    # lora.send(0, payload.encode("ascii"))  # uncomment when module arrives

u = machine.UART(0, baudrate=115200, tx=machine.Pin(0), rx=machine.Pin(1))
lora = reyax.RYLR998(u)

while True:
    Scan_Wifi_and_Send()
    time.sleep(15)