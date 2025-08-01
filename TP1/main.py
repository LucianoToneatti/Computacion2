"""
Programa Principal - Coordinador del Sistema Biométrico
Crea y coordina todos los procesos según la arquitectura requerida
"""
from multiprocessing import Process, Pipe, Queue
import time
import sys

# Importar nuestros módulos
from generador import proceso_generador
from analizador import proceso_analizador
from verificador import proceso_verificador

def main():
    """
    Función principal que coordina todo el sistema
    """
    print("=== Sistema Concurrente de Análisis Biométrico ===")
    print("Tarea 2: Verificación y Construcción de Bloques")
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
        Crear proceso verificador
        """
        proceso_verif = Process(
            target=proceso_verificador,
            args=(queue_resultados,),
            name="Verificador"
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
        proceso_verif.start()  
        proceso_freq.start()
        proceso_pres.start()
        proceso_oxi.start()
        
        print("Procesos iniciados. El verificador construirá la blockchain...")
        print("(Presiona Ctrl+C para terminar anticipadamente)")
        print("-" * 60)
        
        proceso_gen.join(timeout=70)
        
        """
        Dar tiempo extra para que los analizadores terminen 
        """
        proceso_freq.join(timeout=10)
        proceso_pres.join(timeout=10)
        proceso_oxi.join(timeout=10)
        
        """
        Dar tiempo al verificador para procesar todos los resultados
        """
        proceso_verif.join(timeout=15)
        
    except KeyboardInterrupt:
        print("\nInterrupción del usuario. Terminando procesos...")
        
        """
        Terminar procesos si siguen vivos 
        """
        for proceso in [proceso_gen, proceso_verif, proceso_freq, proceso_pres, proceso_oxi]:
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
        
        print("Tarea 2 completada. Revisa el archivo blockchain.json generado.")

if __name__ == "__main__":
    main()