"""
Proceso Verificador - Construye la cadena de bloques
Recibe resultados de analizadores, valida y construye bloques
"""
import json
import hashlib
from multiprocessing import Queue
from collections import defaultdict

def calcular_hash(prev_hash, datos, timestamp):
    """
    Calcula el hash SHA-256 del bloque según especificaciones
    """

    contenido = prev_hash + str(datos) + timestamp
    return hashlib.sha256(contenido.encode()).hexdigest()

def validar_datos(datos):
    """
    Aplica las validaciones según consignas:
    - frecuencia < 200
    - 90 <= oxigeno <= 100  
    - presión sistólica < 200
    """
    alerta = False
    
    if datos["frecuencia"]["media"] >= 200:
        alerta = True
        print(f"⚠️  ALERTA: Frecuencia muy alta ({datos['frecuencia']['media']:.2f} >= 200)")
    
    oxigeno_media = datos["oxigeno"]["media"]
    if oxigeno_media < 90 or oxigeno_media > 100:
        alerta = True
        print(f"⚠️  ALERTA: Oxígeno fuera de rango ({oxigeno_media:.2f}, debe estar entre 90-100)")
    
    if datos["presion"]["media"] >= 200:
        alerta = True
        print(f"⚠️  ALERTA: Presión sistólica muy alta ({datos['presion']['media']:.2f} >= 200)")
    
    return alerta

def construir_bloque(timestamp, datos_completos, prev_hash, indice):

    """
    Validar datos y determinar si hay alerta
    """
    alerta = validar_datos(datos_completos)
    
    bloque = {
        "timestamp": timestamp,
        "datos": datos_completos,
        "alerta": alerta,
        "prev_hash": prev_hash,
        "hash": ""  # Se calculará después
    }
    
    """
    Calcular hash del bloque
    """
    bloque["hash"] = calcular_hash(prev_hash, datos_completos, timestamp)
    
    return bloque, alerta

def proceso_verificador(queue_resultados):
    """
    Proceso verificador principal
    Recibe resultados, agrupa por timestamp, construye y encadena bloques
    """
    print("Verificador iniciado - Esperando resultados...")

    buffer_resultados = defaultdict(dict)
    
    blockchain = []
    prev_hash = "0" * 64 
    
    resultados_procesados = 0
    bloques_creados = 0
    total_esperado = 60 * 3  
    
    while resultados_procesados < total_esperado:
        try:
            
            resultado = queue_resultados.get(timeout=10)
            resultados_procesados += 1
            
            timestamp = resultado["timestamp"]
            tipo = resultado["tipo"]

            buffer_resultados[timestamp][tipo] = {
                "media": resultado["media"],
                "desv": resultado["desv"]
            }
            
            print(f"Recibido {tipo} para {timestamp} "
                  f"({len(buffer_resultados[timestamp])}/3 completo)")
            
            """
            Si tenemos los 3 resultados para este timestamp, crear bloque 
            """
            if len(buffer_resultados[timestamp]) == 3:
 
                tipos_requeridos = {"frecuencia", "presion", "oxigeno"}
                if tipos_requeridos.issubset(buffer_resultados[timestamp].keys()):
                    
                    bloque, tiene_alerta = construir_bloque(
                        timestamp, 
                        buffer_resultados[timestamp], 
                        prev_hash, 
                        bloques_creados
                    )

                    blockchain.append(bloque)
                    prev_hash = bloque["hash"]
                    bloques_creados += 1
                    
                    """
                    Mostrar información del bloque 
                    """
                    print(f"📦 Bloque {bloques_creados} creado: "
                          f"Hash={bloque['hash'][:16]}... "
                          f"{'🚨 ALERTA' if tiene_alerta else '✅ OK'}")
                    
                    del buffer_resultados[timestamp]

                    guardar_blockchain(blockchain)
        
        except Exception as e:
            print(f"Error en verificador: {e}")
            break
    
    """
    Guardar blockchain 
    """
    guardar_blockchain(blockchain)
    
    print(f"\n📊 Verificador finalizado:")
    print(f"   - Bloques creados: {bloques_creados}")
    print(f"   - Resultados procesados: {resultados_procesados}")
    print(f"   - Blockchain guardado en: blockchain.json")

def guardar_blockchain(blockchain):
    """
    Persiste la blockchain a archivo JSON
    """
    try:
        with open("blockchain.json", "w", encoding="utf-8") as f:
            json.dump(blockchain, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error guardando blockchain: {e}")

if __name__ == "__main__":
    pass