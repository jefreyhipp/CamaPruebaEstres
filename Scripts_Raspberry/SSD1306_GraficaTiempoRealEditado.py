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

	"""
	El offset me limita a enviar datos mayores a height - (2*offset)
	"""
	offset = 7
	max_superior = offset
	max_inferior = height - 2*offset

	try:

		puntos = []
		coordenada_x = []
		coordenada_y = []
		i = 0

		port = serial.Serial(
			port = "/dev/ttyS0", 
			baudrate=9600,
			parity=serial.PARITY_NONE,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS)

		alfabeto = { 'epsilon': u'\u03B5', 'sigma': u'\u03C3'}

		#draw.text((1,1), alfabeto['epsilon']+'vs'+ alfabeto['sigma'],font=font,fill=255)
		draw.text((1,1), 'Esfuerzo vs Deformacion'font=font,fill=255)
		draw.line([offset, offset, offset, height - offset], fill=255)
		draw.line([offset, height - offset, width - offset, height - offset], fill=255)
		disp.image(image)
		disp.display()

		print("Listo para recibir datos")

		while True: 

			data = int(port.readline())

			if data is not None: 		#nueva lectura del sensor

				print("dato recibido")
				i += 1					#incrementamos en i cada vez que haya una nueva lectura
				
				coordenada_y.append(data)	#añadimos las coordenadas en y en una lista
				coordenada_x.append(i)		#añadimos las coordenadas en x en una lista

				punto = (data,i)		#creamos el nuevo punto
				puntos.append(punto)	#anadimos el punto anterior a la lista de puntos	

				espaciado_x = offset	#servira como contador para espaciar puntos en x
				espaciado_y = offset	#servira como contador para espaciar puntos en y

				#print("Esta es i: {} y estos son los puntos: {}".format(i,puntos))

				if len(puntos) > 1:

					image = Image.new('1', (width,height))
					draw = ImageDraw.Draw(image)
					disp.clear()

					maximo_y = max(coordenada_y)
					maximo_x = max(coordenada_x)
					resolucion_x = (width - 2*offset) // maximo_x	#permitira ajustar los datos en el eje x
					if resolucion_x < 1: 
						resolucion_x = 1
					resolucion_y = (height - 2*offset) // maximo_y	#permitira ajustar los datos en el eje y
					if resolucion_y < 1: 
						resolucion_y = 1

					#print("Esta es i: {} y estas son las resoluciones (x,y): ({} , {})".format(i,resolucion_x, resolucion_y))

					for n in range( len(puntos) - 1):

						x_inicial = coordenada_x[n]*resolucion_x
						y_inicial = coordenada_y[n]*resolucion_y
						if y_inicial > max_inferior:
							y_inicial = max_inferior

						x_final = coordenada_x[n+1]*resolucion_x
						y_final = coordenada_y[n+1]*resolucion_y
						if y_final > max_inferior:
							y_final =  max_inferior

						#print("Esta es i: {} y este es el punto graficado (x,y) , (x,y): ({} , {}) , ({} , {}) ".format(i,espaciado_x, y_inicial + offset, espaciado_x + resolucion_x, y_final + offset))
						#dibujamos lineas entre puntos
						draw.line([espaciado_x, y_inicial + offset, espaciado_x + resolucion_x, y_final + offset], fill=255)
						#dibujamos contornos
						draw.text((1,1),'Esfuerzo vs Deformacion',font=font,fill=255)
						draw.line([offset, offset, offset, height - offset], fill=255)
						draw.line([offset, height - offset, width - offset, height - offset], fill=255)
						espaciado_x += resolucion_x 

			# Display image
			disp.image(image)
			disp.display()
			time.sleep(0.1)

	except KeyboardInterrupt:
		print("Quit")