"""Modulo para convertir texto a audio usando gTTS."""

from gtts import gTTS


def texto_a_audio(texto: str, archivo_salida: str = "audiolibro.mp3", idioma: str = "es") -> None:
    """Convierte el texto dado a un archivo MP3 usando gTTS."""
    try:
        tts = gTTS(text=texto, lang=idioma, slow=False)
        tts.save(archivo_salida)
    except Exception as e:
        raise RuntimeError(f"Error al generar el audio: {e}") from e
    print(f"Audio guardado como: {archivo_salida}")
