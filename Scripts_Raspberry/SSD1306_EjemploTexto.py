#Codigo demostrativo para el uso de una pantalla oled en raspberry pi 3 
#Yeffri J. Salazar
#Importamos librerias necesarias
import time 
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
#definimos variables 
RST = 24 #numero de pin donde esta conectado el pin RESET de la pantalla oled 
DC = 23 #numero de pin donde esta conectado el pin DC de la pantalla oled
SPI_PORT = 0 #puerto SPI
SPI_DEVICE = 0 #dispositivo SPI
#creamos el objeto controlador
oled= Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))
#definimos altura y anchura de la pantalla
anchura = oled.width
altura = oled.height
#creamos un objeto imagen sobre el cual vamos a dibujar usando PIL
image = Image.new('1', (anchura,altura))
draw = ImageDraw.Draw(image)
#inicializamos la pantalla
oled.begin()
#limpiamos la pantalla
oled.clear()
#.display es la funcion que mostrara los cambios a la pantalla
oled.display()
#escogemos una fuente, en este caso la predefinida
font = ImageFont.load_default()
#escribimos algo de texto
draw.text((0,0),'JEFREY RENE',font=font,fill=255)
draw.text((30,10),'HIPP MENDEZ',font=font,fill=255)
draw.text((00,20),'ESTA ES UNA PRUEBA',font=font,fill=255)
#mostramos la pantalla con ambos comandos
oled.image(image)
oled.display()
#esperamos 1 segundo
time.sleep(5)
draw.rectangle((0,0,anchura,altura), outline=0, fill=0)
#mostramos la pantalla con ambos comandos
oled.display()
#Mas texto
draw.text((0,0),'Felicidades, lo has',font=font,fill=255)
draw.text((30,10),'Hecho',font=font,fill=255)
draw.text((00,20),'Muy bien :3 ',font=font,fill=255)
#mostramos la pantalla con ambos comandos
oled.image(image)
oled.display()