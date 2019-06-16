
import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
    
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

#Raspberry Pi pin configuration:
RST =   24   # on the PiOLED this pin isnt used
#Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# 128x64 display with hardware SPI:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

#Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

#Create blank image for drawing.
#Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

#Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

#Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

#Draw some shapes.
#First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
#Move left to right keeping track of the current x position for drawing shapes.
x = 0

#Load default font.
font = ImageFont.load_default()

#Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
#Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype('Montserrat-Light.ttf', 12)
font2 = ImageFont.truetype('fontawesome-webfont.ttf', 14)
font_icon_big = ImageFont.truetype('fontawesome-webfont.ttf', 20)
font_text_big = ImageFont.truetype('Montserrat-Medium.ttf', 19)

while True:

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname -I | cut -d\' \' -f1 | head --bytes -1"
    IP = subprocess.check_output(cmd, shell = True )
    cmd = "top -bn1 | grep load | awk '{printf \"%.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell = True )
    cmd = "free -m | awk 'NR==2{printf \"MEM: %.2f%%\", $3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell = True )
    cmd = "df -h | awk '$NF==\"/\"{printf \"HDD: %d/%dGB %s\", $3,$2,$5}'"
    cmd = "df -h | awk '$NF==\"/\"{printf \"%s\", $5}'"
    Disk = subprocess.check_output(cmd, shell = True )
    cmd = "vcgencmd measure_temp | cut -d '=' -f 2 | head --bytes -1"
    Temperature = subprocess.check_output(cmd, shell = True )

    # Icons
    draw.text((x, top),       unichr(61931),  font=font2, fill=255)
    draw.text((x+50, top+52), unichr(61888),  font=font2, fill=255)
    draw.text((x, top+52),    unichr(62152),  font=font2, fill=255)
    draw.text((x, top+15),    unichr(62171),  font=font_icon_big, fill=255)
    
    draw.text((18, top),      str(IP),  font=font, fill=255)
    draw.text((x+22, top+12), str(CPU), font=font_text_big, fill=255)
    draw.text((x, top+36),    str(MemUsage),  font=font, fill=255)
    #draw.text((x, top+39),   str(Disk),  font=font, fill=255)
    draw.text((x+66, top+52), str(Disk),  font=font, fill=255)
    draw.text((x+10, top+52), str(Temperature),  font=font, fill=255)
    


    # Display image.
    disp.image(image)
    disp.display()
    time.sleep(5)
