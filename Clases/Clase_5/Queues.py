import queue

# Crear una cola
cola = queue.Queue()

# Añadir elementos a la cola
cola.put(1)
cola.put(2)
cola.put(3)

# Obtener elementos de la cola
while not cola.empty():
    print(cola.get())
