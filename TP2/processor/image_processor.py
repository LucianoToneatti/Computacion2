"""Procesamiento de imágenes con Pillow"""

import logging
import base64
import io
from typing import List

import requests
from PIL import Image
from PIL import UnidentifiedImageError

logger = logging.getLogger("processor.image_processor")


def generate_thumbnails(image_urls: List[str], size: int = 100, timeout: int = 10) -> List[str]:
    """
    Descarga cada imagen de image_urls, genera un thumbnail de `size`x`size`
    y devuelve una lista con las imágenes resultantes codificadas en base64 (PNG).
    Si una imagen falla, se la ignora y se continúa con las siguientes.
    """
    thumbnails: List[str] = []
    for url in image_urls:
        try:
            resp = requests.get(url, timeout=timeout, stream=True)
            resp.raise_for_status()
            data = resp.content
            with io.BytesIO(data) as img_buf:
                try:
                    with Image.open(img_buf) as img:
                        # Convertir a RGB para evitar problemas con paletas/alpha al guardar PNG
                        if img.mode not in ("RGB", "RGBA"):
                            img = img.convert("RGB")
                        img.thumbnail((size, size), Image.LANCZOS)
                        out_buf = io.BytesIO()
                        img.save(out_buf, format="PNG")
                        out_bytes = out_buf.getvalue()
                        thumbnails.append(base64.b64encode(out_bytes).decode("ascii"))
                except UnidentifiedImageError:
                    logger.warning("generate_thumbnails: imagen no identificada o formato no soportado: %s", url)
                    thumbnails.append(None)
                    continue
        except Exception as e:
            logger.exception("generate_thumbnails: fallo procesando %s: %s", url, e)
            # ignorar y seguir con la siguiente imagen
            continue
    return thumbnails
