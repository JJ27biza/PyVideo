import os
import time
import threading
from flask import Flask, send_from_directory
import socket
from werkzeug.serving import make_server

# Variable global para el hilo del servidor, el evento de apagado y la ip local
server_thread = None
http_server = None
server_shutdown_event = threading.Event()
mi_ip = socket.gethostbyname(socket.gethostname())

#Método que permite tener subido un video en un servidor local durante un minuto
def enviarVideo(video_filename):
    try:
        video_directory = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'VideoStore'))

        if not os.path.exists(os.path.join(video_directory, video_filename)):
            print(f"El archivo {video_filename} no se encuentra en la ruta especificada.")
            return

        app = Flask(__name__)

        @app.route('/descarga')
        def serve_video():
            print(f"Ruta al archivo de video: {video_directory}")
            mime_type = 'video/mp4' if video_filename.endswith('.mp4') else 'video/x-matroska'
            print(f"Sirviendo el archivo {video_filename} con MIME {mime_type}")
            return send_from_directory(video_directory, video_filename, as_attachment=True, mimetype=mime_type)

        def start_server():
            global http_server
            http_server = make_server('0.0.0.0', 5000, app)
            http_server.serve_forever()

        global server_thread
        server_thread = threading.Thread(target=start_server)
        server_thread.daemon = True
        server_thread.start()


        time.sleep(60)


        shutdown_server()

    except Exception as error:
        print('Error en el envio de video', error)

#Este método permite apagar el sevidor
def shutdown_server():
    global http_server
    if http_server:
        http_server.shutdown()
    if server_thread:
        server_thread.join()

