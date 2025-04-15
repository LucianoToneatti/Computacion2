import os

# Crear dos pipes: uno para cada dirección
padre_a_hijo_r, padre_a_hijo_w = os.pipe()
hijo_a_padre_r, hijo_a_padre_w = os.pipe()

pid = os.fork()

if pid == 0:
    # Proceso hijo
    os.close(padre_a_hijo_w)  # Cierra escritura del pipe del padre
    os.close(hijo_a_padre_r)  # Cierra lectura del pipe del hijo

    # Leer del padre
    r = os.fdopen(padre_a_hijo_r)
    mensaje_del_padre = r.read()
    print(f"[Hijo] Recibí: {mensaje_del_padre}")
    r.close()

    # Responder al padre
    w = os.fdopen(hijo_a_padre_w, 'w')
    w.write("Hola papá, soy tu hijo proceso 👶")
    w.close()

else:
    # Proceso padre
    os.close(padre_a_hijo_r)  # Cierra lectura del pipe del padre
    os.close(hijo_a_padre_w)  # Cierra escritura del pipe del hijo

    # Enviar mensaje al hijo
    w = os.fdopen(padre_a_hijo_w, 'w')
    w.write("Hola hijo, soy tu padre proceso 🧔")
    w.close()

    # Leer respuesta del hijo
    r = os.fdopen(hijo_a_padre_r)
    respuesta = r.read()
    print(f"[Padre] El hijo respondió: {respuesta}")
    r.close()
