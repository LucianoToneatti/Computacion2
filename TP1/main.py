"""
Programa Principal - Coordinador del Sistema Biométrico
Crea y coordina todos los procesos según la arquitectura requerida
"""
from multiprocessing import Process, Pipe, Queue
import time
import sys

from generador import proceso_generador
from analizador import proceso_analizador

def main():
    """
    Función principal que coordina todo el sistema
    """
    print("=== Sistema Concurrente de Análisis Biométrico ===")
    print("Tarea 1: Generación y Análisis Concurrente")
    print()
    
    """
    Crear pipes para comunicación Generador -> Analizadores 
    """
    pipe_gen_freq, pipe_recv_freq = Pipe()  # Para analizador de frecuencia
    pipe_gen_pres, pipe_recv_pres = Pipe()  # Para analizador de presión  
    pipe_gen_oxi, pipe_recv_oxi = Pipe()    # Para analizador de oxígeno
    
    """
    Crear queue para comunicación Analizadores -> Verificador
    """
    queue_resultados = Queue()
    
    try:
        """
        Crear proceso generador 
        """
        proceso_gen = Process(
            target=proceso_generador,
            args=(pipe_gen_freq, pipe_gen_pres, pipe_gen_oxi),
            name="Generador"
        )
        
        """
        Crear procesos analizadores
        """
        proceso_freq = Process(
            target=proceso_analizador,
            args=(pipe_recv_freq, queue_resultados, "frecuencia"),
            name="Analizador-Frecuencia"
        )
        
        proceso_pres = Process(
            target=proceso_analizador,
            args=(pipe_recv_pres, queue_resultados, "presion"),
            name="Analizador-Presion"
        )
        
        proceso_oxi = Process(
            target=proceso_analizador,
            args=(pipe_recv_oxi, queue_resultados, "oxigeno"),
            name="Analizador-Oxigeno"
        )
        
        print("Iniciando procesos...")
        proceso_gen.start()
        proceso_freq.start()
        proceso_pres.start()
        proceso_oxi.start()
        
        print("Procesos iniciados. Monitoreando resultados...")
        print("(Presiona Ctrl+C para terminar anticipadamente)")
        print("-" * 60)
        
        """
        Monitorear resultados mientras los procesos trabajen 
        """
        resultados_recibidos = 0
        total_esperado = 60 * 3  
        
        while resultados_recibidos < total_esperado:
            try:
            
                resultado = queue_resultados.get(timeout=5)
                resultados_recibidos += 1
                
                print(f"Resultado {resultados_recibidos}/{total_esperado}: "
                      f"{resultado['tipo']} - {resultado['timestamp']} - "
                      f"Media: {resultado['media']:.2f}, Desv: {resultado['desv']:.2f}")
                
            except:
                
                if not any([proceso_gen.is_alive(), proceso_freq.is_alive(), 
                           proceso_pres.is_alive(), proceso_oxi.is_alive()]):
                    print("Todos los procesos han terminado.")
                    break
        
        print("-" * 60)
        print("Esperando que terminen todos los procesos...")
        
        """
        Esperar que terminen todos los procesos
        """
        proceso_gen.join(timeout=10)
        proceso_freq.join(timeout=10)
        proceso_pres.join(timeout=10)
        proceso_oxi.join(timeout=10)
        
        print(f"Tarea 1 completada. Resultados procesados: {resultados_recibidos}")
        
    except KeyboardInterrupt:
        print("\nInterrupción del usuario. Terminando procesos...")
        
        for proceso in [proceso_gen, proceso_freq, proceso_pres, proceso_oxi]:
            if proceso.is_alive():
                proceso.terminate()
                proceso.join(timeout=2)
                if proceso.is_alive():
                    proceso.kill()
        
    except Exception as e:
        print(f"Error en el programa principal: {e}")
        
    finally:
        try:
            pipe_gen_freq.close()
            pipe_gen_pres.close()
            pipe_gen_oxi.close()
            pipe_recv_freq.close()
            pipe_recv_pres.close()
            pipe_recv_oxi.close()
            queue_resultados.close()
        except:
            pass
        
        print("Recursos liberados. Programa terminado.")

if __name__ == "__main__":
    main()