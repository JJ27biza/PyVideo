import os
import time
import threading
from flask import Flask, send_from_directory
import pychromecast

# Configura la ruta al video local
video_path = '../VideoStore/SuperSalto.mkv'  # Cambia esta ruta a la ruta de tu video
video_filename = os.path.basename(video_path)

# Crear una aplicación Flask para servir el video
app = Flask(__name__)

# Ruta para servir el archivo de video
@app.route('/video')
def serve_video():
    # Sirve el archivo con el tipo MIME adecuado según el formato de video
    mime_type = 'video/mp4' if video_filename.endswith('.mp4') else 'video/mkv'  # Cambia según tu tipo de archivo
    print(f"Sirviendo el archivo {video_filename} con MIME {mime_type}")
    return send_from_directory(os.path.dirname(video_path), video_filename, mimetype=mime_type)

# Función para iniciar el servidor HTTP
def start_server():
    app.run(host='0.0.0.0', port=5000, threaded=True)

# Iniciar el servidor HTTP en un hilo separado
server_thread = threading.Thread(target=start_server)
server_thread.daemon = True
server_thread.start()

# Esperar a que el servidor se inicie
time.sleep(2)

# URL local donde el servidor sirve el video
video_url = 'http://localhost:5000/video'

# Descubre los dispositivos Chromecast disponibles en la red
chromecasts, browser = pychromecast.get_chromecasts()

# Verifica que se hayan encontrado dispositivos Chromecast
if not chromecasts:
    print("No se encontraron dispositivos Chromecast.")
    exit()

# Conectar al primer Chromecast encontrado
chromecast = chromecasts[0]
print(f"Conectando al dispositivo: {chromecast.name}")
chromecast.wait()

# Obtener el controlador de medios
media_controller = chromecast.media_controller

# Reproducir el video utilizando el media_controller
print("Reproduciendo el video...")
media_controller.play_media(video_url, 'video/mp4')  # Asegúrate de usar el formato correcto

# Espera a que el video esté listo para reproducirse
media_controller.block_until_active()  # Bloquea hasta que el video comience a reproducirse

# Verifica si el video está reproduciéndose
start_time = time.time()
while media_controller.status.player_state != 'PLAYING' and time.time() - start_time < 30:
    print(f"Esperando que el video se reproduzca... Estado actual: {media_controller.status.player_state}")
    time.sleep(1)

if media_controller.status.player_state == 'PLAYING':
    print("El video se está reproduciendo con éxito.")
else:
    print("No se pudo reproducir el video. Estado actual:", media_controller.status.player_state)
