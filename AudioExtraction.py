from moviepy.editor import *
import traceback

def extraction_Audio(video_path):
    try:
        video = VideoFileClip(video_path)
        audio = video.audio
        audio.write_audiofile(video_path + "audio.mp3")
    except Exception as error:
        print('Error al obtener el audio del video')
        print(str(error))
        traceback.print_exc()

if __name__ == '__main__':
    extraction_Audio('VideoStore/integrale.mp4')
