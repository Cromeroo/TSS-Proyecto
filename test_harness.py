"""test_harness.py - Arnes de pruebas para pdf_to_audio.py (HDD)"""

import os
import sys
import json
import subprocess
import time
import ast

try:
    from reportlab.pdfgen import canvas
except ImportError:
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "reportlab"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    from reportlab.pdfgen import canvas


RUTAS_A_LIMPIAR = []


def generate_mock_pdf(filename, texto="Prueba de texto extraible."):
    """Genera un PDF sintetico para las pruebas."""
    c = canvas.Canvas(filename)
    c.drawString(100, 750, texto)
    c.save()
    RUTAS_A_LIMPIAR.append(filename)


def revisar_try_except_en_source(ruta_script):
    """Verifica que los modulos fuente tengan bloques try-except (skills.md)."""
    modulos = [ruta_script, "src/extractor.py", "src/converter.py", "src/cli.py"]
    resultados = {}
    for mod in modulos:
        if not os.path.exists(mod):
            resultados[mod] = "NO_ENCONTRADO"
            continue
        with open(mod, "r", encoding="utf-8") as f:
            try:
                arbol = ast.parse(f.read())
            except SyntaxError:
                resultados[mod] = "ERROR_SINTAXIS"
                continue
        tiene_try = any(
            isinstance(nodo, ast.Try) for nodo in ast.walk(arbol)
        )
        resultados[mod] = "PASSED" if tiene_try else "FAILED"
    return resultados


def limpiar():
    for r in RUTAS_A_LIMPIAR:
        if os.path.exists(r):
            os.remove(r)


def ejecutar_comando(args):
    """Ejecuta pdf_to_audio.py con argumentos y devuelve el proceso."""
    return subprocess.run(
        [sys.executable, "pdf_to_audio.py"] + args,
        capture_output=True, text=True
    )


def execute_harness():
    print("[HARNESS] Iniciando ciclo de evaluacion automatizado...")

    mock_input = "harness_test_input.pdf"
    expected_output = "audiolibro.mp3"

    limpiar()

    report = {
        "timestamp": time.time(),
        "harness_status": "FAILED",
        "assertions": {},
        "errors": []
    }

    # === 1. Generar PDF de prueba ===
    try:
        generate_mock_pdf(mock_input)
        report["assertions"]["input_generation"] = "PASSED"
    except Exception as e:
        report["assertions"]["input_generation"] = "FAILED"
        report["errors"].append(f"Error al generar PDF: {e}")
        write_report(report)
        return False

    # === 2. Verificar try-except en source (skills.md) ===
    resultados_try = revisar_try_except_en_source("pdf_to_audio.py")
    todos_try_ok = True
    for mod, res in resultados_try.items():
        key = f"try_except_{os.path.basename(mod).replace('.py','')}"
        report["assertions"][key] = res
        if res == "FAILED":
            todos_try_ok = False
            report["errors"].append(f"Modulo '{mod}' no tiene bloques try-except")
        elif res == "NO_ENCONTRADO":
            todos_try_ok = False
            report["errors"].append(f"Modulo '{mod}' no encontrado")

    # === 3. Happy path: ejecucion normal ===
    start = time.time()
    process = ejecutar_comando([mock_input])
    elapsed = round(time.time() - start, 2)
    report["execution_time_seconds"] = elapsed

    report["assertions"]["happy_exit_code"] = "PASSED" if process.returncode == 0 else "FAILED"
    if process.returncode != 0:
        report["errors"].append(
            f"Happy path fallo (exit {process.returncode}): {process.stderr.strip()}"
        )

    if os.path.exists(expected_output):
        report["assertions"]["happy_output_exists"] = "PASSED"
        tam = os.path.getsize(expected_output)
        report["assertions"]["happy_output_size"] = "PASSED" if tam > 5000 else "FAILED"
        if tam <= 5000:
            report["errors"].append(f"MPG generado pero muy pequeno ({tam} bytes)")
        os.remove(expected_output)
    else:
        report["assertions"]["happy_output_exists"] = "FAILED"
        report["assertions"]["happy_output_size"] = "FAILED"
        report["errors"].append("No se genero audiolibro.mp3 en happy path")

    # === 4. Sin argumentos ===
    p = ejecutar_comando([])
    report["assertions"]["no_args_exit_code"] = "PASSED" if p.returncode != 0 else "FAILED"
    if p.returncode == 0:
        report["errors"].append("Script deberia fallar sin argumentos pero retorno 0")

    # === 5. Archivo inexistente ===
    p = ejecutar_comando(["no_existe.pdf"])
    report["assertions"]["file_not_found"] = "PASSED" if p.returncode != 0 else "FAILED"
    if p.returncode == 0:
        report["errors"].append("Script deberia fallar con PDF inexistente pero retorno 0")

    # === 6. Flag --output personalizado ===
    custom_out = "custom_test.mp3"
    p = ejecutar_comando([mock_input, "--output", custom_out])
    if p.returncode == 0 and os.path.exists(custom_out):
        report["assertions"]["custom_output"] = "PASSED"
        os.remove(custom_out)
    else:
        report["assertions"]["custom_output"] = "FAILED"
        report["errors"].append(
            f"Flag --output no funciono (exit {p.returncode}): {p.stderr.strip()}"
        )

    # === Estado global ===
    fallos = [k for k, v in report["assertions"].items() if v == "FAILED"]
    if not fallos:
        report["harness_status"] = "SUCCESS"
        print("[HARNESS] Todas las pruebas pasaron con exito.")
    else:
        print(f"[HARNESS] Evaluacion fallida en: {', '.join(fallos)}")

    limpiar()
    write_report(report)
    return report["harness_status"] == "SUCCESS"


def write_report(data):
    with open("harness_report.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print("[HARNESS] Reporte guardado en 'harness_report.json'.")


if __name__ == "__main__":
    execute_harness()
