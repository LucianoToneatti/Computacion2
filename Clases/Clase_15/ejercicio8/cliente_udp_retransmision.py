#####CLIENTE######


import socket

HOST, PORT = "127.0.0.1", 9007

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.settimeout(2.0)
    retries = 10
    for i in range(1, retries + 1):
        try:
            s.sendto(b"TIME", (HOST, PORT))
            data, _ = s.recvfrom(2048)
            print("Respuesta:", data.decode())
            break
        except socket.timeout:
            print(f"Timeout intento {i}; reintentando...")
    else:
        print("Sin respuesta tras reintentos")


### Configura settimeout(1.0) y reintenta hasta 3 veces si no llega respuesta. Envía "TIME" y espera.