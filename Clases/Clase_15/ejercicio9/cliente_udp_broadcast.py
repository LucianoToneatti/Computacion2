import socket

PORT = 9008
BROADCAST = ("255.255.255.255", PORT)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.settimeout(15.0)
    s.sendto(b"DISCOVER?", BROADCAST)
    try:
        data, addr = s.recvfrom(4096)
        print(f"{addr} -> {data!r}")
    except socket.timeout:
        print("Nadie respondió al broadcast (o la red lo filtra)")



        ##### Escuchar en todas las interfaces
#############    nc -u -l 0.0.0.0 9008


#### servidor nc -u -l -p 9008
