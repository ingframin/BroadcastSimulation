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
from datetime import datetime



def read_ssid(wi,n):

    global running
    global msg_counter
    
    lg = []
    seq = 0
    while running:
        timestamp = str(datetime.now()).split()[1]
        s = wi.readline()
        
        ssid = ("%d-%d"%(n,seq)+'*')
        if b'>' in s:
            wi.write(ssid.encode())
            seq += 1
            lg.append((str(datetime.now()).split()[1],s,'sent:'+ssid))
        else:
            lg.append((str(datetime.now()).split()[1],s,''))
            if b'D1' in s or b'D2' in s:
                msg_counter+=1
        
        if len(lg)> 1000:
            with open('res-%dMps.txt'%n,'a') as log:
                for l in lg:
                    print(l,file=log)
            lg = []
            
            

    with open('res-%dMps.txt'%n,'a') as log:
        for l in lg:
            print(l,file=log)



    
'''test script'''
if __name__=='__main__':

    global running
    global msg_counter
    msg_counter = 0
    running = True

    wifi5 = Serial("COM36",115200,xonxoff = True)

    tr5 = Thread(target=read_ssid,args=(wifi5,12))
    

    tr5.start()
    
    start = perf_counter()
    while running:
       try:
           if msg_counter > 1e5:
               running = False
           print(msg_counter)
           print(perf_counter()-start)
           sleep(1)
       except:
           print('out')
           running = False


    tr5.join()


