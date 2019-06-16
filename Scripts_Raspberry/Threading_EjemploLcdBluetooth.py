import threading
import time
from threading import Thread

import serial
#import RPi.GPIO as GPIO
import math
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

class LCD(Thread):

	def __init__(self):

		Thread.__init__(self)
		
		RST = 24
		DC = 23
		SPI_PORT = 0
		SPI_DEVICE = 0
		disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))
		disp.begin()
		width = disp.width
		height = disp.height
		disp.clear()
		disp.display()	
		image = Image.new('1', (width, height))
		font = ImageFont.load_default()
		draw = ImageDraw.Draw(image)
		text = 'HOLA HOLA HOLA HOLA HOLA HOLA HOLA :('
		maxwidth, unused = draw.textsize(text, font=font)
		amplitude = height/4
		offset = height/2 - 4
		velocity = -2
		startpos = width
		print('Press Ctrl-C to quit.')
		pos = startpos

		while True: 

			#print('A')
			draw.rectangle((0,0,width,height), outline=0, fill=0)
			x = pos
			for i, c in enumerate(text):
				if x > width:
					break
				if x<-10:
					char_width, char_height = draw.textsize(c, font=font)
					x+=char_width
					continue
				y=offset+math.floor(amplitude*math.sin(x/float(width)*2.0*math.pi))
				draw.text((x, y), c, font=font, fill=255)
				char_width, char_height = draw.textsize(c, font=font)
				x+=char_width
			disp.image(image)
			disp.display()
			pos+=velocity
			if pos<-maxwidth:
				pos=startpos
			time.sleep(0.1)

		self.daemon = True
		self.start()

class BLUETOOTH(Thread):

	def __init__(self):

		Thread.__init__(self)
		self.daemon = True
		self.start()
		port = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=3.0)

		while True:
			#print('B')
			port.write("\r\nSay something:")
			time.sleep(1)



BLUETOOTH()	
LCD()
while True: 
	pass
