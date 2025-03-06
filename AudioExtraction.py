from moviepy.editor import *
import traceback

#Método para extraer el audio de un video
def extraction_Audio(video_path):
    try:
        video = VideoFileClip(video_path)
        audio = video.audio
        audio_path = video_path + "_audio.mp3"
        audio.write_audiofile(audio_path)
        return audio_path
    except Exception as error:
        print('Error al obtener el audio del video')
        print(str(error))
        traceback.print_exc()

