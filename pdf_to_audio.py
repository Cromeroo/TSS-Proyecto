"""
pdf_to_audio.py

Script que toma un archivo PDF local, extrae su texto usando pypdf
y convierte ese texto en un archivo MP3 llamado audiolibro.mp3
usando gTTS (Google Text-to-Speech).

Uso:
    python pdf_to_audio.py ruta/al/archivo.pdf
"""

import sys
from pathlib import Path

from gtts import gTTS
from pypdf import PdfReader


def extraer_texto_pdf(ruta_pdf: str) -> str:
    """Extrae y devuelve todo el texto de un archivo PDF."""
    lector = PdfReader(ruta_pdf)
    texto_completo = []
    for num_pagina, pagina in enumerate(lector.pages, start=1):
        texto = pagina.extract_text()
        if texto:
            texto_completo.append(texto)
    return "\n".join(texto_completo)


def texto_a_audio(texto: str, archivo_salida: str = "audiolibro.mp3") -> None:
    """Convierte el texto dado a un archivo MP3 usando gTTS."""
    tts = gTTS(text=texto, lang="es", slow=False)
    tts.save(archivo_salida)
    print(f"Audio guardado como: {archivo_salida}")


def main() -> None:
    if len(sys.argv) != 2:
        print("Uso: python pdf_to_audio.py <ruta_al_pdf>")
        sys.exit(1)

    ruta_pdf = sys.argv[1]

    if not Path(ruta_pdf).is_file():
        print(f"Error: No se encontró el archivo '{ruta_pdf}'")
        sys.exit(1)

    print(f"Extrayendo texto de: {ruta_pdf}")
    texto = extraer_texto_pdf(ruta_pdf)

    if not texto.strip():
        print("Error: El PDF no contiene texto extraíble.")
        sys.exit(1)

    print("Convirtiendo texto a audio...")
    texto_a_audio(texto)


if __name__ == "__main__":
    main()
