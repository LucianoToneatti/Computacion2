"""Protocolo de comunicación entre servidores"""

import struct
import logging
from typing import Dict, Any

from common.serialization import serialize_data

logger = logging.getLogger("common.protocol")


def pack_message(data: Dict[str, Any]) -> bytes:
    """
    Empaqueta un dict en un mensaje binario con header de 4 bytes (big-endian uint32)
    seguido del payload JSON (utf-8).

    Header: struct.pack('!I', len(payload))
    Payload: serialize_data(data)
    """
    try:
        payload = serialize_data(data)
        length = len(payload)
        if length >= 2**32:
            raise ValueError("payload too large for 4-byte length header")
        header = struct.pack("!I", length)
        return header + payload
    except Exception as e:
        logger.exception("pack_message: error empaquetando mensaje: %s", e)
        raise
