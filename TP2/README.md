# TP2 - Sistema de Scraping Distribuido

## Arquitectura
El sistema tiene dos servidores separados por responsabilidad:
- Servidor A (Asyncio): servidor HTTP asincrónico pensado para tareas I/O-bound (peticiones HTTP, red, disco).
- Servidor B (Multiprocessing): servidor TCP para tareas CPU-bound y procesamiento pesado, usa múltiples workers.

## Setup
1. Crear entorno virtual:
   - Linux / macOS:
     ```
     python3 -m venv venv
     ```
   - Windows:
     ```
     python -m venv venv
     ```

2. Activar el entorno:
   - Linux / macOS:
     ```
     source venv/bin/activate
     ```
   - Windows:
     ```
     venv\Scripts\activate
     ```

3. Instalar dependencias:
   ```
   pip install -r requirements.txt
   ```

## Ejecución
Se recomienda arrancar el servidor de procesamiento primero.

Terminal 1 — servidor B (Multiprocessing):
```
python server_processing.py
# o python3 server_processing.py
```

Terminal 2 — servidor A (Asyncio):
```
python server_scraping.py
# o python3 server_scraping.py
```

Al iniciar verás:
- "🚀 Servidor B (Multiprocessing) iniciando en 0.0.0.0:9090"
- "🚀 Servidor A (Asyncio) iniciando en http://0.0.0.0:8080"

## Testing
Probar endpoint /health del Servidor A:
```
curl -s http://0.0.0.0:8080/health
# respuesta esperada: {"status":"ok","server":"A - Asyncio"}
```

## Estructura del Proyecto
```
TP2
├── server_scraping.py
├── server_processing.py
├── client.py
├── scraper
│   ├── __init__.py
│   ├── html_parser.py
│   ├── metadata_extractor.py
│   └── async_http.py
├── processor
│   ├── __init__.py
│   ├── screenshot.py
│   ├── performance.py
│   └── image_processor.py
├── common
│   ├── __init__.py
│   ├── protocol.py
│   └── serialization.py
├── tests
│   ├── __init__.py
│   ├── test_scraper.py
│   └── test_processor.py
├── requirements.txt
├── README.md
└── .gitignore
```