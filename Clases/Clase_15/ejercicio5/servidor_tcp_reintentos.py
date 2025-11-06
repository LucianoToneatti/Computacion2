####EJERCICIO 5

# servidor_tcp_reintentos.py
import socket

HOST, PORT = "127.0.0.1", 9004

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        print(f"Servidor TCP en {HOST}:{PORT}")
        while True:  # secuencial, atiende de a uno
            conn, addr = s.accept()
            with conn:
                print(f"Conexión desde {addr}")
                data = conn.recv(1024)
                if data.strip() == b"ping":
                    conn.sendall(b"pong\n")
                else:
                    conn.sendall(b"echo: " + data)

if __name__ == "__main__":
    main()


### Servidor (profe) nc -l 127.0.0.1 9004. No responde solo; cuando veas ping en la terminal, escribír pong y Enter.

### Servidor (mio) responde automáticamente: si recibe ping, devuelve pong\n. Sigue siendo secuencial (bucle accept() atendiendo de a un cliente).