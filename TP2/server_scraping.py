import logging
from aiohttp import web
import asyncio

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
    Lee el parámetro 'url' de la query string y devuelve un JSON confirmando recepción.
    """
    url = request.query.get("url")
    if not url:
        logger.warning("handle_scrape: falta el parámetro 'url'")
        return web.json_response({"error": "missing 'url' parameter"}, status=400)

    logger.info(f"handle_scrape: petición de scrape para url={url}")
    # Aquí se encolaría el trabajo de scraping; de momento devolvemos eco/confirmación.
    return web.json_response({"status": "queued", "url": url, "server": "A - Asyncio"})


def create_app() -> web.Application:
    app = web.Application()
    app.router.add_get("/health", handle_health)
    app.router.add_get("/scrape", handle_scrape)
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