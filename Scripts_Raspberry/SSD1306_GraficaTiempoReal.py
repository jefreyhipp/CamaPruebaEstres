"""
Uso del modulo OLED SSD1306, donde se muestra una grafica en tiempo real del los valores
numericos recibidos en el puerto serial. Grafica Valor Serial vs N.
Se realiza un ajuste dependiendo de la cantidad N de elementos recibidos.  
"""

import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import RPi.GPIO as GPIO
import serial


if __name__ == "__main__":

	GPIO.setmode(GPIO.BCM)
	RST = 24
	DC = 23
	SPI_PORT = 0
	SPI_DEVICE = 0

	disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

	disp.begin()
	disp.clear()
	disp.display()
	width = disp.width
	height = disp.height
	image = Image.new('1', (width, height))
	draw = ImageDraw.Draw(image)
	draw.rectangle((0,0,width,height), outline=0, fill=0)
	font = ImageFont.load_default()
	#disp.image(image)
	#disp.display()

	# First define some constants
	offset = 1
	top = offset
	bottom = height - offset

	try:

		punto = []
		puntos = []
		datos = []
		i = 0
		maximo = 0

		port = serial.Serial(
			port = "/dev/ttyS0", 
			baudrate=9600,
			parity=serial.PARITY_NONE,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS)

		while True: 

			print("Listo para recibir datos")

			data = int(port.readline())

			if data is not None: 		#nueva lectura del sensor

				image = Image.new('1', (width,height))
				draw = ImageDraw.Draw(image)
				disp.clear()

				print("dato recibido")
				i += 1					#incrementamos en i cada vez que haya una nueva lectura
				
				datos.append(data)				
				punto.append(i)			#anadimos coordenada x del punto
				punto.append(data)		#anadimos coordenada y del punto
				puntos.append(punto)	#anadimos el punto anterior a la lista de puntos	
				punto = []

				espaciado_x = offset	#servira como contador para espaciar puntos en x
				espaciado_y = offset	#servira como contador para espaciar puntos en y

				if len(puntos) > 1:

					maximo = max(datos)
					resolucion_x = width // (len(puntos)-1)		#permitira ajustar los datos en el eje x
					resolucion_y = height // maximo			#permitira ajustar los datos en el eje y

					for n in range( len(puntos) - 1):

						x_inicial = puntos[n][0]
						y_inicial = puntos[n][1]*resolucion_y

						x_final = puntos[n+1][0]
						y_final = puntos[n+1][1]*resolucion_y

						draw.line([espaciado_x, y_inicial, espaciado_x + resolucion_x, y_final], fill=255)
						draw.line([offset, offset, offset, height - offset], fill=255)
						draw.line([offset, height - offset, width - offset, height - offset], fill=255)
						espaciado_x += resolucion_x 

			# Display image
			disp.image(image)
			disp.display()
			time.sleep(0.1)

	except KeyboardInterrupt:
		print("Quit")