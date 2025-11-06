"""Módulo para parsear HTML con BeautifulSoup"""

import logging
from typing import Dict, List, Optional

from bs4 import BeautifulSoup
from scraper.metadata_extractor import extract_metadata

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


def parse_html_full(html_content: str) -> Dict[str, object]:
    """
    Parsea HTML y devuelve un diccionario con:
    - title: texto del <title> o None
    - links: lista de href de todas las etiquetas <a> (solo valores no vacíos)
    - images_count: conteo total de etiquetas <img>
    - metadata: resultado de extract_metadata(soup)
    - structure: resultado de extract_structure(soup)
    """
    try:
        soup = BeautifulSoup(html_content, "html.parser")

        title: Optional[str] = None
        if soup.title and soup.title.string:
            title = soup.title.string.strip()

        links: List[str] = [a.get("href") for a in soup.find_all("a") if a.get("href")]
        images_count: int = len(soup.find_all("img"))

        metadata = extract_metadata(soup)
        structure = extract_structure(soup)

        return {
            "title": title,
            "links": links,
            "images_count": images_count,
            "metadata": metadata,
            "structure": structure,
        }
    except Exception as e:
        logger.exception("Error al parsear HTML completo: %s", e)
        return {
            "title": None,
            "links": [],
            "images_count": 0,
            "metadata": {"description": None, "keywords": None, "og": {}},
            "structure": {f"h{i}": 0 for i in range(1, 7)},
        }


def extract_structure(soup: BeautifulSoup) -> Dict[str, int]:
    """
    Cuenta etiquetas de encabezado H1..H6 en el objeto BeautifulSoup.
    Devuelve un diccionario con claves 'h1'..'h6' y sus respectivos conteos.
    """
    try:
        counts: Dict[str, int] = {}
        for i in range(1, 7):
            tag = f"h{i}"
            counts[tag] = len(soup.find_all(tag))
        return counts
    except Exception as e:
        logger.exception("Error en extract_structure: %s", e)
        return {f"h{i}": 0 for i in range(1, 7)}
