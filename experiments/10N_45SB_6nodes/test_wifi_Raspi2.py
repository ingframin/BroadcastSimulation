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

drones = []


def read_ssid(wi,n):
    c = 0
    start = perf_counter()
    
    global running
    lg = []
    while running:
        s = wi.readline()        
        print(s)
        if b'>' in s:
            ssid = ("%d-"%n +str(c)+'*').encode()
            wi.write(ssid)
            lg.append('count=%d'%c)
            c+=1
        else:
            try:
                lg.append(str(perf_counter()-start)+'\t'+s.decode("utf-8")[:-1])
            except:
                with open('res-%d.txt'%n,'a') as log:
                    for l in lg:
                        print(l,file=log)
            lg = []
        
        if len(lg)>50:
            with open('res-%d.txt'%n,'a') as log:
                for l in lg:
                    print(l,file=log)
            lg = []
            
    with open('res-%d.txt'%n,'a') as log:
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
#    wifi5 = Serial("/dev/ttyUSB5",230400)
#    wifi6 = Serial("/dev/ttyUSB6",230400)
   # udp_rec = Serial("/dev/ttyUSB0",115200)
    
  #  tr0 = Thread(target=read_udp,args=(udp_rec,))
    tr1 = Thread(target=read_ssid,args=(wifi1,3))
    tr2 = Thread(target=read_ssid,args=(wifi2,4))
    tr3 = Thread(target=read_ssid,args=(wifi3,5))
    tr4 = Thread(target=read_ssid,args=(wifi4,6))
 #   tr5 = Thread(target=read_ssid,args=(wifi5,5))
 #   tr6 = Thread(target=read_ssid,args=(wifi6,6))
    
    tr1.daemon = True
    tr2.daemon = True
    tr3.daemon = True
    tr4.daemon = True
 #   tr5.daemon = True
 #   tr6.daemon = True
    
  #  tr0.start()
    tr1.start()
    tr2.start()
    tr3.start()
    tr4.start()
  #  tr5.start()
  #  tr6.start()
    
    start = perf_counter()
    while running:
       try:
           print(perf_counter()-start)
           sleep(1)
       except:
           print('out')
           
           running = False
    
   # tr0.join()
    tr1.join()
    tr2.join()
    tr3.join()
    tr4.join()
   # tr5.join()
   # tr6.join()

