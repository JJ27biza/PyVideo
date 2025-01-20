import whisper
import moviepy.editor as mp
from datetime import timedelta

# Ruta al archivo de video
video_path = "VideoStore/kolderiu.mp4"
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

# Paso 4: Adjuntar subtítulos al video
subtitles = mp.TextClip("Subtítulos", fontsize=24, color='white', bg_color='black')

# Agregar subtítulos al video
video_with_subtitles = video.subclip(0, video.duration).set_duration(video.duration).fx(mp.vfx.add_text, subtitles)

# Guardar el video con subtítulos
video_with_subtitles.write_videofile(output_video_path, codec="libx264", subtitles=output_srt_path)

print(f"Subtítulos generados y guardados en {output_srt_path}")
print(f"Video con subtítulos guardado en {output_video_path}")
