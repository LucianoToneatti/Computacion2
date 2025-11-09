"""Serialización/deserialización de mensajes"""

import json
import logging
from typing import Any, Dict

logger = logging.getLogger("common.serialization")


def serialize_data(data: Dict[str, Any]) -> bytes:
    """
    Serializa un diccionario a bytes JSON (utf-8).
    Lanza TypeError/ValueError si el objeto no es serializable.
    """
    try:
        return json.dumps(data, ensure_ascii=False).encode("utf-8")
    except (TypeError, ValueError) as e:
        logger.exception("serialize_data: error serializando datos: %s", e)
        raise


def deserialize_data(payload: bytes) -> Dict[str, Any]:
    """
    Deserializa bytes JSON (utf-8) a diccionario.
    Lanza json.JSONDecodeError o UnicodeDecodeError en caso de error.
    """
    try:
        if not isinstance(payload, (bytes, bytearray)):
            raise TypeError("payload must be bytes or bytearray")
        text = payload.decode("utf-8")
        obj = json.loads(text)
        if not isinstance(obj, dict):
            # Normalizar a dict para mantener la interfaz esperada
            return {"value": obj}
        return obj
    except Exception as e:
        logger.exception("deserialize_data: error deserializando payload: %s", e)
        raise
