# Historial de Contexto y Memoria del Agente

## Ultimo Estado del Repositorio

- **Proyecto:** TSS-Proyecto (Conversor de PDF a Audio).
- **Branch actual:** develop
- **Remote:** https://github.com/Cromeroo/TSS-Proyecto.git
- **Estado:** Refactorización completa aplicada y arnes HDD en verde.

## Estructura del Proyecto

```
pdf_to_audio.py          # Entry point (thin wrapper)
src/
  __init__.py
  extractor.py           # Extraccion de texto PDF (con try-except)
  converter.py           # Conversion texto a MP3 via gTTS (con try-except)
  cli.py                 # CLI con argparse, validacion de args
test_harness.py          # Arnes HDD con 11 assertions
run_cycle.py             # Automatizador del ciclo HDD
INSTRUCCIONES.txt        # Prompt inicial para futuras sesiones
.github/workflows/test.yml  # CI/CD GitHub Actions
agents.md                # Instrucciones del sistema
skills.md                # Reglas de desarrollo
skills_agentes.md        # Skills de orquestacion
context_memory.md        # Este archivo (memoria del agente)
.gitignore
requirements.txt
README.md
```

## Log de Aprendizaje (Lecciones Aprendidas por la IA)

- Los emojis en print() causan UnicodeEncodeError en Windows terminal (cp1252). Evitarlos.
- `json.dump(data, f, indent=4)` requiere el argumento `fp`. Error comun olvidarlo.
- La auto-instalacion de reportlab via subprocess puede instalar en el Python del sistema, no en el venv. Mejor pre-instalar.
- Un entry point thin wrapper (pdf_to_audio.py) tambien necesita try-except para cumplir skills.md.
- skills.md exige: try-except en I/O y APIs externas, idioma espanol, argparse para argumentos.
- `ast.parse()` permite verificar estaticamente la presencia de try-except en el codigo fuente.
- El arnes HDD debe validar: happy path, casos borde (sin args, archivo inexistente), y presencia de try-except.

## Pruebas Realizadas

- `test_harness.py` ejecutado con exito: 11/11 assertions PASSED.
- `pdf_to_audio.py test_prueba.pdf` -> genera MP3 correctamente.
- `pdf_to_audio.py test_prueba.pdf --output custom.mp3` -> flag personalizado funciona.
- Flujo completo probado: extraccion -> conversion -> archivo valido (>5000 bytes).
