import threading
import time
from threading import Thread

import serial
import RPi.GPIO as GPIO
import math
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

GPIO.setmode(GPIO.BCM)
mensaje = ' :) :) :) :)'

def OLED():
    global mensaje

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
    text = mensaje
    maxwidth, unused = draw.textsize(text, font=font)
    amplitude = height/4
    offset = height/2 - 4
    velocity = -2
    startpos = width
    print('Press Ctrl-C to quit.')
    pos = startpos

    while True: 

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

def BLUETOOTH():
    global mensaje

    port = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=3.0)
    while True:
        port.write('\r\n{}'.format(mensaje))
        time.sleep(1)

def STEPPER1():
   
    #pines = [7,11,13,15]
    pines = [4,17,27,22]

    for pin in pines: 
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)

    secuencia = [ [1,0,0,0], [1,1,0,0], [0,1,0,0], [0,1,1,0], [0,0,1,0], [0,0,1,1], [0,0,0,1], [1,0,0,1] ]

    #for i in range (2048): 
    while True:
        for seq in range (8):
            for pin in range (4):
                GPIO.output(pines[pin], secuencia[seq][pin])
            time.sleep(0.001)

    GPIO.cleanup()

def STEPPER2():
   
    pines = [5,6,13,19]

    for pin in pines: 
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)

    secuencia = [ [1,0,0,0], [1,1,0,0], [0,1,0,0], [0,1,1,0], [0,0,1,0], [0,0,1,1], [0,0,0,1], [1,0,0,1] ]
    #for i in range (2048): 
    while True:
        for seq in range (8):
            for pin in range (4):
                GPIO.output(pines[pin], secuencia[seq][pin])
            time.sleep(0.001)

    GPIO.cleanup()

if __name__ == "__main__":

    t1 = Thread(target = OLED)
    t2 = Thread(target = BLUETOOTH)
    t3 = Thread(target = STEPPER1)
    t4 = Thread(target = STEPPER2)

    t1.setDaemon(True)
    t2.setDaemon(True)
    t3.setDaemon(True)
    t4.setDaemon(True)

    t1.start()
    t2.start()
    t3.start()
    t4.start()

    while True:
        pass