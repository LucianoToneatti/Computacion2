"""
Proceso Principal - Generador de datos biométricos
Genera 60 muestras (1 por segundo) y las envía a los analizadores
"""
import json
import time
import random
from datetime import datetime
from multiprocessing import Process, Pipe

def generar_datos_biometricos():
    """
    Genera un diccionario con datos biométricos simulados
    """
    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    
    # Rangos exactos según consignas
    frecuencia = random.randint(60, 180)
    presion_sistolica = random.randint(110, 180)
    presion_diastolica = random.randint(70, 110)
    oxigeno = random.randint(90, 100)
    
    return {
        "timestamp": timestamp,
        "frecuencia": frecuencia,
        "presion": [presion_sistolica, presion_diastolica],
        "oxigeno": oxigeno
    }

def proceso_generador(pipe_frecuencia, pipe_presion, pipe_oxigeno):
    """
    Proceso principal que genera y envía datos cada segundo
    """
    print("Iniciando generación de datos biométricos...")
    print("Generando 60 muestras (1 por segundo)")
    
    for i in range(60):
        """ 
        Generar datos 
        """
        datos = generar_datos_biometricos()
        
        print(f"Muestra {i+1}/60 - {datos['timestamp']}: "
              f"FC={datos['frecuencia']}, "
              f"PA={datos['presion'][0]}/{datos['presion'][1]}, "
              f"O2={datos['oxigeno']}%")
        
        """ 
        Enviar los mismos datos a los 3 analizadores 
        """
        try:
            pipe_frecuencia.send(datos)
            pipe_presion.send(datos)
            pipe_oxigeno.send(datos)
        except Exception as e:
            print(f"Error enviando datos: {e}")
            break
        
        """ 
        Espera 1 segundo antes de la siguiente muestra
        """
        time.sleep(1)
    
    pipe_frecuencia.send(None)
    pipe_presion.send(None)
    pipe_oxigeno.send(None)
    
    print("Generación completada.")

if __name__ == "__main__":
    pass