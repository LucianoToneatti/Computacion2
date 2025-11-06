"""Extrae metadatos de páginas web"""

import logging
from typing import Dict, Optional
from bs4 import BeautifulSoup

logger = logging.getLogger("scraper.metadata_extractor")


def extract_metadata(soup: BeautifulSoup) -> Dict[str, Optional[object]]:
    """
    Extrae metadata desde un objeto BeautifulSoup.
    Devuelve un diccionario con las claves:
      - description: contenido de <meta name="description"> o None
      - keywords: contenido de <meta name="keywords"> o None
      - og: diccionario con las propiedades Open Graph (por ejemplo "og:title": "..." stored as "title": "...")
    """
    try:
        result: Dict[str, Optional[object]] = {"description": None, "keywords": None, "og": {}}

        # description
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if meta_desc and meta_desc.get("content"):
            result["description"] = meta_desc.get("content").strip()

        # keywords
        meta_kw = soup.find("meta", attrs={"name": "keywords"})
        if meta_kw and meta_kw.get("content"):
            result["keywords"] = meta_kw.get("content").strip()

        # Open Graph (og:*)
        og_dict: Dict[str, str] = {}
        for meta in soup.find_all("meta"):
            prop = meta.get("property") or meta.get("name")
            if not prop:
                continue
            prop = prop.strip()
            if prop.lower().startswith("og:"):
                key = prop[3:]  # quitar "og:"
                content = meta.get("content")
                if content:
                    og_dict[key] = content.strip()

        result["og"] = og_dict
        return result
    except Exception as e:
        logger.exception("Error al extraer metadata: %s", e)
        return {"description": None, "keywords": None, "og": {}}
