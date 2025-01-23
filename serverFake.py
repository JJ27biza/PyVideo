import os
import time
import threading
from flask import Flask, send_from_directory
import socket

#ip privada
mi_ip=socket.gethostbyname(socket.gethostname())

video_directory = os.path.abspath(os.path.join(os.path.dirname(__file__),'VideoStore'))  # Ruta absoluta desde el directorio del script
video_filename = '2024-12-25 20-30-52.mkv'  # Nombre del archivo de video

# Verificar si el archivo existe
if not os.path.exists(os.path.join(video_directory, video_filename)):
    print(f"El archivo {video_filename} no se encuentra en la ruta especificada.")
    exit(1)  # Termina el script si el archivo no existe

# Crear una aplicación Flask para servir el video
app = Flask(__name__)


# Ruta para servir el archivo de video
@app.route('/descarga')
def serve_video():
    # Verificar la ruta al archivo de video
    print(f"Ruta al archivo de video: {video_directory}")

    # Determinar el tipo MIME del archivo
    mime_type = 'video/mp4' if video_filename.endswith('.mp4') else 'video/x-matroska'
    print(f"Sirviendo el archivo {video_filename} con MIME {mime_type}")

    # Servir el archivo para descarga
    return send_from_directory(video_directory, video_filename, as_attachment=True, mimetype=mime_type)


# Función para iniciar el servidor HTTP
def start_server():
    app.run(host='0.0.0.0', port=5000, threaded=True,
            use_reloader=False)  # `use_reloader=False` evita la reinicialización en desarrollo


# Iniciar el servidor HTTP en un hilo separado
server_thread = threading.Thread(target=start_server)
server_thread.daemon = True
server_thread.start()

# Esperar a que el servidor se inicie
time.sleep(2)

# Puedes mostrar la URL para copiar y pegar en otro dispositivo
video_url = 'http://'+mi_ip+':5000/descarga'
print(f"Accede a la URL para descargar el video: {video_url}")

# Evitar que el servidor Flask se cierre
while True:
    time.sleep(60)

