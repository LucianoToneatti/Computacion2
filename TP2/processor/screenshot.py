"""Captura screenshots con Playwright"""

import logging
import base64
from typing import Optional

from playwright.sync_api import sync_playwright

logger = logging.getLogger("processor.screenshot")


def take_screenshot(url: str, timeout: int = 30000) -> str:
    """
    Navega a `url` en modo headless usando Playwright, captura un screenshot (full page)
    y devuelve la imagen codificada en Base64 como string.
    En caso de error retorna cadena vacía y registra la excepción.
    Nota: requiere que Playwright y los navegadores estén instalados (playwright install).
    """
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=timeout)
            # Capturar full page; devuelve bytes
            img_bytes = page.screenshot(full_page=True)
            browser.close()
        return base64.b64encode(img_bytes).decode("ascii")
    except Exception as e:
        logger.exception("take_screenshot: fallo al capturar %s: %s", url, e)
        return ""
