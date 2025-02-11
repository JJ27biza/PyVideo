import os
import time
import threading
from flask import Flask, send_from_directory
import socket
from werkzeug.serving import make_server

# Variable global para el hilo del servidor y el evento de apagado
server_thread = None
http_server = None
server_shutdown_event = threading.Event()

mi_ip = socket.gethostbyname(socket.gethostname())  # Obtener la IP local

def enviarVideo(video_filename):
    try:
        # Verificar si el archivo existe
        video_directory = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'VideoStore'))  # Ruta absoluta desde el directorio del script

        if not os.path.exists(os.path.join(video_directory, video_filename)):
            print(f"El archivo {video_filename} no se encuentra en la ruta especificada.")
            return  # Termina la función si el archivo no existe

        # Crear una aplicación Flask para servir el video
        app = Flask(__name__)

        # Ruta para servir el archivo de video
        @app.route('/descarga')
        def serve_video():
            print(f"Ruta al archivo de video: {video_directory}")
            mime_type = 'video/mp4' if video_filename.endswith('.mp4') else 'video/x-matroska'
            print(f"Sirviendo el archivo {video_filename} con MIME {mime_type}")
            return send_from_directory(video_directory, video_filename, as_attachment=True, mimetype=mime_type)

        # Función para iniciar el servidor HTTP
        def start_server():
            global http_server
            # Usamos make_server para poder detener el servidor después
            http_server = make_server('0.0.0.0', 5000, app)
            # En lugar de serve_forever(), utilizamos un bucle que comprueba el evento de apagado
            http_server.serve_forever()

        # Iniciar el servidor HTTP en un hilo separado
        global server_thread
        server_thread = threading.Thread(target=start_server)
        server_thread.daemon = True
        server_thread.start()

        # Esperar 60 segundos antes de apagar el servidor automáticamente
        print(f"El servidor estará disponible durante 1 minuto para la descarga del video en: http://{mi_ip}:5000/descarga")
        time.sleep(60)  # Esperar un minuto antes de apagar el servidor

        # Apagar el servidor después de 1 minuto
        print("Tiempo de servidor agotado. Apagando el servidor...")
        shutdown_server()

    except Exception as error:
        print('Error en el envio de video', error)

# Mover la función de apagado fuera de la función enviarVideo
def shutdown_server():
    global http_server
    if http_server:
        http_server.shutdown()  # Detener el servidor de forma controlada
    if server_thread:
        server_thread.join()  # Asegurarse de que el hilo termine

if __name__=="__main__":
    enviarVideo('')