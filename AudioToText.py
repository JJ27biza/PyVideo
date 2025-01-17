import os
import whisper

# Ruta del archivo de audio
audio_file_path = ('VideoStore/integrale.mp3')

# Cargar el modelo de Whisper
model = whisper.load_model("base")


def transcribe_audio(audio_path):
    try:
        # Verificar si el archivo de audio existe
        if not os.path.exists(audio_path):
            print(f"Archivo de audio no encontrado: {audio_path}")
            return ''

        # Transcribir el audio
        result = model.transcribe(audio_path, fp16=False)
        text = result['text']

        print(f"Audio transcrito: {audio_path}")
        print(f"Texto: {text}")
        return text
    except Exception as e:
        print(f"Error al transcribir el audio {audio_path}: {e}")
        return ''


# Llamar a la función de transcripción
transcription = transcribe_audio(audio_file_path)

# Verificar si la transcripción fue exitosa
if transcription:
    # Definir la ruta para guardar el archivo de texto con la transcripción
    text_file_path = os.path.splitext(audio_file_path)[0] + '_transcription.txt'

    # Guardar la transcripción en un archivo de texto
    with open(text_file_path, 'w') as file:
        file.write(transcription)

    print(f"Transcripción guardada en: {text_file_path}")
else:
    print("No se pudo transcribir el audio.")
