import logging
from aiohttp import web

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


def create_app() -> web.Application:
    app = web.Application()
    app.router.add_get("/health", handle_health)
    return app


if __name__ == "__main__":
    print("🚀 Servidor A (Asyncio) iniciando en http://0.0.0.0:8080")
    logger.info("Servidor A (Asyncio) iniciando en http://0.0.0.0:8080")
    web.run_app(create_app(), host="0.0.0.0", port=8080)