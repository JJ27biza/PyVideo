import os
import whisper
import moviepy.editor as mp
from datetime import timedelta

# Eliminar la variable de entorno IMAGEMAGICK_BINARY si existe
if "IMAGEMAGICK_BINARY" in os.environ:
    os.environ.pop("IMAGEMAGICK_BINARY")

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
            start_time = str(timedelta(seconds=segment['start']))
            end_time = str(timedelta(seconds=segment['end']))
            text = segment['text']

            # Formatear el archivo SRT
            srt_segment = f"{i + 1}\n{start_time.replace('.', ',')} --> {end_time.replace('.', ',')}\n{text}\n\n"
            f.write(srt_segment)


# Generar archivo SRT
generate_srt(transcription, output_srt_path)

# Paso 4: Crear los subtítulos con MoviePy sin usar ImageMagick
subtitles = []

# Generar clips de subtítulos basados en la transcripción
for segment in transcription['segments']:
    # Crear el clip de texto para cada segmento
    start_time = segment['start']
    end_time = segment['end']
    text = segment['text']

    subtitle = mp.TextClip(text, fontsize=24, color='white', bg_color='black', size=video.size)
    subtitle = subtitle.set_position(('center', 'bottom')).set_duration(end_time - start_time).set_start(start_time)
    subtitles.append(subtitle)

# Combinar el video original con los subtítulos
video_with_subtitles = mp.CompositeVideoClip([video] + subtitles)

# Guardar el video con subtítulos
video_with_subtitles.write_videofile(output_video_path, codec="libx264", fps=video.fps)

print(f"Subtítulos generados y guardados en {output_srt_path}")
print(f"Video con subtítulos guardado en {output_video_path}")


