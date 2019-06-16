"""
Comunicacion Uart raspberry y arduino (Transmisor)
"""

import time
import serial
port = serial.Serial("/dev/ttyS0", baudrate=115200, timeout=3.0)
#port = serial.Serial("/dev/AMA0", baudrate=9600, timeout=3.0)
while True:
	#port.write("\r\nN")
	#port.write("\r\nH")
	port.write('H'.encode('ascii'))
	print("Enviado: H")
	time.sleep(1)
	#port.write("\r\nL")
	port.write('L'.encode('ascii'))
	print("Enviado: L")
	time.sleep(1)
	#rcv = port.read(10)
	#port.write("\r\nYou sent:" + repr(rcv))

# import time
# import serial

# ser=serial.Serial(
# 	port='/dev/ttyAMA0',
# 	baudrate = 9600,
# 	parity=serial.PARITY_NONE,
# 	stopbits=serial.STOPBITS_ONE,
# 	bytesize=serial.EIGHTBITS,
# 	timeout=1
# )

# counter=0

# while 1:
# 	ser.write("hello world")	
# 	time.sleep(1)
# 	counter += 1