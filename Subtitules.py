import os
import whisper
import moviepy.editor as mp
from datetime import timedelta


# Asegúrate de que la variable de entorno IMAGEMAGICK_BINARY no esté presente
if "IMAGEMAGICK_BINARY" in os.environ:
    del os.environ["IMAGEMAGICK_BINARY"]

# Ruta al archivo de video
video_path = "VideoStore/rickyedit.mp4"
output_video_path = "output_video_with_subtitles.mp4"
output_srt_path = "output_subtitles.srt"

# Cargar el modelo Whisper
model = whisper.load_model("base")

# Paso 1: Extraer el audio del video
video = mp.VideoFileClip(video_path)
audio = video.audio
audio_path = "temp_audio.mp3"
audio.write_audiofile(audio_path)

# Paso 2: Transcribir el audio con Whisper
transcription = model.transcribe(audio_path, fp16=False)

# Paso 3: Generar archivo SRT
def generate_srt(transcription, srt_path):
    with open(srt_path, "w", encoding="utf-8") as f:
        for i, segment in enumerate(transcription['segments']):
            # Convertir los tiempos a minutos, segundos y omitir milisegundos
            start_time = str(timedelta(seconds=int(segment['start'])))
            end_time = str(timedelta(seconds=int(segment['end'])))

            # Asegurarse de que el formato sea HH:MM:SS sin milisegundos
            start_time = start_time.split('.')[0]  # Eliminar milisegundos
            end_time = end_time.split('.')[0]      # Eliminar milisegundos

            text = segment['text']

            # Formatear el archivo SRT
            srt_segment = f"{i + 1}\n{start_time} --> {end_time}\n{text}\n\n"
            f.write(srt_segment)

# Generar archivo SRT
generate_srt(transcription, output_srt_path)

