import os
import tempfile
import time

def proceso_hijo(temp_path):
    print(f"[Hijo] PID {os.getpid()} escribiendo en {temp_path}")
    
    time.sleep(1)  # Simulamos trabajo o espera

    with open(temp_path, 'w') as f:
        f.write("Soy el hijo y escribí esto.\n")
    
    print("[Hijo] Terminó de escribir y sale.")
    os._exit(0)  # Salida segura del hijo sin ejecutar más código

def proceso_padre(temp_path):
    print(f"[Padre] PID {os.getpid()} esperando al hijo...")
    
    os.wait()  # Espera al hijo para asegurarse de que escribió
    
    print(f"[Padre] Leyendo de {temp_path}")
    
    try:
        with open(temp_path, 'r') as f:
            contenido = f.read()
            print(f"[Padre] Leyó: {contenido.strip()}")
    except FileNotFoundError:
        print("[Padre] Error: El archivo no existe.")
    except Exception as e:
        print(f"[Padre] Otro error: {e}")

    if os.path.exists(temp_path):
        os.unlink(temp_path)
        print("[Padre] Archivo temporal eliminado.")
    else:
        print("[Padre] Archivo ya no estaba disponible.")

def main():
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_path = temp_file.name
    temp_file.close()

    print(f"[Sistema] Archivo temporal creado en: {temp_path}")

    pid = os.fork()

    if pid == 0:
        proceso_hijo(temp_path)
    else:
        proceso_padre(temp_path)

if __name__ == "__main__":
    main()
