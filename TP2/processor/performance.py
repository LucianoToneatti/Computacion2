"""Análisis de rendimiento web"""

import logging
from typing import Dict

from playwright.sync_api import sync_playwright

logger = logging.getLogger("processor.performance")


def analyze_performance(url: str, timeout: int = 30000) -> Dict[str, int]:
    """
    Usa Playwright (sync) para navegar a `url`, extraer métricas de rendimiento y
    entradas de recursos. Devuelve un diccionario con:
      - load_time_ms: tiempo total de carga (loadEventEnd - navigationStart)
      - total_size_kb: suma de tamaños de recursos en KB (aprox)
      - num_requests: número de recursos cargados
    En caso de error devuelve dict vacío y registra la excepción.
    """
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=timeout)
            page.wait_for_load_state("load", timeout=timeout)

            # Extraer performance.timing para calcular load time
            perf_timing = page.evaluate(
                """() => {
                    const t = window.performance.timing || {};
                    return {
                        navigationStart: t.navigationStart || 0,
                        loadEventEnd: t.loadEventEnd || 0,
                        domContentLoadedEventEnd: t.domContentLoadedEventEnd || 0
                    };
                }"""
            )

            # Extraer entradas de recursos (transferSize / encodedBodySize)
            resources = page.evaluate(
                """() => {
                    try {
                        return performance.getEntriesByType('resource').map(e => ({
                            transferSize: e.transferSize || 0,
                            encodedBodySize: e.encodedBodySize || 0
                        }));
                    } catch (e) {
                        return [];
                    }
                }"""
            )

            browser.close()

        # Calcular load_time_ms
        nav = int(perf_timing.get("navigationStart") or 0)
        load = int(perf_timing.get("loadEventEnd") or 0)
        load_time_ms = (load - nav) if (load >= nav and nav > 0) else 0

        # Calcular num_requests y total_size_kb
        num_requests = 0
        total_bytes = 0
        if isinstance(resources, list):
            num_requests = len(resources)
            for r in resources:
                try:
                    ts = int(r.get("transferSize", 0) or 0)
                except Exception:
                    ts = 0
                try:
                    eb = int(r.get("encodedBodySize", 0) or 0)
                except Exception:
                    eb = 0
                # Preferir transferSize si está disponible (>0), sino encodedBodySize
                chosen = ts if ts > 0 else eb
                total_bytes += chosen

        total_size_kb = round(total_bytes / 1024.0, 2)

        return {"load_time_ms": load_time_ms, "total_size_kb": total_size_kb, "num_requests": num_requests}
    except Exception as e:
        logger.exception("analyze_performance: fallo al obtener métricas de %s: %s", url, e)
        return {}
