"""
Comunicacion Uart raspberry y arduino (Receptor)
"""

import serial
import time

port = serial.Serial(
	port = "/dev/ttyS0", 
	baudrate=115200,
	parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
	)
print("Bluetooth conectado")

contador = 0

try:
    while 1: 
        data = port.readline()
        if data is not None: 
            #print(int(data))
            print(data.decode('ascii'   ))
            contador+= 1
except KeyboardInterrupt:
    print("pulsos totales {}".format(contador))
    print("Quit")