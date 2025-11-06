####EJERCICIO 7

# servidor_udp_pingpong.py
import socket

HOST, PORT = "127.0.0.1", 9006

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, PORT))
        print(f"Servidor UDP escuchando en {HOST}:{PORT}")
        while True:  # secuencial
            data, addr = s.recvfrom(2048)
            print(f"Recibido {data!r} de {addr}")
            if data == b"ping":
                s.sendto(b"pong", addr)
            else:
                s.sendto(b"echo: " + data, addr)

if __name__ == "__main__":
    main()

### Servidor (profe) nc -u -l 127.0.0.1 9006. Cuando aparezca ping, escribí pong y Enter para responder.

### Servidor (mio) al recibir ping, responde pong con sendto. Procesa un datagrama por vez (secuencial).