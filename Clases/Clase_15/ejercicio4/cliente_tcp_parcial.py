#####CLIENTE######

import socket

def recv_all(sock):
    
    chunks = []
    while True:
        b = sock.recv(64 * 1024)  # 64 KiB por iteración
        if not b:
            break
        chunks.append(b)
    return b"".join(chunks)

def main():
    HOST, PORT = "127.0.0.1", 9003
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        data = recv_all(s)
        print(f"Recibidos {len(data)} bytes")

if __name__ == "__main__":
    main()

### Se conecta y lee en bucle con recv(64*1024) hasta que el servidor cierra 
###  la conexión (recv devuelve b''). Une los fragmentos y te dice cuántos bytes 
###  recibió. Es la manera correcta de recibir archivos o streams largos (no asumir que recv trae “todo de una”).