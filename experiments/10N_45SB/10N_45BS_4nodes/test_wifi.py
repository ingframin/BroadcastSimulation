# -*- coding: utf-8 -*-
'''
License:
© Copyright 2018, Networked Systems group, ESAT-TELEMIC,KU Leuven.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.
3. All advertising materials mentioning features or use of this software
   must display the following acknowledgement:
   This product includes software developed by Networked Systems group,
   ESAT-TELEMIC,KU Leuven.
4. Neither the name of the Networked Systems group, ESAT-TELEMIC,KU Leuven nor the
   names of its contributors may be used to endorse or promote products
   derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY ESAT-TELEMIC-KU Leuven, ''AS IS'' AND ANY
EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL Networked Systems group, ESAT-TELEMIC,KU Leuven
BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
THE POSSIBILITY OF SUCH DAMAGE.
'''

from time import sleep, perf_counter
from serial import Serial
from threading import Thread
import socket
from logger import Logger


drones = []


def read_ssid(wi,n,logger):
    c = 0
    start = perf_counter()
    
    global running
    
    id = 0
    while running:
        try:
            s = wi.readline()        
            #print(s)
            if b'>' in s:
                ssid = ("%d-"%n +str(c)+'*').encode()
                wi.write(ssid)
                t = (perf_counter()-start,'count=%d'%c,n)
                print(t)
                logger.log_one(t,'scans')
                c+=1
            else:
                t = (perf_counter()-start,s.decode("utf-8")[:-1],n)
                print(t)
                logger.log_one(t,'scans')
        except:
            pass
        
            
            
 
def receive_udp(sock):
    t = current_thread()
    lg = []
    start = perf_counter()
    global running
    while running:
            
        try:
            data, addr = sock.recvfrom(256)
            print((addr,data))
            lg.append((str(perf_counter()-start),addr,data))
            sock.sendto("Message received".encode(), (addr, 8000))
        except:
            sleep(0.1)
            
        if len(lg)>20:
            with open('res-udp.txt','a') as log:
                for l in lg:
                    print(l,file=log)
            log = []
    with open('res-udp.txt','a') as log:
        for l in lg:
            print(l,file=log)
       



'''test script'''
if __name__=='__main__':

    global running
    running = True
    wifi1 = Serial("/dev/ttyUSB0",230400)
    wifi2 = Serial("/dev/ttyUSB1",230400)
    wifi3 = Serial("/dev/ttyUSB2",230400)
    wifi4 = Serial("/dev/ttyUSB3",230400)
    logger = Logger('scan_broadcast_log.db','sb_schema.sql')
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', 8000))
    sock.setblocking(False)
    sock.settimeout(2.0)
    
    tr1 = Thread(target=read_ssid,args=(wifi1,1,logger))
    tr2 = Thread(target=read_ssid,args=(wifi2,2,logger))
    tr3 = Thread(target=read_ssid,args=(wifi1,1,logger))
    tr4 = Thread(target=read_ssid,args=(wifi2,2,logger))
    tr_udp = Thread(target=receive_udp,args=(sock,))
    
    tr1.start()
    tr2.start()
    tr3.start()
    tr4.start()
    tr_udp.start()
    start = perf_counter()
    while running:
       try:
           print(perf_counter()-start)
           sleep(1)
       except:
           print('out')
           
           running = False
    
    tr1.join()
    tr2.join()
    tr3.join()
    tr4.join()
