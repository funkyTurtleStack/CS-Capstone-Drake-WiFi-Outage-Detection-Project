
# Code from https://timhanewich.medium.com/how-to-use-a-reyax-rylr998-lora-module-with-a-raspberry-pi-pico-and-other-microcontrollers-4ae52686836f
import reyax
import time
import machine
u = machine.UART(0, baudrate=115200, tx=machine.Pin(0), rx=machine.Pin(1))
lora = reyax.RYLR998(u)
if lora.pulse: # the pulse function returns True if a simple test command was able to validate the existence of the connected RYLR998 module.
    print("Connected")
    
while True:
    lora.send(0, "Hello World".encode("ascii"))
    print("test")
    time.sleep(5)