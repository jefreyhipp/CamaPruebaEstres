import threading

def runA():
    while True:
        print('A')

def runB():
    while True:
        print('B')

# This works!
t1 = threading.Thread(target=runA)
t2 = threading.Thread(target=runB)

t1.start()
t2.start()