import logging
from aiohttp import web
import asyncio
import aiohttp
from scraper.async_http import fetch_page
from scraper.html_parser import parse_html_full

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
    parsea el HTML con parse_html_basic y devuelve el diccionario resultante como JSON.
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

    # Parsear el HTML y devolver el resultado del parser como JSON
    parsed = parse_html_full(content)
    return web.json_response(parsed)


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


async def _run_app() -> None:
    app = create_app()
    runner = web.AppRunner(app)
    await runner.setup()

    # Intentamos enlazar en IPv4 e IPv6; IPv6 puede fallar en algunos entornos.
    site4 = web.TCPSite(runner, "0.0.0.0", 8080)
    site6 = web.TCPSite(runner, "::", 8080)

    await site4.start()
    try:
        await site6.start()
        logger.info("Servidor A escuchando en IPv4 y IPv6 en el puerto 8080")
    except Exception as e:
        # Si falla el bind IPv6, seguimos con IPv4
        logger.warning(f"No se pudo enlazar IPv6 (::) - continuando solo con IPv4: {e}")

    print("🚀 Servidor A (Asyncio) iniciando en http://0.0.0.0:8080")
    logger.info("Servidor A (Asyncio) iniciando en http://0.0.0.0:8080")

    # Mantener el servidor en ejecución hasta interrupción
    try:
        await asyncio.Event().wait()
    finally:
        await runner.cleanup()


if __name__ == "__main__":
    asyncio.run(_run_app())