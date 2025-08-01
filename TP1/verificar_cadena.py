"""
Verificador de Integridad de la cadena de bloques
"""
import json
import hashlib
import os
from datetime import datetime

def calcular_hash(prev_hash, datos, timestamp):
    """
    Calcula el hash SHA-256 de un bloque
    """
    contenido = prev_hash + str(datos) + timestamp
    return hashlib.sha256(contenido.encode()).hexdigest()

def verificar_cadena():
    """
    Verifica la integridad de la cadena de bloques
    """
    
    # Verificar si existe el archivo
    if not os.path.exists('blockchain.json'):
        print("❌ Error: No se encontró el archivo blockchain.json")
        return False
    
    try:
        # Cargar la cadena de bloques
        with open('blockchain.json', 'r') as f:
            blockchain = json.load(f)
        
        print(f"🔍 Verificando cadena de bloques con {len(blockchain)} bloques...")
        print("=" * 60)
        
        bloques_corruptos = []
        bloques_validos = 0
        
        for i, bloque in enumerate(blockchain):
            # Recalcular el hash del bloque
            hash_calculado = calcular_hash(
                bloque['prev_hash'],
                bloque['datos'],
                bloque['timestamp']
            )
            
            # Verificar si el hash coincide
            if hash_calculado == bloque['hash']:
                bloques_validos += 1
                print(f"✅ Bloque {i+1}: Hash válido")
            else:
                bloques_corruptos.append(i+1)
                print(f"❌ Bloque {i+1}: Hash corrupto")
                print(f"   Hash esperado: {bloque['hash']}")
                print(f"   Hash calculado: {hash_calculado}")
            
            # Verificar encadenamiento (excepto para el primer bloque)
            if i > 0:
                prev_hash_esperado = blockchain[i-1]['hash']
                if bloque['prev_hash'] == prev_hash_esperado:
                    print(f"🔗 Bloque {i+1}: Encadenamiento válido")
                else:
                    bloques_corruptos.append(i+1)
                    print(f"💔 Bloque {i+1}: Encadenamiento corrupto")
                    print(f"   Prev_hash esperado: {prev_hash_esperado}")
                    print(f"   Prev_hash actual: {bloque['prev_hash']}")
        
        print("=" * 60)
        
        # Resumen de la verificación
        print(f"📊 RESUMEN DE VERIFICACIÓN:")
        print(f"   Total de bloques: {len(blockchain)}")
        print(f"   Bloques válidos: {bloques_validos}")
        print(f"   Bloques corruptos: {len(set(bloques_corruptos))}")
        
        if bloques_corruptos:
            print(f"   Bloques con problemas: {sorted(set(bloques_corruptos))}")
            return False
        else:
            print("✅ La cadena de bloques es íntegra y válida")
            return True
            
    except json.JSONDecodeError:
        print("❌ Error: El archivo blockchain.json tiene formato inválido")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def generar_reporte():
    """Genera el archivo reporte.txt con estadísticas"""
    
    if not os.path.exists('blockchain.json'):
        print("❌ Error: No se encontró el archivo blockchain.json")
        return
    
    try:
        with open('blockchain.json', 'r') as f:
            blockchain = json.load(f)
        
        # Contadores y acumuladores
        total_bloques = len(blockchain)
        bloques_con_alerta = 0
        suma_frecuencia = 0
        suma_presion = 0
        suma_oxigeno = 0
        
        for bloque in blockchain:
            # Contar alertas
            if bloque.get('alerta', False):
                bloques_con_alerta += 1
            
            # Acumular promedios
            datos = bloque['datos']
            suma_frecuencia += datos['frecuencia']['media']
            suma_presion += datos['presion']['media']
            suma_oxigeno += datos['oxigeno']['media']
        
        # Calcular promedios generales
        promedio_frecuencia = suma_frecuencia / total_bloques if total_bloques > 0 else 0
        promedio_presion = suma_presion / total_bloques if total_bloques > 0 else 0
        promedio_oxigeno = suma_oxigeno / total_bloques if total_bloques > 0 else 0
        
        # Generar reporte
        fecha_reporte = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        contenido_reporte = f"""REPORTE DE ANÁLISIS BIOMÉTRICO
================================

Fecha de generación: {fecha_reporte}
Archivo analizado: blockchain.json

ESTADÍSTICAS GENERALES:
- Cantidad total de bloques: {total_bloques}
- Número de bloques con alertas: {bloques_con_alerta}
- Porcentaje de bloques con alertas: {(bloques_con_alerta/total_bloques*100):.2f}%

PROMEDIOS GENERALES:
- Frecuencia cardíaca promedio: {promedio_frecuencia:.2f} bpm
- Presión arterial promedio: {promedio_presion:.2f} mmHg
- Oxígeno en sangre promedio: {promedio_oxigeno:.2f}%

INFORMACIÓN ADICIONAL:
- Duración total del monitoreo: {total_bloques} segundos ({total_bloques/60:.2f} minutos)
- Integridad de la cadena: {"✅ Verificada" if verificar_integridad_silenciosa() else "❌ Comprometida"}
"""
        
        # Escribir archivo de reporte
        with open('reporte.txt', 'w', encoding='utf-8') as f:
            f.write(contenido_reporte)
        
        print(f"📄 Reporte generado: reporte.txt")
        print("📊 Contenido del reporte:")
        print("-" * 40)
        print(contenido_reporte)
        
    except Exception as e:
        print(f"❌ Error al generar el reporte: {e}")

def verificar_integridad_silenciosa():
    """Verificación silenciosa para el reporte"""
    try:
        with open('blockchain.json', 'r') as f:
            blockchain = json.load(f)
        
        for i, bloque in enumerate(blockchain):
            hash_calculado = calcular_hash(
                bloque['prev_hash'],
                bloque['datos'],
                bloque['timestamp']
            )
            
            if hash_calculado != bloque['hash']:
                return False
            
            if i > 0 and bloque['prev_hash'] != blockchain[i-1]['hash']:
                return False
        
        return True
    except:
        return False

def main():
    """Función principal"""
    print("🔐 VERIFICADOR DE CADENA DE BLOQUES")
    print("=" * 60)
    
    # Verificar integridad de la cadena
    cadena_integra = verificar_cadena()
    
    print("\n" + "=" * 60)
    
    # Generar reporte
    generar_reporte()
    
    print("\n" + "=" * 60)
    print("✅ Tarea 3 completada exitosamente")

if __name__ == "__main__":
    main()