# -*- coding: utf-8 -*-
from time import sleep, perf_counter
from serial import Serial
from threading import Thread
from datetime import datetime

def tx_data(filename,wifi):
    with open('data.bin','rb') as df:
        data = df.read()
        i = 0
        while i< len(data):
            s = wifi.readline()
            if b'=' in s:
                wifi.write(data[i])
                i+=1
        
        sleep(10)        
        
        running = False
        
def rx_data(filename,wifi):
    buffer = []
    global running
    while running:
        s = wifi.readline()
        if b'byte:' in s:
            ls = s.split(b':')
            buffer.append(ls[1].strip()[0])
        

if __name__=='__main__':

    global running
    running = True
    wifi1 = Serial("COM36",115200,xonxoff = True)
    wifi2 = Serial("COM38",115200,xonxoff = True)
    
    tr1 = Thread(target=tx_data,args=('data.bin',wifi1))
    tr2 = Thread(target=rx_data,args=('rx_data.bin',wifi2))

    
    tr1.start()
    tr2.start()

    start = perf_counter()
    while running:
       try:
           print(perf_counter()-start)
           sleep(1)
           if perf_counter() - start > 7200:
               running = False

       except:
           print('out')
           running = False

    tr1.join()
    tr2.join()