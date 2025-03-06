import moviepy.editor as mp
from datetime import timedelta
import re

#Método  para leer y procesar el archivo SRT para poder añadir en el video
def parse_srt(srt_file):
    with open(srt_file, "r", encoding="utf-8") as file:
        srt_text = file.read()

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
#Método donde se añaden los str al video y se guarda en VideoStoreSubtitles
def srt_To_Video(video_ruta):

    try:
        video_path='../VideoStore/'+video_ruta
        srt_path = video_ruta + "_subtitles.srt"
        output_video_path = '../VideoStoreSubtitles/'+video_ruta + "with_subtitles.mp4"

        video = mp.VideoFileClip(video_path)

        subtitles = parse_srt(srt_path)

        if not subtitles:
            print("No se encontraron subtítulos en el archivo SRT.")


        subtitle_clips = []
        for subtitle in subtitles:
            start_time = subtitle['start']
            end_time = subtitle['end']
            text = subtitle['text']

            subtitle_clip = mp.TextClip(text, fontsize=24, color='white', bg_color='black',
                                        size=(video.w, 80))  # Tamaño y altura ajustados
            subtitle_clip = subtitle_clip.set_position(('center', 'bottom'))  # Centrar el texto en la parte inferior
            subtitle_clip = subtitle_clip.set_duration(end_time - start_time).set_start(start_time)
            subtitle_clips.append(subtitle_clip)


        video_with_subtitles = mp.CompositeVideoClip([video] + subtitle_clips)

        video_with_subtitles.write_videofile(output_video_path, codec="libx264", fps=video.fps)




    except Exception as error:
        print('Error en el paso de str_to_video',error)

