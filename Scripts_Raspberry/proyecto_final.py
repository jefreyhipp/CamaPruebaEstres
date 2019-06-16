"""
Union de codigo de Ejemplos Varios presentados en los archivos. 
Los procesos se manejaran en hilos paralelos. 
"""

import time
import sys
import serial
import RPi.GPIO as GPIO
from hx711 import HX711


longitud_inicial = 120
area_inicial = 60

GPIO.setmode(GPIO.BCM)

class celda_carga:

	def __init__(self):

		self.hx = HX711(5, 6) # sck, dout
		self.hx.set_reading_format("MSB", "MSB")
		self.hx.set_reference_unit(-130)
		self.hx.reset()
		self.hx.tare()
		print("Tare done! Add weight now...") 

		while True:
			self.lectura()

	def lectura(self):

		global lectura_celda

		try:

			#inicio = time.time()
			self.lectura_celda = self.hx.get_weight(1)
			#print(val) 

			self.hx.power_down()
			self.hx.power_up()

			#time.sleep(0.000001)
			#fin = time.time()
			#print("proceso: {}".format(fin - inicio))

		except (KeyboardInterrupt, SystemExit):
			print("Adios")
			sys.exit()

class inicio():

	contador = 0

	def __init__(self):

		global lectura_celda

		GPIO.setup(4, GPIO.IN)	 #DIR
		GPIO.setup(17, GPIO.OUT) #MS1
		GPIO.setup(27, GPIO.OUT) #MS2
		GPIO.setup(22, GPIO.OUT) #MS3
		GPIO.setup(26, GPIO.OUT) #FINAL CARRRERA

		self.bandera1 = False
		self.bandera2 = False
		self.contador = 0
		self.paso = 0
		self.temporal = [0,0]
		self.actual = [0,0]

		self.port = serial.Serial(
			port = "/dev/ttyS0", 
			baudrate=115200,
			parity=serial.PARITY_NONE,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS
		) 	

		fichero = open('datos.txt', 'w')

		try:

			if GPIO.input(26):										#se presiona el final carrera
				self.bandera1 = True

			if self.bandera1 == False: 	#aun sin presionar el final carrera
				GPIO.output(4, True) 	#a favor de las manecillas del reloj
				GPIO.output(17, False) 
				GPIO.output(27, False) 
				GPIO.output(22, False) 
				port.write('H'.encode('ascii'))
				print("Enviado: H")

			elif self.bandera1 == True and lectura_celda < 30 and paso == 0:
				GPIO.output(4, False)
				self.paso += 1
				port.write('H'.encode('ascii'))
				print("Enviado: H")

			elif self.bandera1 == True and self.lectura_celda >= 30 and paso == 1:
				GPIO.output(4, True)
				self.paso += 1
				self.bandera2 = True
				self.contador = 0
				port.write('H'.encode('ascii'))
				print("Enviado: H")
			
			while self.cuenta() < 40 and self.bandera2 == True :
				port.write('H'.encode('ascii'))
				print("Enviado: H")
			else: 
				self.bandera2 = False
				port.write('H'.encode('ascii'))
				print("Enviado: H")
				self.contador = 0
				GPIO.output(17, True) 
				GPIO.output(27, False) 
				GPIO.output(22, False) 

			while True:
				
				self.temporal = [self.actual[0], self.actual[1]]
				self.actual = [self.cuenta()*(0.002/1800)/longitud_inicial , ((self.lectura_celda/1000)*9.8)/area_inicial]

				delta_y = self.actual[0] - self.temporal[0]
				delta_x = self.actual[1] - self.temporal[1]

				if delta_y / delta_x < -100:
					port.write('L'.encode('ascii'))
					print("Enviado: L")


				fichero.write('{:.10f} , {:.10f}'.format(esfuerzo, deformacion))

		except (KeyboardInterrupt, SystemExit):
			print("Adios")
			fichero.close()

	def cuenta(self):

		while True:
			self.data = self.port.readline()
			if self.data is not None: 
				#print(data)
				self.contador+= 1
			return self.contador

if __name__ == "__main__":

	try: 

		t1 = Thread(target = celda_carga)
		t2 = Thread(target = inicio)
		t1.start()
		t2.start()

	except KeyboardInterrupt:

		print("Proceso terminado")