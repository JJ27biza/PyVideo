import os
import time
import threading
from flask import Flask, send_file

# Configura la ruta al video local
video_path = '../VideoStore/SuperSalto.mkv'  # Cambia esta ruta a la ruta de tu video
video_filename = os.path.basename(video_path)

# Crear una aplicación Flask para servir el video
app = Flask(__name__)

# Ruta para servir el archivo de video
@app.route('/video')
def serve_video():
    # Sirve el archivo de video y establece el tipo MIME adecuado
    print(f"Sirviendo el archivo {video_filename}")
    return send_file(video_path, mimetype='video/x-matroska')  # Tipo MIME para MKV

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

