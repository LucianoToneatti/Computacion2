"""Módulo para parsear HTML con BeautifulSoup"""

import logging
from typing import Dict, List, Optional
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from scraper.metadata_extractor import extract_metadata

logger = logging.getLogger("scraper.html_parser")


def parse_html_basic(html_content: str, base_url: str = "") -> Dict[str, object]:
    """
    Parsea HTML y extrae:
    - title: texto del <title> o None
    - links: lista de href absolutos de todas las etiquetas <a> (solo valores no vacíos)
    - images_count: conteo total de etiquetas <img>

    Se aplica urljoin para convertir los links relativos a absolutos.
    """
    try:
        #  usar lxml
        soup = BeautifulSoup(html_content, "lxml")

        title: Optional[str] = None
        if soup.title and soup.title.string:
            title = soup.title.string.strip()

        #  aplicar urljoin también a los <a href>
        raw_links = [a.get("href") for a in soup.find_all("a") if a.get("href")]
        links: List[str] = [urljoin(base_url, href) for href in raw_links]

        images_count: int = len(soup.find_all("img"))

        return {"title": title, "links": links, "images_count": images_count}
    except Exception as e:
        logger.exception("Error al parsear HTML: %s", e)
        return {"title": None, "links": [], "images_count": 0}


def parse_html_full(html_content: str, base_url: str = "") -> Dict[str, object]:
    """
    Parsea HTML y devuelve un diccionario con:
    - title
    - links: href absolutos
    - images_count
    - image_urls: lista de src absolutos de las primeras 5 imágenes
    - meta_tags
    - structure
    """
    try:
        #  usar lxml
        soup = BeautifulSoup(html_content, "lxml")

        title: Optional[str] = None
        if soup.title and soup.title.string:
            title = soup.title.string.strip()

        #  aplicar urljoin también a los links
        raw_links = [a.get("href") for a in soup.find_all("a") if a.get("href")]
        links: List[str] = [urljoin(base_url, href) for href in raw_links]

        images_count: int = len(soup.find_all("img"))

        # Resolver imágenes absolutas (primeras 5)
        image_urls: List[str] = []
        for img in soup.find_all("img"):
            src = img.get("src")
            if not src:
                continue
            image_urls.append(urljoin(base_url, src))
        image_urls = image_urls[:5]

        metadata = extract_metadata(soup)
        structure = extract_structure(soup)

        return {
            "title": title,
            "links": links,
            "images_count": images_count,
            "image_urls": image_urls,
            "meta_tags": metadata,
            "structure": structure,
        }
    except Exception as e:
        logger.exception("Error al parsear HTML completo: %s", e)
        return {
            "title": None,
            "links": [],
            "images_count": 0,
            "image_urls": [],
            "meta_tags": {"description": None, "keywords": None, "og": {}},
            "structure": {f"h{i}": 0 for i in range(1, 7)},
        }


def extract_structure(soup: BeautifulSoup) -> Dict[str, int]:
    """
    Cuenta etiquetas de encabezado H1..H6.
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

