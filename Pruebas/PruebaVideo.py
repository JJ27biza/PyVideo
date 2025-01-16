import os
import time
import threading
from flask import Flask, send_from_directory

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

# Reproducir el video en un bucle infinito
while True:
    print("Reproduciendo el video...")
    time.sleep(1)  # Simulamos que el video se está reproduciendo (solo como referencia)

    # Aquí puedes agregar alguna lógica para reiniciar o comprobar que el video se sirvió correctamente.
    # Este es un bucle simple, en el que el servidor seguirá sirviendo el video sin intervención.

    # Espera 30 segundos antes de simular que el video ha terminado y reiniciarlo.
    time.sleep(30)  # Ajusta este tiempo según la duración del video
    print("El video ha terminado. Reiniciando la reproducción...")
