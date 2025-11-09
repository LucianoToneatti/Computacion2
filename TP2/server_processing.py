import logging
import socketserver
import multiprocessing
import struct
from common.serialization import deserialize_data, serialize_data
from processor.screenshot import take_screenshot

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
    """Handler que hace echo de los datos recibidos. (No usado por defecto)"""
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


class ProcessingTCPHandler(socketserver.BaseRequestHandler):
    """
    Handler que recibe un mensaje (header+payload), lo deserializa,
    y envía una respuesta mock.
    """

    def _read_exact(self, n: int) -> bytes:
        """Lee exactamente n bytes del socket o lanza ConnectionError si se cierra."""
        buf = bytearray()
        while len(buf) < n:
            chunk = self.request.recv(n - len(buf))
            if not chunk:
                raise ConnectionError("socket closed while reading")
            buf.extend(chunk)
        return bytes(buf)

    def _receive_message(self) -> bytes:
        """
        Lee un mensaje completo (header+payload) y devuelve el payload.
        Lanza ConnectionError o struct.error si falla.
        """
        # Leer header de 4 bytes
        header = self._read_exact(4)
        length = struct.unpack("!I", header)[0]
        logger.info("ProcessingTCPHandler: esperando %d bytes de payload...", length)

        # Leer payload completo
        payload = self._read_exact(length)
        return payload

    def _send_response(self, data: dict):
        """Serializa, empaqueta y envía una respuesta dict al cliente."""
        try:
            payload = serialize_data(data)
            header = struct.pack("!I", len(payload))
            self.request.sendall(header + payload)
        except Exception as e:
            logger.exception("ProcessingTCPHandler: fallo enviando respuesta a %s: %s", self.client_address, e)

    def handle(self):
        """Coordina la recepción, procesamiento y respuesta."""
        addr = self.client_address
        logger.info(f"ProcessingTCPHandler: conexión entrante desde {addr}")

        try:
            # --- 1. Recibir Mensaje ---
            payload = self._receive_message()

            # --- 2. Deserializar ---
            try:
                obj = deserialize_data(payload)
                logger.info("ProcessingTCPHandler: deserializado: %s", obj)
            except Exception as e:
                logger.exception("ProcessingTCPHandler: error deserializando payload: %s", e)
                # Enviar respuesta de error y terminar
                err_resp = {"status": "error", "message": "invalid payload"}
                self._send_response(err_resp)
                return

            # --- 3. Procesar (usar pool para tarea CPU-bound: screenshot) ---
            # Obtener el pool desde el servidor (puede ser None)
            pool = getattr(self.server, "pool", None)
            screenshot_b64 = ""
            try:
                url = obj.get("url") if isinstance(obj, dict) else None
                if not url:
                    raise ValueError("missing 'url' in payload")

                if pool:
                    # pool.apply es síncrono y bloqueará el thread handler hasta completar
                    screenshot_b64 = pool.apply(take_screenshot, args=(url,))
                else:
                    # fallback sin pool
                    screenshot_b64 = take_screenshot(url)

                response = {"status": "ok", "screenshot": screenshot_b64}
            except Exception as e:
                logger.exception("ProcessingTCPHandler: error en procesamiento: %s", e)
                response = {"status": "error", "message": "processing_failed", "detail": str(e)}

            self._send_response(response)
            logger.info("ProcessingTCPHandler: respuesta enviada a %s", addr)

        except ConnectionError as ce:
            logger.warning("ProcessingTCPHandler: conexión cerrada prematuramente por %s: %s", addr, ce)
        except Exception as e:
            logger.exception("Error en ProcessingTCPHandler para %s: %s", addr, e)
        finally:
            logger.info(f"ProcessingTCPHandler: conexión cerrada {addr}")


class PooledTCPServer(socketserver.ThreadingTCPServer):
    """ThreadingTCPServer que conserva un pool de procesos en self.pool."""
    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True, pool=None):
        super().__init__(server_address, RequestHandlerClass, bind_and_activate=bind_and_activate)
        self.pool = pool


def run_server(host="0.0.0.0", port=9090):
    num_workers = multiprocessing.cpu_count()
    print(f"🚀 Servidor B (Multiprocessing) iniciando en {host}:{port}")
    logger.info(f"Servidor B (Multiprocessing) iniciando en {host}:{port} - CPU workers disponibles: {num_workers}")

    # Crear un pool para demostrar uso de multiprocessing (usado por PooledTCPServer)
    pool = multiprocessing.Pool(processes=num_workers)

    socketserver.ThreadingTCPServer.allow_reuse_address = True
    server = PooledTCPServer((host, port), ProcessingTCPHandler, pool=pool)

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