import os
import time

def crear_cascada(profundidad, nivel=0):
    print(f"Soy el proceso {os.getpid()} y estoy en el nivel {nivel}")

    if profundidad > 0:
        pid = os.fork()
        if pid == 0:
            # Proceso hijo
            print(f"Soy el hijo {os.getpid()} de {os.getppid()}")
            time.sleep(2)
            crear_cascada(profundidad - 1, nivel + 1)
            os._exit(0)
        else:
            # Proceso padre no espera a su hijo
            time.sleep(1)

if __name__ == "__main__":
    PROFUNDIDAD = 5  # Número de generaciones en la cascada
    crear_cascada(PROFUNDIDAD)
