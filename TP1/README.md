# Sistema Concurrente de Análisis Biométrico con Cadena de Bloques Local

## Descripción
Sistema que simula el monitoreo biométrico de una prueba de esfuerzo durante 60 segundos, procesando datos de frecuencia cardíaca, presión arterial y oxígeno en sangre mediante procesos concurrentes y almacenando los resultados en una cadena de bloques local.

## Requisitos del Sistema
- Python ≥ 3.9
- Librerías estándar: `numpy`, `hashlib`, `multiprocessing`, `queue`, `os`, `json`, `datetime`, `random`

## Estructura del Proyecto
```
├── main.py              # Proceso principal y coordinación
├── generador.py         # Generación de muestras biométricas
├── analizador.py        # Procesos de análisis concurrente
├── verificador.py       # Construcción de blockchain
├── verificar_cadena.py  # Verificación de integridad
├── blockchain.json      # Cadena de bloques generada
├── reporte.txt         # Reporte estadístico
└── README.md           # Este archivo
```

## Instalación y Ejecución

### 1. Ejecución Principal
```bash
python main.py
```
Este comando ejecutará todo el sistema:
- Generará 60 muestras biométricas (1 por segundo)
- Procesará los datos con 3 analizadores concurrentes
- Construirá la cadena de bloques
- Guardará el resultado en `blockchain.json`

### 2. Verificación de Integridad
```bash
python verificar_cadena.py
```
Este comando:
- Verificará la integridad de todos los bloques
- Validará el encadenamiento de la blockchain
- Generará el archivo `reporte.txt` con estadísticas

## Funcionamiento del Sistema

### Arquitectura
```
Generador → [Pipe/FIFO] → Analizadores (3 procesos) → [Queue] → Verificador → Blockchain
```

### Proceso de Datos
1. **Generador**: Crea muestras cada segundo con frecuencia (60-180), presión (110-180/70-110), oxígeno (90-100)
2. **Analizadores**: Mantienen ventana móvil de 30 segundos y calculan media/desviación estándar
3. **Verificador**: Agrupa resultados, valida rangos y construye bloques con hash SHA-256
4. **Blockchain**: Cadena enlazada persistida en JSON

### Validaciones de Alertas
- Frecuencia cardíaca ≥ 200 bpm
- Oxígeno fuera del rango 90-100%
- Presión sistólica ≥ 200 mmHg

## Archivos Generados

### blockchain.json
Contiene la cadena de bloques con estructura:
```json
{
  "timestamp": "YYYY-MM-DDTHH:MM:SS",
  "datos": {
    "frecuencia": {"media": X, "desv": Y},
    "presion": {"media": X, "desv": Y},
    "oxigeno": {"media": X, "desv": Y}
  },
  "alerta": boolean,
  "prev_hash": "...",
  "hash": "sha256(...)"
}
```

### reporte.txt
Estadísticas del análisis:
- Cantidad total de bloques
- Número de bloques con alertas
- Promedios generales de frecuencia, presión y oxígeno
- Información de integridad de la cadena

## Ejemplo de Ejecución

```bash
$ python main.py
Generador iniciado - Enviando 60 muestras...
Analizador frecuencia iniciado
Analizador presion iniciado
Analizador oxigeno iniciado
Verificador iniciado - Esperando resultados...

Muestra 1/60 - 2025-08-01T13:38:30: FC=67, PA=148/94, O2=94%
[... procesamiento ...]
📦 Bloque 60 creado: Hash=ce109dacf27d39d2... ✅ OK

Tarea 2 completada. Revisa el archivo blockchain.json generado.

$ python verificar_cadena.py
🔍 Verificando cadena de bloques con 60 bloques...
✅ Bloque 1: Hash válido
[... verificación ...]
✅ La cadena de bloques es íntegra y válida
📄 Reporte generado: reporte.txt
✅ Tarea 3 completada exitosamente
```

## Características Técnicas

### Concurrencia
- 4 procesos principales (1 generador + 3 analizadores)
- 1 proceso verificador
- Comunicación via Pipes y Queues
- Sincronización automática por timestamps

### Seguridad
- Hashes SHA-256 para integridad
- Encadenamiento criptográfico
- Verificación de integridad post-ejecución

### Rendimiento
- Procesamiento en tiempo real (1 muestra/segundo)
- Ventana móvil eficiente (30 segundos)
- Almacenamiento persistente en JSON

## Solución de Problemas

### Error: "No se encontró blockchain.json"
- Ejecutar primero `python main.py`

### Error: "Procesos no finalizan"
- Verificar que no hay procesos zombi: `ps aux | grep python`
- El sistema maneja automáticamente la limpieza de recursos

### Verificación falla
- El blockchain podría estar corrupto
- Regenerar ejecutando `python main.py` nuevamente

## Autor
Luciano Toneatti 
