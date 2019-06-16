import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
pines = [7,11,13,15]
#pines = [29,31,33,35]

for pin in pines: 
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin, 0)

#secuencia = [[1,1,0,0], [0,1,1,0], [0,0,1,1], [1,0,0,1]]
secuencia = [ [1,0,0,0], [1,1,0,0], [0,1,0,0], [0,1,1,0], [0,0,1,0], [0,0,1,1], [0,0,0,1], [1,0,0,1] ]

#for i in range (2048):
while True: 
	for seq in range (8):
		for pin in range (4):
			GPIO.output(pines[pin], secuencia[seq][pin])
		time.sleep(0.005)

GPIO.cleanup()