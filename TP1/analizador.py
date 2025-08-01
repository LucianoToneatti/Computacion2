"""
Procesos Analizadores - Procesan señales biométricas específicas
Mantienen ventana móvil de 30 segundos y calculan estadísticas
"""
import numpy as np
from collections import deque
from multiprocessing import Queue

def extraer_valor_senal(datos, tipo_senal):
    """
    Extrae el valor específico según el tipo de señal
    """
    if tipo_senal == "frecuencia":
        return datos["frecuencia"]
    elif tipo_senal == "presion":
        return datos["presion"][0]  
    elif tipo_senal == "oxigeno":
        return datos["oxigeno"]
    else:
        raise ValueError(f"Tipo de señal desconocido: {tipo_senal}")

def proceso_analizador(pipe_entrada, queue_salida, tipo_senal):
    """
    Analizador que procesa una señal específica
    """
    print(f"Analizador {tipo_senal} iniciado")
    
    ventana = deque(maxlen=30)  
    """ 
    Automáticamente mantiene solo 30 elementos 
    """
    contador_muestras = 0
    
    while True:
        try:
            datos = pipe_entrada.recv()
            
            if datos is None:
                print(f"Analizador {tipo_senal} terminando...")
                break
            
            contador_muestras += 1
            valor = extraer_valor_senal(datos, tipo_senal)
            
            ventana.append(valor)
            
            """
            Calcular estadísticas sobre la ventana actual
            """
            if len(ventana) > 0:  
                valores_array = np.array(list(ventana))
                media = float(np.mean(valores_array))
                desviacion = float(np.std(valores_array))
                
                """
                Crear resultado según formato de consignas
                """
                resultado = {
                    "tipo": tipo_senal,
                    "timestamp": datos["timestamp"],
                    "media": media,
                    "desv": desviacion
                }
                
                """
                Envia al verificador
                """
                queue_salida.put(resultado)
                
                print(f"{tipo_senal.capitalize()} - Muestra {contador_muestras}: "
                      f"valor={valor}, media={media:.2f}, desv={desviacion:.2f}, "
                      f"ventana_size={len(ventana)}")
            
        except Exception as e:
            print(f"Error en analizador {tipo_senal}: {e}")
            break
    
    print(f"Analizador {tipo_senal} finalizado")

if __name__ == "__main__":
    pass