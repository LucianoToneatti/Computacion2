import logging
from aiohttp import web
import asyncio
import aiohttp
import struct
import argparse
from scraper.async_http import fetch_page
from scraper.html_parser import parse_html_full
from common.protocol import pack_message
from common.serialization import deserialize_data
import datetime

# Logging setup (to console and file)
logger = logging.getLogger("server_a")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S")

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
file_handler = logging.FileHandler("server_a.log")
file_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)


async def handle_health(request: web.Request) -> web.Response:
    """GET /health -> {"status": "ok", "server": "A - Asyncio"}"""
    logger.info("Received /health request")
    return web.json_response({"status": "ok", "server": "A - Asyncio"})


async def handle_scrape(request: web.Request) -> web.Response:
    """
    GET /scrape?url=<...>
    Lee el parámetro 'url' de la query string, usa app['http_session'] para obtener la página,
    parsea el HTML con parse_html_full y devuelve el diccionario resultante como JSON.
    Además envía el resultado al servidor de procesamiento B y combina ambas respuestas.
    """
    url = request.query.get("url")
    if not url:
        logger.warning("handle_scrape: falta el parámetro 'url'")
        return web.json_response(
            {"error": "missing 'url' parameter", "message": "El parámetro 'url' es obligatorio"},
            status=400,
        )

    logger.info(f"handle_scrape: petición de scrape para url={url}")

    session = request.app.get("http_session")
    if not session:
        logger.error("handle_scrape: http_session no disponible")
        return web.json_response({"error": "server not ready"}, status=503)

    # Obtener el contenido de la página
    content = await fetch_page(session, url)
    if content is None:
        logger.warning("handle_scrape: fallo al obtener el contenido de %s", url)
        return web.json_response({"error": "failed to fetch url"}, status=502)

    # Parsear el HTML (usar base_url para resolver relativos)
    parsed = parse_html_full(content, url)

    # Enviar resultado al servidor de procesamiento B y combinar respuestas
    processing_result = {}
    try:
        payload = {"type": "scrape_result", "url": url, "scrape": parsed}
        processing_result = await call_processing_server(payload)
    except Exception as e:
        logger.exception("handle_scrape: fallo al llamar a server B: %s", e)
        processing_result = {"error": "processing_call_failed", "detail": str(e)}

    # Formato de respuesta requerido
    resp = {
        "url": url,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "status": "success",
        "scraping_data": parsed,
        "processing_data": processing_result,
    }
    return web.json_response(resp)


async def call_processing_server(data_to_send: dict, host: str = "127.0.0.1", port: int = 9090) -> dict:
    """
    Conecta por TCP al servidor de procesamiento (host:port), empaqueta y envía
    data_to_send usando pack_message, lee la respuesta (header+payload),
    deserializa y devuelve el dict resultante.

    Asegura el cierre del writer en finally.
    """
    logger.info("call_processing_server: conectando a %s:%d", host, port)
    try:
        reader, writer = await asyncio.open_connection(host, port)
    except Exception as e:
        logger.exception("call_processing_server: error al conectar a %s:%d -> %s", host, port, e)
        return {"error": "connect_failed", "detail": str(e)}

    try:
        # Empaquetar y enviar
        msg = pack_message(data_to_send)
        writer.write(msg)
        await writer.drain()

        # Leer header (4 bytes) y payload exacto
        header = await reader.readexactly(4)
        length = struct.unpack("!I", header)[0]
        logger.info("call_processing_server: esperando %d bytes de respuesta", length)
        payload = await reader.readexactly(length)

        # Deserializar respuesta
        try:
            resp_obj = deserialize_data(payload)
            return resp_obj
        except Exception as e:
            logger.exception("call_processing_server: error deserializando respuesta: %s", e)
            return {"error": "invalid_response", "detail": str(e)}
    finally:
        try:
            writer.close()
            await writer.wait_closed()
        except Exception:
            pass


async def on_startup(app: web.Application) -> None:
    logger.info("on_startup: creando aiohttp ClientSession")
    app["http_session"] = aiohttp.ClientSession()


async def on_cleanup(app: web.Application) -> None:
    session = app.get("http_session")
    if session:
        logger.info("on_cleanup: cerrando aiohttp ClientSession")
        await session.close()
        app.pop("http_session", None)


def create_app() -> web.Application:
    app = web.Application()
    app.router.add_get("/health", handle_health)
    app.router.add_get("/scrape", handle_scrape)
    app.on_startup.append(on_startup)
    app.on_cleanup.append(on_cleanup)
    return app


async def _run_app(host: str = "::", port: int = 8080) -> None:
    app = create_app()
    runner = web.AppRunner(app)
    await runner.setup()

    # Crear TCPSite usando los parámetros host/port recibidos
    site = web.TCPSite(runner, host, port)

    try:
        await site.start()
        logger.info("Servidor A escuchando en %s:%d", host, port)
        print(f"🚀 Servidor A (Asyncio) iniciando en http://{host}:{port}")
    except Exception as e:
        logger.exception("No se pudo iniciar TCPSite en %s:%d -> %s", host, port, e)
        # Si el host es '::' intentamos enlazar también en 0.0.0.0 por compatibilidad
        if host == "::":
            try:
                site4 = web.TCPSite(runner, "0.0.0.0", port)
                await site4.start()
                logger.info("Servidor A escuchando en 0.0.0.0:%d como fallback", port)
                print(f"🚀 Servidor A (Asyncio) iniciando en http://0.0.0.0:{port}")
            except Exception as e2:
                logger.exception("Fallback IPv4 falló: %s", e2)
                raise

    # Mantener el servidor en ejecución hasta interrupción
    try:
        await asyncio.Event().wait()
    finally:
        await runner.cleanup()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Servidor A - scraping async")
    parser.add_argument("-i", "--host", default="::", help="host a bindear (default '::')")
    parser.add_argument("-p", "--port", type=int, default=8080, help="puerto (default 8080)")
    args = parser.parse_args()

    try:
        asyncio.run(_run_app(args.host, args.port))
    except Exception as e:
        logger.exception("Error arrancando la app: %s", e)