import sys
import threading
import time
from threading import Thread

EMULATE_HX711=False

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711



def celda1():
    hx = HX711(27, 22) # sck, dout
    hx.set_reading_format("MSB", "MSB")
    hx.set_reference_unit(-130)
    hx.reset()
    hx.tare()

    print "Tare done! Add weight now..." 

    while True:
        try:

            val = hx.get_weight(1)
            print("celda1 : {}".format(val))  
            hx.power_down()
            hx.power_up()
            time.sleep(0.000001)

        except (KeyboardInterrupt, SystemExit):
            cleanAndExit()

def celda2():
    hx = HX711(5, 6) # sck, dout
    hx.set_reading_format("MSB", "MSB")
    hx.set_reference_unit(-131)
    hx.reset()
    hx.tare()

    print "Tare done! Add weight now..." 

    while True:
        try:

            val = hx.get_weight(5)
            print("celda2 : {}".format(val))  
            hx.power_down()
            hx.power_up()
            time.sleep(0.000001)

        except (KeyboardInterrupt, SystemExit):
            cleanAndExit()

def cleanAndExit():
    print "Cleaning..." 

    if not EMULATE_HX711:
        GPIO.cleanup()
        
    print("Bye!")
    sys.exit()


if __name__ == "__main__":

    t1 = Thread(target = celda1)
    t2 = Thread(target = celda2)
    #t3 = Thread(target = cleanAndExit)

    t1.setDaemon(True)
    t2.setDaemon(True)
    #t3.setDaemon(True)

    t1.start()
    t2.start()
    #t3.start()

    while True:
        pass
