# Historial de Contexto y Memoria del Agente

## Ultimo Estado del Repositorio

- **Proyecto:** TSS-Proyecto (Conversor de PDF a Audio).
- **Estado actual:** Script base `pdf_to_audio.py` funcional. Arnés de pruebas `test_harness.py` creado y ejecutado con exito (SUCCESS).

## Log de Aprendizaje (Lecciones Aprendidas por la IA)

- **Remote URL:** https://github.com/Cromeroo/TSS-Proyecto.git (recordado para futuros pushes)
- Los emojis en print() causan UnicodeEncodeError en Windows terminal (cp1252). Evitar emojis en outputs de scripts.
- `json.dump(data, indent=4)` requiere el argumento posicional `fp` (el file pointer). Error comun: `TypeError: dump() missing 1 required positional argument: 'fp'`.
- El arnés actual solo prueba el camino feliz. Hace falta validar manejo de errores (`try-except`) segun `skills.md`.
- `reportlab` auto-instalado via subprocess puede terminar en el Python del sistema, no en el venv. Mejor pre-instalarlo.
