import os
import time
import threading
from flask import Flask, send_from_directory
import pychromecast
import socket

def emit_in_local(video_path,nombre_chromecast):
    try:
        print('Video',video_path)
        mi_ip = socket.gethostbyname(socket.gethostname())
        video_filename = os.path.basename(video_path)

        # Crear una aplicación Flask para servir el video
        app = Flask(__name__)

        # Ruta para servir el archivo de video
        @app.route('/video')
        def serve_video():
            mime_type = 'video/mp4' if video_filename.endswith(
                '.mp4') else 'video/x-matroska'  # Cambia según tu tipo de archivo
            print(f"Sirviendo el archivo {video_filename} con MIME {mime_type}")
            return send_from_directory(os.path.dirname(video_path), video_filename, mimetype=mime_type)

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

        # Obtener la IP de la máquina en lugar de 'localhost' para que otros dispositivos puedan acceder
        video_url = 'http://'+mi_ip+':5000/video'  # Usa la IP local de tu máquina

        # Descubre los dispositivos Chromecast disponibles en la red
        chromecasts, browser = pychromecast.get_chromecasts()

        # Verifica que se hayan encontrado dispositivos Chromecast
        if not chromecasts:
            print("No se encontraron dispositivos Chromecast.")
            exit()

        # Buscar el Chromecast por nombre
        chromecast = None
        for cast in chromecasts:
            if cast.name == nombre_chromecast:
                chromecast = cast
                break

        if chromecast is None:
            print(f"No se encontró un dispositivo Chromecast con el nombre: {nombre_chromecast}")
            exit()

        print(f"Conectando al dispositivo: {chromecast.name}")
        chromecast.wait()

        # Obtener el controlador de medios
        media_controller = chromecast.media_controller

        # Verifica si el Chromecast está listo para reproducir medios
        if not media_controller.status or media_controller.status.player_state == 'IDLE':
            print("El Chromecast no está listo para reproducir.")
            exit()

        # Reproducir el video utilizando el media_controller
        print("Reproduciendo el video...")
        media_controller.play_media(video_url, 'video/mp4')  # Usa el formato correcto para el archivo

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

        # Evitar que el servidor Flask se cierre
        while True:
            time.sleep(60)  # Mantén el servidor funcionando indefinidamente

    except Exception as error:
        print(error)
