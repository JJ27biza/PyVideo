import moviepy.editor as mp
from datetime import timedelta
import re

# Función para leer y procesar el archivo SRT
def parse_srt(srt_file):
    with open(srt_file, "r", encoding="utf-8") as file:
        srt_text = file.read()

    # Expresión regular actualizada para extraer subtítulos (horas, minutos, segundos)
    pattern = r'(\d+)\s*(\d{1,2}):(\d{2}):(\d{2}) --> (\d{1,2}):(\d{2}):(\d{2})\s*([\s\S]*?)(?=\n\d+\s|\Z)'
    matches = re.findall(pattern, srt_text)

    subtitles = []
    for match in matches:
        start_time = timedelta(hours=int(match[1]), minutes=int(match[2]), seconds=int(match[3]))
        end_time = timedelta(hours=int(match[4]), minutes=int(match[5]), seconds=int(match[6]))
        text = match[7].replace('\n', ' ')  # Reemplazar saltos de línea por espacios

        subtitles.append({
            "start": start_time.total_seconds(),
            "end": end_time.total_seconds(),
            "text": text
        })

    return subtitles


# Ruta al archivo de video y al archivo SRT
video_path = "VideoStore/rickyedit.mp4"
srt_path = "output_subtitles.srt"
output_video_path = "output_video_with_subtitles.mp4"

# Cargar el video
video = mp.VideoFileClip(video_path)

# Leer y procesar los subtítulos desde el archivo SRT
subtitles = parse_srt(srt_path)

# Verificar si los subtítulos fueron extraídos correctamente
if not subtitles:
    print("No se encontraron subtítulos en el archivo SRT.")
else:
    print(f"Total de subtítulos extraídos: {len(subtitles)}")

# Crear una lista de clips de texto para cada subtítulo
subtitle_clips = []
for subtitle in subtitles:
    start_time = subtitle['start']
    end_time = subtitle['end']
    text = subtitle['text']

    # Crear el clip de texto para cada subtítulo
    subtitle_clip = mp.TextClip(text, fontsize=24, color='white', bg_color='black',
                                size=(video.w, 80))  # Tamaño y altura ajustados
    subtitle_clip = subtitle_clip.set_position(('center', 'bottom'))  # Centrar el texto en la parte inferior
    subtitle_clip = subtitle_clip.set_duration(end_time - start_time).set_start(start_time)
    subtitle_clips.append(subtitle_clip)

# Verificar si se están agregando los subtítulos correctamente
print(f"Total de clips de subtítulos generados: {len(subtitle_clips)}")

# Combinar los clips de subtítulos con el video original (sin audio)
video_with_subtitles = mp.CompositeVideoClip([video] + subtitle_clips)

# Guardar el video con subtítulos
video_with_subtitles.write_videofile(output_video_path, codec="libx264", fps=video.fps)

print(f"Video con subtítulos guardado en {output_video_path}")
