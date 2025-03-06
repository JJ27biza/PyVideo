import os
import time
import threading
from flask import Flask, send_from_directory
import pychromecast
import socket

#Este método crea un servidor local flask para poder enviar el video al chromecast por la ip y la ruta para su emision a traves del nombre y la ruta del video
def emit_in_local(video_path, nombre_chromecast):
    try:
        mi_ip = socket.gethostbyname(socket.gethostname())
        video_filename = os.path.basename(video_path)
        app = Flask(__name__)

        @app.route('/video')
        def serve_video():
            mime_type = 'video/mp4' if video_filename.endswith('.mp4') else 'video/x-matroska'
            return send_from_directory(os.path.dirname(video_path), video_filename, mimetype=mime_type)

        def start_server():
            app.run(host='0.0.0.0', port=5000, threaded=True, use_reloader=False)

        server_thread = threading.Thread(target=start_server)
        server_thread.daemon = True
        server_thread.start()

        time.sleep(2)
        video_url = f'http://{mi_ip}:5000/video'

        chromecasts, browser = pychromecast.get_chromecasts()
        if not chromecasts:
            print("No se encontraron dispositivos Chromecast.")
            return

        chromecast = next((cast for cast in chromecasts if cast.name == nombre_chromecast), None)
        if chromecast is None:
            print(f"No se encontró un dispositivo Chromecast con el nombre: {nombre_chromecast}")
            return

        chromecast.wait()
        media_controller = chromecast.media_controller

        media_controller.play_media(video_url, 'video/mp4')
        media_controller.block_until_active()

        while not stop_event.is_set() and media_controller.status.player_state == 'PLAYING':
            time.sleep(1)

        if stop_event.is_set():
            media_controller.stop()

        func = request.environ.get('werkzeug.server.shutdown')
        if func:
            func()

    except Exception as error:
        print(f"Error al emitir el video: {error}")






