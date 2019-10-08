from serial import Serial

port = Serial("COM38",230400)

while True:
    p = port.readline()
    if b'rssi' in p:
        print(p)
