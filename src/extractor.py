"""Modulo para extraer texto de archivos PDF."""

from pathlib import Path

from pypdf import PdfReader


def extraer_texto_pdf(ruta_pdf: str) -> str:
    """Extrae y devuelve todo el texto de un archivo PDF."""
    if not Path(ruta_pdf).is_file():
        raise FileNotFoundError(f"No se encontro el archivo '{ruta_pdf}'")

    try:
        lector = PdfReader(ruta_pdf)
    except Exception as e:
        raise RuntimeError(f"Error al leer el PDF '{ruta_pdf}': {e}") from e

    texto_completo = []
    for pagina in lector.pages:
        try:
            texto = pagina.extract_text()
            if texto:
                texto_completo.append(texto)
        except Exception as e:
            print(f"Advertencia: No se pudo extraer texto de una pagina: {e}")

    texto_final = "\n".join(texto_completo)
    if not texto_final.strip():
        raise ValueError("El PDF no contiene texto extraible.")

    return texto_final
