# TP2 - Sistema de Scraping Distribuido

## Arquitectura

El sistema tiene dos servidores separados por responsabilidad:

Servidor A (Asyncio): servidor HTTP asincrónico pensado para tareas I/O-bound (peticiones HTTP, red, disco).

Servidor B (Multiprocessing): servidor TCP para tareas CPU-bound y procesamiento pesado, usa múltiples workers.

Setup

Crear entorno virtual:

python3 -m venv .venv


Activar el entorno:

source .venv/bin/activate


(En Windows: .venv\Scripts\activate)

Instalar dependencias de Python:

pip install -r requirements.txt


Instalar los navegadores para Playwright:

playwright install


# Ejecución

Se deben ejecutar los dos servidores en terminales separadas. Se recomienda arrancar el Servidor B primero.

## Terminal 1 — Servidor B (Procesamiento)

### Iniciar con valores por defecto (Puerto 9090, Workers = CPUs)
python3 server_processing.py

Iniciar con argumentos específicos:
python3 server_processing.py -p 9090 -n 4


Verás: 🚀 Servidor B (Multiprocessing) iniciando en 0.0.0.0:9090 (workers=4)

## Terminal 2 — Servidor A (Scraping)

### Iniciar con valores por defecto (Puerto 8080, Host '::')
### NOTA: Se recomienda usar -i 127.0.0.1 para evitar problemas IPv4/IPv6
python3 server_scraping.py -i 127.0.0.1 -p 8080


Verás: 🚀 Servidor A (Asyncio) iniciando en http://127.0.0.1:8080

Testing

Hay dos formas de probar el sistema:

1. Pruebas Unitarias (Pytest)

Este comando prueba la lógica interna del scraper (ej. el parseo de HTML) sin necesidad de levantar los servidores.

============================= test session starts ==============================
platform linux -- Python 3.11.2, pytest-8.4.2, pluggy-1.6.0
rootdir: /home/lucianotoneatti/Documentos/Facultad/Computacion2/Computacion2/TP2
plugins: asyncio-1.2.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collected 1 item                                                               

tests/test_scraper.py .                                                  [100%]

============================== 1 passed in 0.04s ===============================


2. Prueba de Integración (Cliente)

Con ambos servidores corriendo, abre una tercera terminal para ejecutar el cliente.

## Terminal 3 — Cliente

### Ejecutar una solicitud de scraping completa
python3 client.py -p 8080 https://github.com


(El cliente apuntará al Servidor A en el puerto 8080 y le pedirá scrapear github.com)

Tras unos segundos, verás el JSON completo con los datos de scraping_data y processing_data.

Health Check (Opcional)

Puedes usar curl para verificar rápidamente si el Servidor A está vivo:

curl http://127.0.0.1:8080/health
# Respuesta: {"status": "ok", "server": "A - Asyncio"}


Estructura del Proyecto

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
