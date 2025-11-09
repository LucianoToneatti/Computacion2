"""Análisis de rendimiento web"""

import logging
from typing import Dict

from playwright.sync_api import sync_playwright

logger = logging.getLogger("processor.performance")


def analyze_performance(url: str, timeout: int = 30000) -> Dict[str, int]:
    """
    Usa Playwright (sync) para navegar a `url`, extraer window.performance.timing
    y devolver un diccionario con los valores (enteros) y algunas métricas derivadas.
    En caso de error devuelve dict vacío y registra la excepción.
    """
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=timeout)
            page.wait_for_load_state("load", timeout=timeout)

            # Extraer objeto performance.timing como un POJO
            perf = page.evaluate(
                """() => {
                    const t = window.performance.timing || {};
                    const out = {};
                    for (const k in t) {
                        try { out[k] = t[k]; } catch (e) { out[k] = null; }
                    }
                    return out;
                }"""
            )
            browser.close()

        # Normalizar a enteros cuando sea posible y calcular métricas simples
        result: Dict[str, int] = {}
        for k, v in (perf or {}).items():
            try:
                result[k] = int(v) if v is not None else None
            except Exception:
                result[k] = None

        nav = result.get("navigationStart")
        load = result.get("loadEventEnd")
        dom = result.get("domContentLoadedEventEnd")
        if isinstance(nav, int) and isinstance(load, int) and load >= nav:
            result["total_load_time_ms"] = load - nav
        if isinstance(nav, int) and isinstance(dom, int) and dom >= nav:
            result["dom_content_loaded_ms"] = dom - nav

        return result
    except Exception as e:
        logger.exception("analyze_performance: fallo al obtener métricas de %s: %s", url, e)
        return {}
