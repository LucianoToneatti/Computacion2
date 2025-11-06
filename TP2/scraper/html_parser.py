"""Módulo para parsear HTML con BeautifulSoup"""

import logging
from typing import Dict, List, Optional

from bs4 import BeautifulSoup

logger = logging.getLogger("scraper.html_parser")


def parse_html_basic(html_content: str) -> Dict[str, object]:
    """
    Parsea HTML y extrae:
    - title: texto del <title> o None
    - links: lista de href de todas las etiquetas <a> (solo valores no vacíos)
    - images_count: conteo total de etiquetas <img>
    """
    try:
        soup = BeautifulSoup(html_content, "html.parser")

        title: Optional[str] = None
        if soup.title and soup.title.string:
            title = soup.title.string.strip()

        links: List[str] = [a.get("href") for a in soup.find_all("a") if a.get("href")]
        images_count: int = len(soup.find_all("img"))

        return {"title": title, "links": links, "images_count": images_count}
    except Exception as e:
        logger.exception("Error al parsear HTML: %s", e)
        return {"title": None, "links": [], "images_count": 0}
