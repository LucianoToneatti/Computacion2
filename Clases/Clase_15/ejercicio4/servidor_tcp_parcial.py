####EJERCICIO 4

# servidor_tcp_parcial.py
import socket

HOST, PORT = "127.0.0.1", 9003

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        print(f"Servidor TCP escuchando en {HOST}:{PORT}")
        conn, addr = s.accept()
        with conn:
            print(f"Conexión desde {addr}")
            with open("archivo_grande.bin", "rb") as f:
                while chunk := f.read(64 * 1024):
                    conn.sendall(chunk)
            print("Archivo enviado.")

if __name__ == "__main__":
    main()


### Servidor (netcat del profe): nc -l 127.0.0.1 9003 < archivo_grande.bin

### Servidor (mio) Hace lo mismo que nc, pero leyendo el archivo y enviándolo por sendall en chunks. Es secuencial: atiende una conexión por vez.