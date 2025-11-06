####EJERCICIO 8

# servidor_udp_retransmision.py
import socket
import time

HOST, PORT = "127.0.0.1", 9007

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, PORT))
        print(f"Servidor UDP en {HOST}:{PORT}")
        while True:  # atiende de a un datagrama por vez
            data, addr = s.recvfrom(2048)
            print(f"Recibido {data!r} de {addr}")
            if data.strip() == b"TIME":
                now = time.ctime().encode()
                s.sendto(now, addr)

if __name__ == "__main__":
    main()


### Servidor (profe) nc -u -l 127.0.0.1 9007. Cuando ves TIME, escribís una respuesta (por ejemplo, 12:34:56) y Enter.

### Servidor (mio) si recibe TIME, responde con un timestamp (time.ctime()).