import os
import time

def crear_proceso_zombi():
    pid = os.fork()
    if pid == 0:  # Soy el proceso hijo
        print("Hijo zombi creado con PID", pid)
        os._exit(0)  # Finalizar inmediatamente
    else:  # Soy el proceso padre
        time.sleep(10)  # Esperar 10 segundos antes de recolectar el estado del hijo

if __name__ == '__main__':
    crear_proceso_zombi()
