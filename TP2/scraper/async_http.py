"""Cliente HTTP asíncrono con aiohttp"""

import logging
import asyncio
from typing import Optional

import aiohttp

logger = logging.getLogger("scraper.async_http")


async def fetch_page(session: aiohttp.ClientSession, url: str) -> Optional[str]:
    """
    Realiza un GET a `url` con timeout de 30 segundos usando la sesión proporcionada.
    Devuelve el contenido (texto) en caso de éxito, o None si ocurre ClientError o TimeoutError.
    """
    try:
        timeout = aiohttp.ClientTimeout(total=30)
        async with session.get(url, timeout=timeout) as resp:
            resp.raise_for_status()
            return await resp.text()
    except aiohttp.ClientError as e:
        logger.exception("ClientError al obtener %s: %s", url, e)
    except asyncio.TimeoutError:
        logger.warning("Timeout al obtener %s", url)
    return None
