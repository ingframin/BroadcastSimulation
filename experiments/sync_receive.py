from datetime import datetime
from threading import Thread
from serial import Serial
from time import sleep, perf_counter
import subprocess

def read_ssid(wi,n):

    start = perf_counter()
    
    global running
    lg = []
    while running:
        s = wi.readline()        
        print(s)
        timestamp = str(datetime.now()).split()[1]
        if b'>' in s:

            ssid = ("%d-"%n+timestamp+'*')
            wi.write(ssid.encode())
            lg.append('sent:'+ssid)
        if b'sync' in s:
            date = s.decode('utf-8').replace('*','').split('-')[1]
            o = subprocess.check_output('date +%T -s "%s"'%date,stderr=subprocess.STDOUT,shell=True)
            print(o)
        try:
            lg.append(timestamp+'\t'+s.decode("utf-8")[:-1])
        except:
            pass
        
        if len(lg)>200:
            with open('res-%d.txt'%n,'a') as log:
                for l in lg:
                    print(l,file=log)
            lg = []
            
    with open('res-%d.txt'%n,'a') as log:
        for l in lg:
            print(l,file=log)
            
        
if __name__=='__main__':

    global running
    running = True
    wifi1 = Serial("/dev/ttyUSB0",230400)

       
    tr1 = Thread(target=read_ssid,args=(wifi1,2))
  
    tr1.daemon = True
   
    tr1.start()
   

    start = perf_counter()
    while running:
       try:
           print(perf_counter()-start)
           sleep(1)
       except:
           print('out')
           
           running = False
    
    tr1.join()

