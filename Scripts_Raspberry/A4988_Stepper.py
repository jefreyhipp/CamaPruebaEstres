"""
Ejemplo del uso del modulo A49886 para el control de un motor stepper
"""

from time import sleep
import RPi.GPIO as GPIO

DIR = 12
STEP = 16
CW = 1
CCW = 0
SPR = 86400

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)

MODE = (26,19,13)
GPIO.setup(MODE, GPIO.OUT)

RESOLUTION ={
				'FULL': (0,0,0),
				'HALF': (1,0,0), 
				'1/4': (0,1,0),
				'1/8': (0,0,1),
				'1/16': (1,1,1)
			}
GPIO.output(MODE, RESOLUTION['FULL'])

step_count = SPR
delay = 0.001

GPIO.output(DIR, CW)
for x in range (step_count): 
	GPIO.output(STEP, GPIO.HIGH)
	sleep(delay)
	GPIO.output(STEP, GPIO.LOW)
	sleep(delay)

sleep(1)

GPIO.output(DIR, CCW)
for x in range (step_count*2): 
	GPIO.output(STEP, GPIO.HIGH)
	sleep(delay)
	GPIO.output(STEP, GPIO.LOW)
	sleep(delay)
