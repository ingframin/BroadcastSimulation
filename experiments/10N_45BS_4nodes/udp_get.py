import socket

def receive_udp(sock):
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
            break
            
        if len(lg)>20:
            with open('res-udp.txt','a') as log:
                for l in lg:
                    print(l,file=log)
            lg = []
    with open('res-udp.txt','a') as log:
        for l in lg:
            print(l,file=log)


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 8000))
sock.setblocking(False)
sock.settimeout(2.0)

receive_udp(sock)
