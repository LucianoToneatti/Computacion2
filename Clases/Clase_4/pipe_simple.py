import os

# Crear el pipe: devuelve dos file descriptors (lectura, escritura)
read_fd, write_fd = os.pipe()

# Crear proceso hijo con fork
pid = os.fork()

if pid == 0:
    # Proceso hijo
    os.close(write_fd)  # Cierra el extremo de escritura, solo va a leer
    r = os.fdopen(read_fd)  # Abre el extremo de lectura como archivo
    mensaje = r.read()
    print(f"Hijo recibió: {mensaje}")
    r.close()
else:
    # Proceso padre
    os.close(read_fd)  # Cierra el extremo de lectura, solo va a escribir
    w = os.fdopen(write_fd, 'w')  # Abre el extremo de escritura como archivo
    w.write("¡Hola desde el padre!\n")
    w.close()
