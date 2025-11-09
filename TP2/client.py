"""Cliente de prueba: solicita /scrape al servidor A y muestra el JSON formateado."""
import argparse
import json
import sys

import requests


def main() -> None:
    parser = argparse.ArgumentParser(description="Cliente para el sistema de scraping")
    parser.add_argument("url", help="URL a scrapear")
    parser.add_argument("-i", "--host", default="127.0.0.1", help="host del servidor A (default 127.0.0.1)")
    parser.add_argument("-p", "--port", type=int, default=8080, help="puerto del servidor A (default 8080)")
    parser.add_argument("-t", "--timeout", type=float, default=15.0, help="timeout de la petición en segundos")
    args = parser.parse_args()

    endpoint = f"http://{args.host}:{args.port}/scrape"
    try:
        resp = requests.get(endpoint, params={"url": args.url}, timeout=args.timeout)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"Error realizando la petición: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        data = resp.json()
    except ValueError as e:
        print(f"Respuesta no JSON: {e}", file=sys.stderr)
        print(resp.text, file=sys.stderr)
        sys.exit(1)

    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
