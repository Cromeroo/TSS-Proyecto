import os
import sys
import json
import subprocess
import time

# Intentar importar reportlab para generar el PDF de prueba programáticamente
try:
    from reportlab.pdfgen import canvas
except ImportError:
    print("[HARNESS] Instalando dependencia requerida para el arnés: reportlab...")
    subprocess.run([sys.executable, "-m", "pip", "install", "reportlab"], stdout=subprocess.DEVNULL)
    from reportlab.pdfgen import canvas

def generate_mock_pdf(filename):
    """STUB: Genera un archivo PDF sintético controlado para la prueba"""
    c = canvas.Canvas(filename)
    c.drawString(100, 750, "Prueba de arquitectura agéntica.")
    c.drawString(100, 730, "El arnés de ingeniería ha validado que este texto fue extraído e interpretado.")
    c.save()

def execute_harness():
    print("[HARNESS] Iniciando ciclo de evaluacion automatizado...")
    
    # Configuración de rutas
    target_script = "pdf_to_audio.py"
    mock_input = "harness_test_input.pdf"
    expected_output = "audiolibro.mp3"
    
    # Limpieza de entorno previo
    for f in [mock_input, expected_output]:
        if os.path.exists(f): os.remove(f)

    report = {
        "timestamp": time.time(),
        "harness_status": "FAILED",
        "assertions": {},
        "errors": []
    }

    # 1. Fase de generación de Input sintético
    try:
        generate_mock_pdf(mock_input)
        report["assertions"]["input_generation"] = "PASSED"
    except Exception as e:
        report["assertions"]["input_generation"] = "FAILED"
        report["errors"].append(f"Error al generar PDF sintético: {str(e)}")
        write_report(report)
        return False

    # 2. Fase de ejecución (Driver)
    start_time = time.time()
    process = subprocess.run(
        [sys.executable, target_script, mock_input],
        capture_output=True,
        text=True
    )
    execution_time = time.time() - start_time
    report["execution_time_seconds"] = round(execution_time, 2)

    # 3. Matriz de Validación (Assertions)
    report["assertions"]["script_exit_code"] = "PASSED" if process.returncode == 0 else "FAILED"
    
    if process.returncode != 0:
        report["errors"].append(f"El script falló con exit code {process.returncode}. Stderr: {process.stderr.strip()}")
    
    # Validar existencia y calidad del output
    if os.path.exists(expected_output):
        report["assertions"]["output_file_exists"] = "PASSED"
        file_size = os.path.getsize(expected_output)
        report["assertions"]["output_size_valid"] = "PASSED" if file_size > 5000 else "FAILED"
        if file_size <= 5000:
            report["errors"].append(f"El archivo MP3 se generó pero está corrupto o casi vacío ({file_size} bytes).")
    else:
        report["assertions"]["output_file_exists"] = "FAILED"
        report["assertions"]["output_size_valid"] = "FAILED"
        report["errors"].append("El script terminó pero jamás generó el archivo 'audiolibro.mp3'.")

    # Determinar estado global
    failed_assertions = [k for k, v in report["assertions"].items() if v == "FAILED"]
    if not failed_assertions:
        report["harness_status"] = "SUCCESS"
        print("[HARNESS] Todas las pruebas pasaron con exito.")
    else:
        print(f"[HARNESS] Evaluacion fallida en: {', '.join(failed_assertions)}")

    write_report(report)
    return report["harness_status"] == "SUCCESS"

def write_report(data):
    with open("harness_report.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print("[HARNESS] Reporte estructurado guardado en 'harness_report.json'.")

if __name__ == "__main__":
    execute_harness()