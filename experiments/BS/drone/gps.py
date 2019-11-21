from timestamp import *
from serial import Serial

def decode_GPGGA(sentence):
    ss = sentence.split(b',')
    c = {}
    if b'GPGGA' not in sentence:
        print('no gpgga')
        return
    try:

        ts = TimeStamp(stamp=ss[1][0:2].decode()+':'+ss[1][2:4].decode()+':'+ss[1][4:].decode())
    
        c['T'] = ts
    except:
        print('T')
        return
    try:
        lat_deg = float(ss[2][0:2].decode())+(float(ss[2][2:].decode())/60.0)
        if b'S' in ss[3]:
            lat_deg *= -1
        c['Lat'] = lat_deg
    except:
        print('lat')
        return
    try:
        lon_deg = float(ss[4][0:3].decode())+(float(ss[4][3:].decode())/60.0)
        if b'W' in ss[5]:
            lon_deg *= -1
        c['Lon'] = lon_deg
    except:
        print('lon')
        return

    try:
        hdop = float(ss[8].decode())
        
        c['HDOP'] = hdop
    except:
        print('HDOP')
        return
    try:
        h_sea = float(ss[9].decode())
        
        c['Altitude_Sea'] = h_sea
    except:
        print('hsea')
        return

    try:
        h_WGS84 = float(ss[11].decode())
        
        c['Altitude_WGS84'] = h_WGS84
    except:
        print('h_WGS84')
        return
    print(c)
    return c

   

    



if __name__=='__main__':
    gps = Serial("/dev/tty.SLAB_USBtoUART22",9600)
    while True:
        coords = gps.readline()
            
        if b'GPGGA' in coords:
            print(decode_GPGGA(coords))
