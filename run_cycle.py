#!/usr/bin/env python
"""
run_cycle.py - Automatiza el bucle HDD (Harness-Driven Development).

Uso:
    python run_cycle.py          # Ejecuta un ciclo completo
    python run_cycle.py --loop   # Ejecuta en bucle hasta SUCCESS
"""

import subprocess
import sys
import time
import json


def ejecutar_harness():
    result = subprocess.run(
        [sys.executable, "test_harness.py"],
        capture_output=True, text=True
    )
    print(result.stdout)
    if result.stderr:
        print(f"[STDERR] {result.stderr}")
    return result.returncode


def leer_reporte():
    try:
        with open("harness_report.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def main():
    loop = "--loop" in sys.argv
    max_iteraciones = 10

    for i in range(max_iteraciones):
        print(f"\n{'='*50}")
        print(f" CICLO HDD #{i + 1}")
        print(f"{'='*50}")

        codigo = ejecutar_harness()
        reporte = leer_reporte()

        if reporte and reporte.get("harness_status") == "SUCCESS":
            print("\n[HDR] ESTADO: SUCCESS - Todas las pruebas pasan.")
            return 0

        if not loop:
            print("\n[HDR] ESTADO: FAILED - Revisa harness_report.json")
            return 1

        print(f"\n[HDR] Reintentando ({i + 2}/{max_iteraciones})...")
        time.sleep(1)

    print(f"\n[HDR] Limite de {max_iteraciones} ciclos alcanzado sin exito.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
