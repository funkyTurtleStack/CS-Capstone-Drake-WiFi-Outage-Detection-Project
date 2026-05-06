# Code from https://timhanewich.medium.com/how-to-use-a-reyax-rylr998-lora-module-with-a-raspberry-pi-pico-and-other-microcontrollers-4ae52686836f
# imports
import reyax
import time
import machine
import network
# from pythonping import ping

def Scan_Wifi_and_write():
    # Find out Wifi networks
    networks = wlan.scan()

    # print(f"Found {len(networks)} networks")

    # Sending: :-55|eduroam:-78|DUEntertainment:-84|DUGuest:-78|:-69|eduroam:-64|DUEntertainment:-69|DUGuest:-60|:-78|DIRECT-Y5-CS-308:-66|:-28
    # (ssid, bssid, channel, RSSI, security, hidden)
    # security: Open, WEP, WPA-PSK, WPA2-PSK, WPA/WPA2-PSK
    # net: (b'DUGuest', b'\xd6n*w\x86\xa0', 6, -62, 0, 3)
    # rssi closer to 0 is better
    best_networks = {}
    for net in networks:
        # print("net:", net)
        ssid_raw = net[0].decode("utf-8")
        if ssid_raw in ("eduroam", "DUEntertainment", "DUGuest"):
            ssid = ssid_raw.replace(",", "").replace("|", "")
            rssi = net[3]
            # print (f"SSID: {ssid}, RSSI: {rssi}")
            if ssid not in best_networks or rssi > best_networks[ssid]: # Higher RSSI is better
                best_networks[ssid] = rssi
    with open("entries.txt", "a") as f:
        for ssid, rssi in best_networks.items():
            f.write(f"{ssid}:{rssi}\n")
        # print(f"written", f)

def Calculate_data(cycle_count):
    ed_speed = 0
    ed_count = 0
    DUE_speed = 0
    DUE_count = 0
    DUG_speed = 0
    DUG_count = 0


    with open("entries.txt", "r") as f:
        # cycle_count = 15
        # print(f"file contents: {f}")
        for entry in f:
            if "eduroam" in entry:
                ed_speed += int(entry.split(":")[1])
                ed_count += 1
            elif "DUEntertainment" in entry:
                DUE_speed += int(entry.split(":")[1])
                DUE_count += 1
            elif "DUGuest" in entry:
                DUG_speed += int(entry.split(":")[1])
                DUG_count += 1


        ed_avg = ed_speed / ed_count if ed_count > 0 else 0
        DUE_avg = DUE_speed / DUE_count if DUE_count > 0 else 0
        DUG_avg = DUG_speed / DUG_count if DUG_count > 0 else 0


        # print(f"ed_speed / count: {ed_avg}, DUE: {DUE_avg}, DUG: {DUG_avg}")
        # print(f"ed_%: {(ed_count/15)*100:.2f}%, DUE_%: {(DUE_count/15)*100:.2f}%, DUG_%: {(DUG_count/15)*100:.2f}%")


        with open("calculated.txt", "a") as g:
            g.write(f"Loc: {location}\n")
            g.write(f"ed_avg: {ed_avg}, DUE_avg: {DUE_avg}, DUG_avg: {DUG_avg}\n")
            g.write(f"ed_%: {(ed_count/cycle_count)*100:.2f}%, DUE_%: {(DUE_count/cycle_count)*100:.2f}%, DUG_%: {(DUG_count/cycle_count)*100:.2f}%\n")

def Send_payload():
    # payload = location
    with open("calculated.txt", "r") as f:
        payload = f.read()
        # print(f"Data to send: {payload}")


    # Clearing File Contents
    # print(f"payload: {payload")
    open("entries.txt", "w").close()
    open("calculated.txt", "w").close()
    
    payload = payload.replace("\n", " | ").strip()    

    # LoRa only allows 240 bytes of data
    if len(payload) > 200:
        payload = payload[:200]

    print(f"Sending: {payload}")

    try:
        lora.send(0, payload.encode("ascii"))
    except Exception as e:
        print(f"Send Failed: {e}")

# Location
location = "CS-3" # Collier Scripts 3rd floor

# Connect to WiFi
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
scans = 60 # 60 scans with 5 second sleep is 5 minutes
while True:
    successful_scans = 0 # Reset

    for i in range (scans):
        try:
            Scan_Wifi_and_write()
            successful_scans += 1
            fail_count = 0
        except Exception as e:
            print(f"Error: {e}")
            fail_count += 1
            if fail_count >= 3:
                print("Resetting UART module")
                u = machine.UART(0, baudrate=115200, tx=machine.Pin(0), rx = machine.Pin(1))
                fail_count = 0
        time.sleep(5) # Time in Seconds

    Calculate_data(successful_scans)


    Send_payload()


