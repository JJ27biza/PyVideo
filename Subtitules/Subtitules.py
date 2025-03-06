import os
import whisper
import moviepy.editor as mp
from datetime import timedelta

#Método para generar str en un archivo
def generate_srt(transcription, srt_path):
    with open(srt_path, "w", encoding="utf-8") as f:
        for i, segment in enumerate(transcription['segments']):
            start_time = str(timedelta(seconds=int(segment['start'])))
            end_time = str(timedelta(seconds=int(segment['end'])))
            start_time = start_time.split('.')[0]
            end_time = end_time.split('.')[0]
            text = segment['text']
            srt_segment = f"{i + 1}\n{start_time} --> {end_time}\n{text}\n\n"
            f.write(srt_segment)

#Método para generar los str con Whisper
def str_Subtitules(video_ruta):
    if "IMAGEMAGICK_BINARY" in os.environ:
        del os.environ["IMAGEMAGICK_BINARY"]
    video_path='../VideoStore/'+video_ruta
    output_srt_path = video_ruta+"_subtitles.srt"

    model = whisper.load_model("base")

    video = mp.VideoFileClip(video_path)
    audio = video.audio
    audio_path = "temp_audio.mp3"
    audio.write_audiofile(audio_path)

    transcription = model.transcribe(audio_path, fp16=False)
    generate_srt(transcription, output_srt_path)




