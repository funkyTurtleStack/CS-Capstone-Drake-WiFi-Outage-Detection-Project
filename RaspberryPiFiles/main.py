
# Code from https://timhanewich.medium.com/how-to-use-a-reyax-rylr998-lora-module-with-a-raspberry-pi-pico-and-other-microcontrollers-4ae52686836f
# imports
import reyax
import time
import machine
from pythonping import ping


# setting up GPIO pins and lora for the radio transmitter
u = machine.UART(0, baudrate=115200, tx=machine.Pin(0), rx=machine.Pin(1))
lora = reyax.RYLR998(u)


if lora.pulse: # the pulse function returns True if a simple test command was able to validate the existence of the connected RYLR998 module.
    print("Connected")


while True:

    for i in range(60): # send a message every 15 minutes
        # ping wifi
        result = ping("google.com", count=20, timeout=2, interval = 5)
        if result.success():
            print(result.rtt_avg_ms)


        # add wifi to text note

        # sleep for 15 seconds
        # time.sleep(15)


    # lora.send(0, "Hello World".encode("ascii"))
    print("test")
        