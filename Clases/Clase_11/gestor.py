#!/usr/bin/env python3

import argparse
import os
import random
import time
import subprocess
import sys

def main():
    parser = argparse.ArgumentParser(description="Crea procesos hijos.")
    parser.add_argument("--num", type=int, required=True, help="Cantidad de procesos hijos a crear")
    parser.add_argument("--verbose", action="store_true", help="Activa mensajes detallados")
    args = parser.parse_args()

    num_processes = args.num
    verbose = args.verbose

    hijos_pids = []

    print(f"[PADRE] Mi PID es {os.getpid()}")

    for i in range(num_processes):
        pid = os.fork()
        if pid == 0:
            # Proceso hijo
            tiempo = random.randint(1, 5)
            if verbose:
                print(f"[HIJO {os.getpid()}] Voy a dormir {tiempo} segundos")
            time.sleep(tiempo)
            if verbose:
                print(f"[HIJO {os.getpid()}] Terminando")
            sys.exit(0)  # Importante: termina el hijo
        else:
            # Proceso padre
            hijos_pids.append(pid)

    if verbose:
        print(f"[PADRE] Esperando que terminen {len(hijos_pids)} procesos hijos...")

    for pid in hijos_pids:
        os.waitpid(pid, 0)

    print("[PADRE] Todos los hijos terminaron.")
    print("[PADRE] Jerarquía de procesos (pstree):\n")

    # Mostrar la jerarquía de procesos usando pstree -p
    subprocess.run(["pstree", "-p", str(os.getpid())])

if __name__ == "__main__":
    main()
