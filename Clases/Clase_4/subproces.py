import os
import subprocess

# Creamos un pipe
read_fd, write_fd = os.pipe()

pid = os.fork()

if pid == 0:
    # Hijo: tr a-z A-Z
    os.close(write_fd)  # No escribe

    # Redirige la entrada estándar al pipe
    os.dup2(read_fd, 0)  # 0 = stdin
    os.close(read_fd)

    # Ejecuta el comando tr
    os.execlp("tr", "tr", "a-z", "A-Z")

else:
    # Padre: echo "hola mundo"
    os.close(read_fd)  # No lee

    # Escribe al pipe
    w = os.fdopen(write_fd, 'w')
    w.write("hola mundo\n")
    w.close()

    # Espera al hijo
    os.wait()
