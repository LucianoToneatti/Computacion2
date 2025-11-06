import logging
import socketserver
import multiprocessing

# Logging setup (to console and file)
logger = logging.getLogger("server_b")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S")

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
file_handler = logging.FileHandler("server_b.log")
file_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)


class EchoHandler(socketserver.BaseRequestHandler):
    """Handler que hace echo de los datos recibidos."""
    def handle(self):
        addr = self.client_address
        logger.info(f"Conexión entrante desde {addr}")
        try:
            while True:
                data = self.request.recv(4096)
                if not data:
                    break
                logger.info(f"Recibido {len(data)} bytes de {addr}")
                self.request.sendall(data)
        except Exception as e:
            logger.exception(f"Error en handler para {addr}: {e}")
        finally:
            logger.info(f"Conexión cerrada {addr}")


def run_server(host="0.0.0.0", port=9090):
    num_workers = multiprocessing.cpu_count()
    print(f"🚀 Servidor B (Multiprocessing) iniciando en {host}:{port}")
    logger.info(f"Servidor B (Multiprocessing) iniciando en {host}:{port} - CPU workers disponibles: {num_workers}")

    # Crear un pool para demostrar uso de multiprocessing (no usado directamente aquí)
    pool = multiprocessing.Pool(processes=num_workers)

    socketserver.ThreadingTCPServer.allow_reuse_address = True
    server = socketserver.ThreadingTCPServer((host, port), EchoHandler)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt recibido, apagando servidor B...")
    finally:
        server.shutdown()
        server.server_close()
        pool.terminate()
        pool.join()
        logger.info("Servidor B detenido.")


if __name__ == "__main__":
    run_server()