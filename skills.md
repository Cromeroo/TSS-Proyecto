\# OpenCode Agent Skills \& Rules



Este archivo define las directrices obligatorias, flujos de trabajo de ingeniería y arneses de automatización para todas las tareas de este repositorio. El agente debe consultar este archivo antes de ejecutar cualquier acción.



\## 1. Reglas de Desarrollo (Core Skills)

\- \*\*Idioma Estricto:\*\* Toda interacción, comentarios en el código, documentación y strings visibles deben estar exclusivamente en español latinoamericano.

\- \*\*Robustez de Código:\*\* Todo script de Python debe implementar bloques `try-except` explícitos para el manejo de excepciones, especialmente al interactuar con el sistema de archivos (I/O) o APIs externas.

\- \*\*Validación de Datos:\*\* Si un script interactúa con payloads JSON, entradas de usuario o configuraciones, se debe priorizar el uso de la librería `Pydantic` para garantizar la validación estricta de los tipos de datos.



\## 2. Convenciones de Control de Versiones (Git Harness)

\- \*\*Formato de Commits:\*\* Todos los mensajes de commit generados automáticamente por el agente deben seguir estrictamente la especificación de \*Conventional Commits\*. Ejemplos aceptados:

&#x20; - `feat(audio): añade soporte para extracción de texto en pdf\_to\_audio.py`

&#x20; - `fix(clima): corrige manejo de timeout en la petición HTTP`

&#x20; - `docs(readme): actualiza instrucciones de instalación en el entorno virtual`

\- \*\*Gestión de Entornos:\*\* No subir jamás binarios, entornos virtuales (`.venv/`, `venv/`), archivos temporales de audio (`.mp3`), PDFs de prueba, o carpetas de caché (`\_\_pycache\_\_/`). Todo debe estar correctamente mapeado en el archivo `.gitignore`.



\## 3. Optimización de Hardware Local (Performance Tuning)

\- Este entorno de desarrollo está respaldado por una GPU dedicada Radeon de 16GB de VRAM y un procesador Ryzen 9 de alto rendimiento. 

\- Al proponer arquitecturas o procesamiento local de IA (como embeddings de texto locales o modelos de machine learning ligeros), asume que el sistema cuenta con suficiente memoria caché y ancho de banda de GPU para paralelizar tareas intensivas.

