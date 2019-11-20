from timestamp import *
from serial import Serial

def decode_GPGGA(sentence):
    ss = sentence.split(b',')
    c = {}
    try:

        ts = TimeStamp(ss[1][0:2].decode()+':'+ss[1][2:4].decode()+':'+ss[1][4:].decode())
    
        c['T'] = ts
    except:
        return None
    try:
        lat_deg = float(ss[2][0:2].decode())+(float(ss[2][2:].decode())/60.0)
        if b'S' in ss[3]:
            lat_deg *= -1
        c['Lat'] = lat_deg
    except:
        return None
    try:
        lon_deg = float(ss[4][0:3].decode())+(float(ss[4][3:].decode())/60.0)
        if b'W' in ss[5]:
            lon_deg *= -1
        c['Lon'] = lon_deg
    except:
        return None

    try:
        hdop = float(ss[8].decode())
        
        c['HDOP'] = hdop
    except:
        return None

    try:
        h_sea = float(ss[9].decode())
        
        c['Altitude_Sea'] = h_sea
    except:
        return None

    try:
        h_WGS84 = float(ss[11].decode())
        
        c['Altitude_WGS84'] = h_WGS84
    except:
        return None
    
    return c

   

    



if __name__=='__main__':
    gps = Serial("/dev/tty.SLAB_USBtoUART22",9600)
    while True:
        coords = gps.readline()
            
        if b'GPGGA' in coords:
            print(decode_GPGGA(coords))
