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
import sys

drones = []


def read_ssid(wi,n):
    c = 0
    start = perf_counter()
    log = []
    fc = 0
 
    while True:
        try:
            s = wi.readline()        
            #print(s)
            if b'>' in s:
                ssid = ("%d-"%n +str(c)+'*').encode()
                wi.write(ssid)
                t = (perf_counter()-start,'count=%d'%c,n)
                print(t)
                log.append(t)
                c+=1
            else:
                t = (perf_counter()-start,s.decode("utf-8")[:-1],n)
                log.append(t)
                print(t)
            if len(log)>10000:
                with open('log-%d-%d.txt'%(fc,n),'w') as f:
                    for l in log:
                        print(l,file=f)
                fc +=1
                        
        except KeyboardInterrupt:
            with open('log-%d-%d.txt'%(fc,n),'w') as f:
                for l in log:
                    print(l,file=f)
                fc +=1
            return
            
        except Exception as e:
            print("Error on node%d"%n+str(e))
            log.append(e)
            with open('log-%d-%d.txt'%(fc,n),'w') as f:
                for l in log:
                    print(l,file=f)
                fc +=1
            
                
'''test script'''
if __name__=='__main__':

    wifi1 = Serial(sys.argv[1],230400, timeout = 10)
    

    read_ssid(wifi1,sys.argv[2])


