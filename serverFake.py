import os
import time
import threading
from flask import Flask, send_from_directory
from future.standard_library import import_top_level_modules

##inicializar server al querer enviar un video y seleccionar un archivo de video que querrramos enviar

# Configura la ruta al video local
video_path = '../VideoStore/Qué es una integral. Explicación desde cero - Matemáticas con Juan (720p, h264).mp4'  # Cambia esta ruta a la ruta de tu video
video_filename = os.path.basename(video_path)

# Crear una aplicación Flask para servir el video
app = Flask(__name__)

# Ruta para servir el archivo de video
@app.route('/descarga')
def serve_video():
    mime_type = 'video/mp4' if video_filename.endswith('.mp4') else 'video/x-matroska'  # Cambia según tu tipo de archivo
    print(f"Sirviendo el archivo {video_filename} con MIME {mime_type}")

# Función para iniciar el servidor HTTP
def start_server():
    app.run(host='0.0.0.0', port=5000, threaded=True, use_reloader=False)  # `use_reloader=False` evita la reinicialización en desarrollo

# Iniciar el servidor HTTP en un hilo separado
server_thread = threading.Thread(target=start_server)
server_thread.daemon = True
server_thread.start()

# Esperar a que el servidor se inicie
time.sleep(2)


video_url = 'http://192.168.8.103:5000/video'  # Usa la IP local de tu máquina
#añadir url en patalla para copiar y pegar en el dispositivo destinatario

# Evitar que el servidor Flask se cierre
while True:
    time.sleep(60)