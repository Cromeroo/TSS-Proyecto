"""Modulo de interfaz de linea de comandos con argparse."""

import argparse
import sys
from pathlib import Path

from src.extractor import extraer_texto_pdf
from src.converter import texto_a_audio


def configurar_argumentos() -> argparse.ArgumentParser:
    """Configura y devuelve el parser de argumentos."""
    parser = argparse.ArgumentParser(
        description="Convierte un archivo PDF a audio MP3 usando gTTS."
    )
    parser.add_argument(
        "pdf",
        type=str,
        help="Ruta al archivo PDF de entrada"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="audiolibro.mp3",
        help="Nombre del archivo MP3 de salida (default: audiolibro.mp3)"
    )
    parser.add_argument(
        "-l", "--lang",
        type=str,
        default="es",
        help="Idioma para el TTS (default: es)"
    )
    return parser


def main() -> None:
    """Punto de entrada principal."""
    parser = configurar_argumentos()
    args = parser.parse_args()

    if not Path(args.pdf).is_file():
        print(f"Error: No se encontro el archivo '{args.pdf}'")
        sys.exit(1)

    try:
        print(f"Extrayendo texto de: {args.pdf}")
        texto = extraer_texto_pdf(args.pdf)
        print("Convirtiendo texto a audio...")
        texto_a_audio(texto, args.output, args.lang)
    except (FileNotFoundError, ValueError, RuntimeError) as e:
        print(f"Error: {e}")
        sys.exit(1)
