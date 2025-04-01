import os
import time

def child_process(number):
    print(f"Hijo {number}: Mi PID es {os.getpid()}")
    time.sleep(2)
    print(f"Hijo {number}: Terminando")

for i in range(2):  # Crear dos hijos
    pid = os.fork()
    if pid == 0:
        child_process(i + 1)
        os._exit(0)  # Asegurar que el hijo termina aquí

# El padre continúa sin esperar a los hijos
print("Yo soy el padre")
print("Yo soy el padre")